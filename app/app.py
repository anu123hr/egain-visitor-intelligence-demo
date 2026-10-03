from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

st.set_page_config(
    page_title="eGain Visitor Intelligence",
    layout="wide"
)

st.title("eGain Visitor Intelligence")
st.write(
    "Prioritized accounts based on website behavior and buying-intent signals."
)

# -----------------------------
# Load data
# -----------------------------

accounts = pd.read_csv(DATA_DIR / "accounts.csv")

sessions = pd.read_csv(
    DATA_DIR / "sessions.csv",
    parse_dates=["session_start", "session_end"]
)

enriched_ips = pd.read_csv(DATA_DIR / "enriched_ips.csv")

clean_logs = pd.read_csv(
    DATA_DIR / "clean_logs.csv",
    parse_dates=["Date & Time (UTC)"]
)

# -----------------------------
# Filters
# -----------------------------

st.subheader("Account Prioritization")

search_term = st.text_input(
    "Search account or domain",
    placeholder="Example: AT&T, bluecrossma.com, zscaler.com"
)

filter1, filter2, filter3 = st.columns(3)

with filter1:
    min_intent = st.number_input(
        "Minimum Intent Score",
        min_value=0,
        value=0,
        step=10
    )

with filter2:
    min_sessions = st.number_input(
        "Minimum Sessions",
        min_value=0,
        value=0,
        step=1
    )

