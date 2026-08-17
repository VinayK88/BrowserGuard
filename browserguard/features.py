import math
from .models import Extension

PERMISSION_WEIGHTS={
    'cookies':18,'<all_urls>':16,'clipboardRead':12,'webRequestBlocking':12,
    'scripting':10,'tabs':6,'webRequest':6,'identity':5
}

FEATURE_NAMES=(
    'permission_sensitivity','permission_count','permission_delta','publisher_unverified',
    'update_risk','log_age_days','log_active_users','session_access','cookie_access',
    'ai_assistant','external_posting','oauth_bridge','log_event_ratio','resource_count'
)

def permission_sensitivity(e:Extension)->int:
    return sum(PERMISSION_WEIGHTS.get(p,0) for p in e.permissions)

def event_ratio(e:Extension)->float:
    return e.observed_events/max(e.baseline_events,1)

def resource_count(e:Extension)->int:
    return int(e.session_access)+int(e.cookie_access)+(2*int(e.oauth_bridge))+int(e.ai_assistant)

def feature_vector(e:Extension)->list[float]:
    update_risk={'stable':0,'beta':1,'external':2}.get(e.update_channel,1)
    return [
        float(permission_sensitivity(e)),
        float(len(e.permissions)),
        float(e.permission_delta),
        float(not e.publisher_verified),
        float(update_risk),
        math.log1p(e.age_days),
        math.log1p(e.active_users),
        float(e.session_access),
        float(e.cookie_access),
        float(e.ai_assistant),
        float(e.external_posting),
        float(e.oauth_bridge),
        math.log1p(event_ratio(e)),
        float(resource_count(e)),
    ]
