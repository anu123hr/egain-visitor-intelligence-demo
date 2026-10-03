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

The prototype uses this pipeline:

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

That is three backticks.

### Step 3: save

Press:

```
Control + O

Data Processing
Log Cleaning
The raw weblogs contain both human and automated traffic.
The cleaning step removes obvious non-human activity such as:
- bots
- crawlers
- scraping tools
- monitoring traffic
- preview agents
- suspiciously high-volume IP behavior
The prototype intentionally favors precision over completeness.
Sessionization
Requests are grouped into sessions using a 30-minute inactivity window.
For every session, the pipeline calculates:
- session start
- session end
- pageviews
- unique pages
- intent score
- high-intent visits
- product visits
- customer-proof visits
- primary topic of interest
Intent Scoring
Each page is categorized and assigned an intent weight.
Page Category	Intent Points
High Intent / Contact	10
Product	5
Customer Proof	4
Research	2
Other	0
Investor	0
Careers	0
Noise	0


The scoring model is intentionally simple and explainable.
The goal is to prioritize commercial behavior rather than raw traffic volume.
Topic Classification
Pages are also mapped to broad topics such as:
- AI Knowledge
- Knowledge Management
- Customer Success
- Products
- Thought Leadership
- Commercial Intent
This gives the sales rep context on what an account appears to be researching.
IP and Account Enrichment
Visitor IP addresses are enriched using IPinfo network metadata.
The enrichment adds fields such as:
- ASN
- network/company name
- domain
- country
The prototype also applies basic heuristics to separate:
- hosting/cloud providers
- consumer ISPs
- potential enterprise networks
Enterprise candidates are then aggregated into account-level records.
Account Prioritization
The application ranks accounts using behavioral signals such as:
- total intent score
- high-intent visits
- product-page visits
- customer-proof visits
- number of sessions
- number of unique visitor IPs
- total pageviews
This allows a rep to move from hundreds of thousands of raw web requests to a short list of accounts worth reviewing.
Sales Rep Experience
Prioritized Accounts
The main view lets a sales rep:
- search by account or domain
- filter by minimum intent score
- filter by minimum session count
- filter by country
- compare account-level activity
Account Detail
For each selected account, the rep can see:
- intent score
- sessions
- unique visitor IPs
- pageviews
- top topic
- high-intent visits
- product visits
- customer-proof visits
- first seen
- last seen
- recent sessions
- exact pages visited
- referral URLs
Why This Account Matters
The prototype converts behavioral metrics into a simple rep-facing explanation.
Example:
Zscaler shows meaningful buying activity with multiple high-intent visits, product-page visits, and repeat sessions.

This is intended to help the rep understand the signal without interpreting raw logs.
Privacy
The public deployment does not expose raw visitor IP addresses.
IP addresses are hashed before being included in the demo repository.
Company names and domains are retained so the sales workflow can be demonstrated realistically.
No API keys, access tokens, .env files, or raw IP addresses are included in the public repository.
Important Limitations
IP-to-company attribution is probabilistic
An IP or ASN owner is not always the visitor's employer.
Traffic can originate through:
- VPNs
- corporate proxies
- security vendors
- shared networks
- ISPs
- cloud infrastructure
For example, a network may belong to Zscaler or an ISP even though the end visitor works for another organization.
A production implementation should therefore include an attribution-confidence score.
Intent scoring is heuristic
The current intent model is manually defined.
A production system could improve the weights using historical outcomes such as:
- meetings booked
- opportunities created
- pipeline progression
- closed-won deals
Topic classification is rule-based
The prototype classifies topics using URL patterns.
A more advanced system could classify pages using:
- page content
- embeddings
- LLM classification
- product taxonomy
IP coverage is limited
The prototype enriches a subset of high-intent IPs rather than every visitor IP.
This keeps the prototype inexpensive and fast, but a production pipeline would enrich and cache a much broader set of visitors.
Production Extensions
With additional time, I would add:
- CRM integration
- account owner mapping
- contact enrichment
- attribution confidence
- intent trend detection
- repeat-visit alerts
- real-time ingestion
- Slack or email alerts
- AI-generated account briefs
- recommended outreach angles
- Salesforce opportunity correlation
- multiple IP enrichment providers
Tech Stack
- Python
- Pandas
- Streamlit
- IPinfo
- GitHub
- Streamlit Community Cloud
Repository Structure
app/
    app.py

data/
    accounts.csv
    sessions.csv
    enriched_ips.csv
    clean_logs.csv

requirements.txt
README.md

Running Locally
Install dependencies:
pip install -r requirements.txt

Start the application:
streamlit run app/app.py

Demo Notes
The public demo uses processed data.
Raw visitor IP addresses are not included.
The purpose of the prototype is to demonstrate how eGain website activity can be transformed from raw weblogs into account-level sales intelligence that a rep can search, prioritize, and act on.
