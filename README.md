# eGain Visitor Intelligence

A prototype sales intelligence application that transforms anonymous website visitor logs into prioritized account-level insights for sales teams.

## What It Does

The application helps sales reps answer:

- Which companies are showing meaningful interest in eGain?
- Which accounts should I prioritize?
- What products or topics are they researching?
- Are they showing high-intent behavior?
- What pages have they visited recently?

The app provides a searchable list of accounts ranked by intent, along with an account detail view showing recent activity, buying signals, topic interest, and page-level history.

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
```

## Data Processing

### Log Cleaning

The raw weblogs contain both human and automated traffic.

The cleaning process removes obvious non-human activity such as:

- bots
- crawlers
- scraping tools
- monitoring traffic
- preview agents
- suspiciously high-volume IP behavior

The prototype intentionally favors precision over completeness.

### Sessionization

Requests are grouped into sessions using a 30-minute inactivity window.

For each session, the pipeline calculates:

- session start and end time
- pageviews
- unique pages
- intent score
- high-intent visits
- product visits
- customer-proof visits
- primary topic of interest

## Intent Scoring

Each page is categorized and assigned a simple intent weight.

| Page Category | Intent Points |
|---|---:|
| High Intent / Contact | 10 |
| Product | 5 |
| Customer Proof | 4 |
| Research | 2 |
| Other | 0 |
| Investor | 0 |
| Careers | 0 |
| Noise | 0 |

The goal is to prioritize commercially meaningful behavior rather than raw website traffic.

## Topic Classification

Pages are mapped to topics such as:

- AI Knowledge
- Knowledge Management
- Customer Success
- Products
- Thought Leadership
- Commercial Intent

This helps sales reps understand what an account appears to be researching.

## IP and Account Enrichment

Visitor IP addresses are enriched using IPinfo network metadata.

The enrichment adds information such as:

- ASN
- network/company name
- domain
- country

The prototype also applies basic heuristics to distinguish:

- hosting and cloud providers
- consumer ISPs
- potential enterprise networks

Potential enterprise traffic is then aggregated into account-level activity.

## Account Prioritization

Accounts are prioritized using behavioral signals including:

- total intent score
- high-intent visits
- product-page visits
- customer-proof visits
- number of sessions
- number of unique visitor IPs
- total pageviews

This turns hundreds of thousands of raw web requests into a smaller set of accounts a sales rep can investigate.

## Sales Rep Experience

The main application allows a sales rep to:

- search by company or domain
- filter by intent score
- filter by session count
- filter by geography
- compare prioritized accounts

For each account, the rep can see:

- intent score
- sessions
- unique visitor IPs
- pageviews
- top topics
- buying signals
- first and last activity
- recent sessions
- pages visited
- referral URLs

## Why This Account Matters

The prototype converts behavioral metrics into a simple rep-facing explanation.

For example:

> Zscaler shows meaningful buying activity with repeat sessions, product-page visits, and high-intent behavior.

This helps a rep understand the signal without having to interpret raw weblogs.

## Privacy

The public demo does not expose raw visitor IP addresses.

IP addresses are hashed before being included in the public demo repository.

Company names and domains are retained so the sales-rep workflow can be demonstrated realistically.

No API keys, access tokens, `.env` files, or raw IP addresses are included.

## Limitations

### IP-to-company attribution is probabilistic

An IP or ASN owner is not always the visitor's employer.

Traffic may come through:

- VPNs
- corporate proxies
- security vendors
- shared networks
- ISPs
- cloud infrastructure

A production implementation should include an attribution-confidence score and potentially use multiple enrichment providers.

### Intent scoring is heuristic

The current scoring system is intentionally simple and explainable.

A production system could learn better weights using outcomes such as:

- meetings booked
- opportunities created
- pipeline progression
- closed-won deals

### Topic classification is rule-based

The prototype currently classifies topics using URL patterns.

A more advanced system could use:

- page content
- embeddings
- LLM classification
- product taxonomy

### Enrichment coverage is limited

The prototype enriches a subset of high-intent IP addresses rather than every website visitor.

A production pipeline would enrich and cache a broader set of visitors.

## Production Extensions

With additional time, I would add:

- CRM integration
- account owner mapping
- contact enrichment
- attribution confidence scoring
- intent trend detection
- repeat-visit alerts
- real-time ingestion
- Slack or email alerts
- AI-generated account briefs
- recommended outreach angles
- Salesforce opportunity correlation
- multiple enrichment providers

## Tech Stack

- Python
- Pandas
- Streamlit
- IPinfo
- GitHub
- Streamlit Community Cloud

## Repository Structure

```text
app/
    app.py

data/
    accounts.csv
    sessions.csv
    enriched_ips.csv
    clean_logs.csv

requirements.txt
README.md
```

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app/app.py
```

## Demo Notes

The public demo uses processed data and does not expose raw visitor IP addresses.

The purpose of the prototype is to demonstrate how eGain website activity can be transformed from raw weblogs into actionable account intelligence that a sales rep can search, prioritize, and act on.
