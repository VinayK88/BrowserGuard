from functools import lru_cache
import math
import random
import numpy as np
from sklearn.ensemble import IsolationForest
from .features import FEATURE_NAMES, feature_vector
from .models import Extension

MODEL_NAME='IsolationForest'
TRAINING_SAMPLES=800
RANDOM_STATE=41

def _normal_reference_corpus(n:int=TRAINING_SAMPLES, seed:int=RANDOM_STATE)->np.ndarray:
    rng=random.Random(seed)
    rows=[]
    for _ in range(n):
        permission_sensitivity=max(0,min(20,round(rng.gauss(5,4))))
        permission_count=max(1,min(5,round(rng.gauss(2.5,1))))
        permission_delta=0 if rng.random()<0.90 else 1
        publisher_unverified=1 if rng.random()<0.06 else 0
        update_risk=0 if rng.random()<0.94 else 1
        age_days=max(10,min(1600,int(rng.lognormvariate(math.log(350),0.75))))
        active_users=max(1,min(500,int(rng.lognormvariate(math.log(70),0.9))))
        session_access=1 if rng.random()<0.12 else 0
        cookie_access=1 if rng.random()<0.025 else 0
        ai_assistant=1 if rng.random()<0.10 else 0
        external_posting=1 if rng.random()<0.05 else 0
        oauth_bridge=1 if rng.random()<0.10 else 0
        ratio=max(0.2,min(4.0,rng.lognormvariate(math.log(1.0),0.35)))
        resource_count=session_access+cookie_access+(2*oauth_bridge)+ai_assistant
        rows.append([
            permission_sensitivity,permission_count,permission_delta,publisher_unverified,
            update_risk,math.log1p(age_days),math.log1p(active_users),session_access,
            cookie_access,ai_assistant,external_posting,oauth_bridge,math.log1p(ratio),
            resource_count,
        ])
    return np.asarray(rows,dtype=float)

@lru_cache(maxsize=1)
def _trained_model():
    X=_normal_reference_corpus()
    model=IsolationForest(
        n_estimators=200,
        max_samples='auto',
        contamination=0.08,
        random_state=RANDOM_STATE,
    )
    model.fit(X)
    abnormality=-model.decision_function(X)
    means=X.mean(axis=0)
    stds=X.std(axis=0)
    stds=np.where(stds<1e-9,1.0,stds)
    return model,abnormality,means,stds

def score_extension(e:Extension)->dict:
    model,reference_abnormality,means,stds=_trained_model()
    x=np.asarray([feature_vector(e)],dtype=float)
    abnormality=float(-model.decision_function(x)[0])
    percentile=float((reference_abnormality<=abnormality).mean()*100)
    outlier=bool(model.predict(x)[0]==-1)
    z=np.abs((x[0]-means)/stds)
    ranked=np.argsort(z)[::-1]
    deviations=[
        f'{FEATURE_NAMES[i]} ({z[i]:.1f}σ from normal reference)'
        for i in ranked[:3] if z[i]>=1.5
    ]
    return {
        'model':MODEL_NAME,
        'anomaly_score':round(percentile,1),
        'outlier':outlier,
        'raw_abnormality':round(abnormality,4),
        'top_feature_deviations':deviations,
    }

def ml_risk_adjustment(anomaly_score:float)->int:
    if anomaly_score>=99: return 12
    if anomaly_score>=95: return 8
    if anomaly_score>=85: return 4
    return 0