with filter3:
    country_options = ["All"] + sorted(
        accounts["countries"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_country = st.selectbox(
        "Country",
        country_options
    )

filtered_accounts = accounts.copy()

if search_term:
    search_mask = (
        filtered_accounts["as_name"]
        .fillna("")
        .str.contains(search_term, case=False, regex=False)
        |
        filtered_accounts["as_domain"]
        .fillna("")
        .str.contains(search_term, case=False, regex=False)
    )

    filtered_accounts = filtered_accounts[search_mask]

filtered_accounts = filtered_accounts[
    filtered_accounts["total_intent"] >= min_intent
]

filtered_accounts = filtered_accounts[
    filtered_accounts["sessions"] >= min_sessions
]

if selected_country != "All":
    filtered_accounts = filtered_accounts[
        filtered_accounts["countries"].fillna("").str.contains(
            selected_country,
            case=False,
            regex=False
        )
    ]

# -----------------------------
# Summary metrics
# -----------------------------

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Accounts",
    len(filtered_accounts)
)

metric2.metric(
    "Total Sessions",
    int(filtered_accounts["sessions"].sum())
)

metric3.metric(
    "High-Intent Visits",
    int(filtered_accounts["high_intent_visits"].sum())
)

# -----------------------------
# Prioritized accounts table
# -----------------------------

st.subheader("Prioritized Accounts")

account_table = filtered_accounts[
    [
        "as_name",
        "as_domain",
        "countries",
        "unique_ips",
        "sessions",
        "total_pageviews",
        "top_topic",
        "total_intent",
        "high_intent_visits",
        "product_visits",
        "customer_proof_visits"
    ]
].copy()

account_table = account_table.rename(
    columns={
        "as_name": "Account",
        "as_domain": "Domain",
        "countries": "Countries",
        "unique_ips": "Unique IPs",
        "sessions": "Sessions",
        "total_pageviews": "Pageviews",
        "top_topic": "Top Interest",
        "total_intent": "Intent Score",
        "high_intent_visits": "High Intent",
        "product_visits": "Product",
        "customer_proof_visits": "Customer Proof"
    }
)

st.dataframe(
    account_table,
    width="stretch",
    hide_index=True
)

# -----------------------------
# Account detail
# -----------------------------

st.subheader("Account Detail")

account_names = (
    filtered_accounts["as_name"]
    .dropna()
    .unique()
    .tolist()
)

if account_names:

    selected_account = st.selectbox(
        "Select an account",
        account_names
    )

    account_row = filtered_accounts[
        filtered_accounts["as_name"] == selected_account
    ].iloc[0]

    # -----------------------------
    # Account IPs and raw activity
    # -----------------------------

    account_ips = enriched_ips[
        enriched_ips["as_name"] == selected_account
    ]["ip"].tolist()

    account_sessions = sessions[
        sessions["ip"].isin(account_ips)
    ].copy()

    account_logs = clean_logs[
        clean_logs["IP"].isin(account_ips)
    ].copy()

    # -----------------------------
    # Account metrics
    # -----------------------------

    detail1, detail2, detail3, detail4 = st.columns(4)

    detail1.metric(
        "Intent Score",
        int(account_row["total_intent"])
    )

    detail2.metric(
        "Sessions",
        int(account_row["sessions"])
    )

    detail3.metric(
        "Unique IPs",
        int(account_row["unique_ips"])
    )

    detail4.metric(
        "Pageviews",
        int(account_row["total_pageviews"])
    )

    # -----------------------------
    # Why this account matters
    # -----------------------------

    st.write("### Why This Account Matters")

    st.write(
        f"**Top Interest:** {account_row['top_topic']}"
    )

    topic_counts = (
        account_logs["Topic"]
        .value_counts()
        .head(3)
    )

    if not topic_counts.empty:

        st.write("**Top Topics:**")

        for topic, count in topic_counts.items():
            st.write(
                f"- {topic}: {count} pageviews"
            )

    summary_parts = []

    if account_row["high_intent_visits"] > 0:
        summary_parts.append(
            f"{int(account_row['high_intent_visits'])} high-intent visits"
        )

    if account_row["product_visits"] > 0:
        summary_parts.append(
            f"{int(account_row['product_visits'])} product-page visits"
        )

    if account_row["customer_proof_visits"] > 0:
        summary_parts.append(
            f"{int(account_row['customer_proof_visits'])} customer-proof visits"
        )

    if account_row["unique_ips"] > 1:
        summary_parts.append(
            f"{int(account_row['unique_ips'])} distinct visitor IPs"
        )

    if summary_parts:

        summary_text = ", ".join(summary_parts)

        st.info(
            f"{selected_account} shows meaningful buying activity with "
            f"{summary_text}. "
            f"The account generated "
            f"{int(account_row['sessions'])} sessions across "
            f"{int(account_row['total_pageviews'])} pageviews."
        )

    else:

        st.info(
            f"{selected_account} has website activity, "
            f"but no strong buying-intent signals were detected."
        )

    # -----------------------------
    # Buying signals
    # -----------------------------

    st.write("### Buying Signals")

    st.write(
        f"""
        - High-intent visits: **{int(account_row["high_intent_visits"])}**
        - Product visits: **{int(account_row["product_visits"])}**
        - Customer-proof visits: **{int(account_row["customer_proof_visits"])}**
        - First seen: **{account_row["first_seen"]}**
        - Last seen: **{account_row["last_seen"]}**
        """
    )

    # -----------------------------
    # Account information
    # -----------------------------

    st.write("### Account Information")

    st.write(
        f"""
        **Domain:** {account_row["as_domain"]}  
        **Countries:** {account_row["countries"]}  
        **Network Type:** {account_row["network_type"]}
        """
    )

    # -----------------------------
    # Recent sessions
    # -----------------------------

    st.write("### Recent Activity")

    account_sessions = account_sessions.sort_values(
        "session_start",
        ascending=False
    )

    recent_activity = account_sessions[
        [
            "session_start",
            "session_end",
            "pageviews",
            "unique_pages",
            "top_topic",
            "intent_score",
            "high_intent_visits",
            "product_visits",
            "customer_proof_visits"
        ]
    ].head(20)

    st.dataframe(
        recent_activity,
        width="stretch",
        hide_index=True
    )

    # -----------------------------
    # Pages visited
    # -----------------------------

    st.write("### Pages Visited")

    account_logs = account_logs.sort_values(
        "Date & Time (UTC)",
        ascending=False
    )

    page_activity = account_logs[
        [
            "Date & Time (UTC)",
            "Page URL",
            "Page Category",
            "Topic",
            "Intent Points",
            "Referral URL"
        ]
    ].head(50)

    st.dataframe(
        page_activity,
        width="stretch",
        hide_index=True
    )

else:

    st.info(
        "No accounts match the current filters."
    )
