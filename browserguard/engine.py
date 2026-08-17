from .models import Assessment, Decision, Extension

SENSITIVE={'cookies':18,'<all_urls>':16,'clipboardRead':12,'webRequestBlocking':12,'scripting':10,'tabs':6,'webRequest':6,'identity':5}

def assess(e:Extension)->Assessment:
    score=sum(SENSITIVE.get(p,0) for p in e.permissions)
    reasons=[]; actions=[]
    if not e.publisher_verified: score+=12; reasons.append('publisher is not verified')
    if e.permission_delta>=2: score+=16; reasons.append('recent permission expansion')
    elif e.permission_delta==1: score+=7; reasons.append('recent permission change')
    if e.update_channel!='stable': score+=8; reasons.append('non-stable or external update channel')
    if e.session_access: score+=9; reasons.append('can observe authenticated browser sessions')
    if e.cookie_access: score+=14; reasons.append('cookie access increases session exposure')
    if e.external_posting: score+=9; reasons.append('can send browser-derived data externally')
    if e.oauth_bridge: score+=7; reasons.append('browser-to-OAuth/SaaS trust path present')
    if e.ai_assistant and (e.session_access or e.external_posting): score+=8; reasons.append('AI assistant handles sensitive browser context')
    ratio=round(e.observed_events/max(e.baseline_events,1),1)
    if ratio>=20: score+=16; reasons.append('extreme event-volume deviation')
    elif ratio>=3: score+=8; reasons.append('material event-volume deviation')
    if e.age_days>1200 and not e.publisher_verified: score+=7; reasons.append('legacy unverified extension remains installed')
    if e.active_users>=300: score+=8; reasons.append('large user blast radius')
    score=min(score,100)
    decision=Decision.CRITICAL if score>=75 else Decision.HIGH_RISK if score>=50 else Decision.REVIEW if score>=25 else Decision.NORMAL
    if decision in (Decision.CRITICAL,Decision.HIGH_RISK): actions += ['review extension ownership and deployment source','compare current permissions with approved baseline']
    if e.cookie_access: actions.append('remove unnecessary cookie/session access')
    if e.permission_delta: actions.append('investigate the extension update that changed permissions')
    if e.external_posting: actions.append('review external destinations and data-handling policy')
    if not actions: actions.append('continue routine monitoring')
    return Assessment(e.ext_id,e.name,decision,score,ratio,e.active_users,reasons,actions)

def blast_radius(e:Extension):
    resources=['browser-session'] if e.session_access else []
    if e.cookie_access: resources.append('cookies')
    if e.oauth_bridge: resources.extend(['oauth-grants','saas-apps'])
    if e.ai_assistant: resources.append('ai-context')
    return {'extension':e.name,'users':e.active_users,'resources':resources,'nodes':1+e.active_users+len(resources),'edges':e.active_users+len(resources)}
