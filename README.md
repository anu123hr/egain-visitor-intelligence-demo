# eGain Visitor Intelligence

A prototype sales intelligence application that turns anonymous website visitor logs into prioritized account-level insights for sales teams.

## What it does

The application helps sales reps answer:

- Which companies are showing meaningful interest in eGain?
- Which accounts should I prioritize?
- What products or topics are they researching?
- Are they showing high-intent behavior?
- What pages have they visited recently?

The app provides a searchable list of accounts ranked by intent and an account detail view with recent activity, buying signals, topic interest, and page-level history.

## Architecture

The prototype uses the following pipeline:

```text
Website Logs
    ↓
Bot / Noise Filtering
    ↓
Sessionization
    ↓
Page Classification + Intent Scoring
    ↓
IP / Network Enrichment
    ↓
Account Aggregation
    ↓
Streamlit Sales Intelligence UI
	EOF
