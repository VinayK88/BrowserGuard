# ML Design Notes

## Why unsupervised anomaly detection?

Enterprise browser telemetry is often label-sparse: most extension activity is benign, confirmed malicious examples are rare, and extension behavior can change after updates. BrowserGuard therefore uses Isolation Forest as a behavioral anomaly layer instead of pretending the synthetic fixtures form a realistic supervised training set.

## Normal-reference corpus

The corpus is deterministic and generated with `random_state=41`. It represents low-to-moderate permission sensitivity, mostly stable publishers/update channels, low rates of session/cookie access, limited OAuth bridging, and event volumes close to baseline.

The corpus is intentionally part of the project implementation rather than presented as real enterprise data.

## Features

`browserguard/features.py` is the single source of truth for feature extraction. Continuous reach variables are log transformed to reduce domination by large extension age, user counts, or event ratios.

## Model output

`browserguard/ml.py` exposes:

- `anomaly_score`: normal-reference percentile, 0–100;
- `outlier`: Isolation Forest's inlier/outlier decision;
- `raw_abnormality`: internal model margin for debugging;
- `top_feature_deviations`: largest standardized deviations from the reference corpus.

The final `risk_score` is:

```text
hybrid risk = min(100, rule_score + bounded_ml_adjustment)
```

This keeps policy reasoning inspectable and makes the ML contribution explicit.

## What this project does not claim

- No model was trained on private Chrome/Edge/Firefox/Safari telemetry.
- The synthetic baseline is not a production benchmark.
- The anomaly percentile is not a probability of maliciousness.
- Standardized feature deviations are not SHAP values or causal explanations.
