from .features import permission_sensitivity
from .ml import score_extension, ml_risk_adjustment
from .models import Assessment, Decision, Extension

def decision_for_score(score:int)->Decision:
    return Decision.CRITICAL if score>=75 else Decision.HIGH_RISK if score>=50 else Decision.REVIEW if score>=25 else Decision.NORMAL

def rule_score(e:Extension)->int:
    score=permission_sensitivity(e)
    if not e.publisher_verified: score+=12
    if e.permission_delta>=2: score+=16
    elif e.permission_delta==1: score+=7
    if e.update_channel!='stable': score+=8
    if e.session_access: score+=9
    if e.cookie_access: score+=14
    if e.external_posting: score+=9
    if e.oauth_bridge: score+=7
    if e.ai_assistant and (e.session_access or e.external_posting): score+=8
    ratio=e.observed_events/max(e.baseline_events,1)
    if ratio>=20: score+=16
    elif ratio>=3: score+=8
    if e.age_days>1200 and not e.publisher_verified: score+=7
    if e.active_users>=300: score+=8
    return min(score,100)

def assess(e:Extension)->Assessment:
    base=rule_score(e)
    reasons=[]; actions=[]
    if not e.publisher_verified: reasons.append('publisher is not verified')
    if e.permission_delta>=2: reasons.append('recent permission expansion')
    elif e.permission_delta==1: reasons.append('recent permission change')
    if e.update_channel!='stable': reasons.append('non-stable or external update channel')
    if e.session_access: reasons.append('can observe authenticated browser sessions')
    if e.cookie_access: reasons.append('cookie access increases session exposure')
    if e.external_posting: reasons.append('can send browser-derived data externally')
    if e.oauth_bridge: reasons.append('browser-to-OAuth/SaaS trust path present')
    if e.ai_assistant and (e.session_access or e.external_posting): reasons.append('AI assistant handles sensitive browser context')
    ratio=round(e.observed_events/max(e.baseline_events,1),1)
    if ratio>=20: reasons.append('extreme event-volume deviation')
    elif ratio>=3: reasons.append('material event-volume deviation')
    if e.age_days>1200 and not e.publisher_verified: reasons.append('legacy unverified extension remains installed')
    if e.active_users>=300: reasons.append('large user blast radius')

    ml=score_extension(e)
    adjustment=ml_risk_adjustment(ml['anomaly_score'])
    score=min(100,base+adjustment)
    decision=decision_for_score(score)
    if ml['outlier']:
        reasons.append(f"Isolation Forest flags behavior as anomalous ({ml['anomaly_score']:.1f}th normal-reference percentile)")

    if decision in (Decision.CRITICAL,Decision.HIGH_RISK):
        actions += ['review extension ownership and deployment source','compare current permissions with approved baseline']
    if e.cookie_access: actions.append('remove unnecessary cookie/session access')
    if e.permission_delta: actions.append('investigate the extension update that changed permissions')
    if e.external_posting: actions.append('review external destinations and data-handling policy')
    if ml['outlier']: actions.append('compare recent behavior with the learned normal-reference profile')
    if not actions: actions.append('continue routine monitoring')

    return Assessment(
        e.ext_id,e.name,decision,score,base,ml['anomaly_score'],ml['outlier'],adjustment,
        ratio,e.active_users,ml['top_feature_deviations'],reasons,actions
    )

def blast_radius(e:Extension):
    resources=['browser-session'] if e.session_access else []
    if e.cookie_access: resources.append('cookies')
    if e.oauth_bridge: resources.extend(['oauth-grants','saas-apps'])
    if e.ai_assistant: resources.append('ai-context')
    return {'extension':e.name,'users':e.active_users,'resources':resources,'nodes':1+e.active_users+len(resources),'edges':e.active_users+len(resources)}
