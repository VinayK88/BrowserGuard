# Methodology

BrowserGuard uses a **hybrid security decision model**:

1. deterministic posture / policy scoring;
2. an unsupervised Isolation Forest behavior-anomaly model;
3. browser-to-SaaS blast-radius features;
4. a bounded ML adjustment applied to the transparent rule score.

The rule layer combines permission sensitivity, publisher trust, permission drift, update-channel state, session/cookie exposure, external posting, OAuth/SaaS reach, AI-context handling, event-volume deviation, and user reach.

## ML layer

The Isolation Forest is trained on **800 deterministic synthetic normal-reference extension profiles** using a fixed random seed. It receives 14 features:

- permission sensitivity
- permission count
- permission delta
- publisher verification state
- update-channel risk
- extension age
- active-user reach
- session access
- cookie access
- AI-assistant context
- external posting
- OAuth/SaaS bridge state
- event-volume ratio
- downstream resource count

`ml_anomaly_score` is the percentile of a candidate extension's Isolation Forest abnormality relative to the synthetic normal-reference corpus. It is **not a probability of compromise**.

The ML adjustment is deliberately bounded:

| Normal-reference anomaly percentile | Added risk |
| --- | ---: |
| `< 85` | `+0` |
| `85–94.9` | `+4` |
| `95–98.9` | `+8` |
| `>= 99` | `+12` |

This means ML can increase investigation priority but cannot erase or replace explicit policy evidence.

## Explainability

Isolation Forest does not provide additive feature attribution by default. BrowserGuard therefore reports the largest standardized feature deviations from the normal-reference corpus as **diagnostic context**, not causal attribution.

## Evaluation boundary

All fixtures and training profiles are synthetic. The baseline validates implementation behavior, reproducibility, and expected decision logic. It does not establish real-world detection accuracy, false-positive rate, or compromise probability.

A production implementation should train and validate against authorized managed-browser telemetry, extension inventory/change history, identity context, network destinations, SaaS access, analyst dispositions, and time-based holdouts.
