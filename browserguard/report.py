from collections import Counter
from .features import FEATURE_NAMES
from .fixtures import EXTENSIONS
from .engine import assess, blast_radius, decision_for_score
from .ml import MODEL_NAME, TRAINING_SAMPLES

def build_report():
    rows=[assess(e) for e in EXTENSIONS]
    counts=Counter(r.decision.value for r in rows)
    matches=sum(r.decision==e.expected for r,e in zip(rows,EXTENSIONS))
    changed=sum(decision_for_score(r.rule_score)!=r.decision for r in rows)
    return {
        'summary':{
            'extensions':len(rows),
            'expected_outcomes_matched':matches,
            'counts':dict(counts),
            'mean_risk_score':round(sum(r.risk_score for r in rows)/len(rows),1),
            'users_behind_high_or_critical':sum(r.users_exposed for r in rows if r.decision.value in ('HIGH_RISK','CRITICAL')),
            'ml_model':MODEL_NAME,
            'ml_outliers':sum(r.ml_outlier for r in rows),
            'mean_ml_anomaly_score':round(sum(r.ml_anomaly_score for r in rows)/len(rows),1),
            'hybrid_decisions_changed_vs_rules':changed,
        },
        'ml':{
            'model':MODEL_NAME,
            'normal_reference_samples':TRAINING_SAMPLES,
            'features':list(FEATURE_NAMES),
            'anomaly_score_meaning':'percentile relative to deterministic synthetic normal-reference behavior; not a probability',
        },
        'assessments':[r.to_dict() for r in rows],
        'blast_radius':{e.ext_id:blast_radius(e) for e in EXTENSIONS},
    }
