\# Kubernetes Portability Scoring Engine



\## Purpose

A Python prototype that calculates portability scores for Kubernetes migration experiments.



\## Files

\- `scoring\_engine.py`: Calculates portability scores.

\- `migration\_metrics.json`: Contains sample migration data for testing.



\## Metrics

The scoring engine considers:

\- Percentage of YAML changes

\- Number of manual rewrites

\- Migration time

\- Failed deployments

\- Provider-specific dependencies



\## Scoring Method

The program normalizes each metric against a configured limit and combines the results using provisional weights.



A higher score indicates lower measured migration effort under this model.



\## Limitations

\- The scoring weights and limits are provisional and need team review.

\- The included measurements are sample data, not real experimental results.

\- Actual migration measurements must be collected before reporting final findings.

\## Current metrics format

`migration_metrics.json` stores migration duration in hours. The scoring engine
normalizes that field against a 48-hour limit. Older records using
`migration_time_minutes` remain supported with the existing 120-minute limit.
Values outside a metric's range are rejected for that record; other records
are still reported.

An optional `portability_score_percent` is displayed as a stored value. It is
not used to calculate the formula-based score, so the two scores may differ.

## Migration decision engine

Run `python decision_engine.py` in this directory, or choose option 5 from the
project's main menu. Select a source and a different destination from AWS EKS,
Google GKE, Azure AKS, and Kubeadm. The metrics file contains all 12 directed
migration pairs; self-migrations are not offered. The engine uses the
formula-calculated portability score and `provider_dependencies` to make a
deterministic recommendation:

- Recommend staying with the current service when the score is below 20%, or
  provider dependencies exceed 7 out of 10.
- Otherwise, recommend migration and print a work estimate and a migration
  checklist.

The included pair metrics are illustrative planning inputs, not verified
measurements. The provider-dependency metric is a provisional 0-10 estimate,
calibrated below the high-lock-in cutoff for these examples; it is not a
literal count of configuration entries. Replace these example values with
measurements from your own migration experiments before using the
recommendation operationally.

The estimate treats the migration time as hands-on person-hours and
assumes 6 productive hours per engineer per workday. Team size is estimated at
one engineer per 5 person-days, up to 3 engineers. These are planning
assumptions, not measured staffing data; update them when project-specific
effort and team-capacity measurements are available.

Run the unit tests with `python -m unittest discover -s portability-scoring`.


\## Next Steps

1\. Agree on the scoring formula with the team.

2\. Collect real migration measurements.

3\. Validate the scores.

4\. Prepare charts and identify high-friction components.
