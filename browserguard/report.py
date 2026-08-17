from collections import Counter
from .fixtures import EXTENSIONS
from .engine import assess, blast_radius

def build_report():
    rows=[assess(e) for e in EXTENSIONS]
    counts=Counter(r.decision.value for r in rows)
    matches=sum(r.decision==e.expected for r,e in zip(rows,EXTENSIONS))
    return {'summary':{'extensions':len(rows),'expected_outcomes_matched':matches,'counts':dict(counts),'mean_risk_score':round(sum(r.risk_score for r in rows)/len(rows),1),'users_behind_high_or_critical':sum(r.users_exposed for r in rows if r.decision.value in ('HIGH_RISK','CRITICAL'))},'assessments':[r.to_dict() for r in rows],'blast_radius':{e.ext_id:blast_radius(e) for e in EXTENSIONS}}
