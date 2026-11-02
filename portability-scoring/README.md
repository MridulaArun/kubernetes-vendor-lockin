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


\## Next Steps

1\. Agree on the scoring formula with the team.

2\. Collect real migration measurements.

3\. Validate the scores.

4\. Prepare charts and identify high-friction components.
