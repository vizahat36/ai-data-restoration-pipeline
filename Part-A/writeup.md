# Part A Writeup: Data Cleaning and Quality Analysis

## Assumptions During Cleaning

While building the cleaning pipeline, I made a few explicit assumptions so that the final dataset is suitable for model training and analysis.

1. A valid conversation must contain at least two turns.
2. Every turn must have non-empty text after trimming whitespace.
3. Consecutive duplicate turns with the same role and same text are considered noise.
4. Metadata is mandatory and must include `call_duration_seconds` and `outcome`.
5. `call_duration_seconds` must be numeric and strictly greater than zero.
6. `outcome` must be one of the expected labels: payment_committed, callback_scheduled, escalated, or no_resolution.
7. Garbled text patterns (for example mojibake-like strings) indicate data corruption and are rejected.
8. Language labels are expected to match text content at a heuristic level; strong mismatch is rejected.

These assumptions prioritize training readiness and label consistency over maximizing data retention.

## Hardest Issue to Detect

The hardest issue to detect programmatically was language mismatch across Hindi, Hinglish, and English.

This is difficult because real call-center text is naturally mixed. A single conversation can contain English payment terms, Hinglish transliteration, and occasional Devanagari text. So a strict rule would create many false positives.

To handle this, I used a lightweight heuristic strategy:

1. Character script checks (Devanagari vs Latin).
2. Simple keyword signals for Hinglish and English.
3. A final mismatch check between predicted language and provided label.

This approach is intentionally simple and explainable for the assignment. In production, I would replace it with a stronger language ID model and confidence thresholds.

## Scaling to 100,000 Conversations

If this pipeline were scaled from 100 to 100,000 conversations, I would make the following changes:

1. Stream processing instead of full in-memory loading, by reading and validating line-by-line.
2. Batch and parallel validation for CPU-bound checks (for example multiprocessing or distributed workers).
3. Structured logging and metrics export (rejection rate by reason, language drift, metadata error trends).
4. Better fault tolerance (bad-line quarantine, retry queues, and audit files for parsing failures).
5. More robust language and corruption detection using specialized libraries or compact classifiers.

These changes keep memory usage stable, improve throughput, and make quality monitoring reliable at scale.

## Additional Quality Checks and Initiative

Beyond mandatory checks, I added quality reporting signals that are useful for ML operations:

1. Rejection reason percentages (not just counts).
2. Language distribution before and after cleaning.
3. Outcome distribution before and after cleaning.
4. Average turns per conversation before and after cleaning.
5. Maximum turns, median turns, and average call duration.

These metrics help detect hidden skew after cleaning, surface unusual conversation lengths, and provide better visibility for downstream model training decisions.
