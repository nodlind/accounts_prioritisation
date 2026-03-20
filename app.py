import streamlit as st
import pandas as pd
import altair as alt

from auth import require_auth, logout
from data import load_data, preprocessing
from scoring import add_scorecard, scorecard_config

st.set_page_config(layout="wide")

# 🔐 Auth
require_auth()

st.sidebar.write(f"Logged in as: {st.session_state.username}")

if st.sidebar.button("Logout"):
    logout()

st.title("Account Prioritisation Tool")

# 📥 Load data
df = load_data("account_prioritisation_challenge_data.csv")
df = preprocessing(df)
df = add_scorecard(df, scorecard_config)

# 🎯 Priority score
df["priority_score"] = df["risk_score"] + df["opp_score"]

# 🧭 Filters
st.sidebar.header("Filters")

min_arr = st.sidebar.slider(
    "Minimum ARR (£)",
    int(df["arr_gbp"].min()),
    int(df["arr_gbp"].max()),
    0
)

df = df[df["arr_gbp"] >= min_arr]

# 📊 Scatterplot
st.subheader("Account Prioritisation Map")

risk_mid = df["risk_score"].median()
opp_mid = df["opp_score"].median()

base = alt.Chart(df).mark_circle(opacity=0.7).encode(
    x=alt.X("risk_score:Q", title="Risk Score"),
    y=alt.Y("opp_score:Q", title="Opportunity Score"),
    size=alt.Size("arr_gbp:Q", scale=alt.Scale(range=[50, 1200]), title="ARR (£)"),
    color=alt.Color("priority_score:Q", scale=alt.Scale(scheme="redyellowgreen")),
    tooltip=["account_name", "risk_score", "opp_score", "arr_gbp"]
)

vertical = alt.Chart(pd.DataFrame({'x': [risk_mid]})).mark_rule(strokeDash=[5,5]).encode(x='x:Q')
horizontal = alt.Chart(pd.DataFrame({'y': [opp_mid]})).mark_rule(strokeDash=[5,5]).encode(y='y:Q')

st.altair_chart(base + vertical + horizontal, use_container_width=True)

# 📋 Table
st.subheader("Prioritised Accounts")

df_sorted = df.sort_values(by="priority_score", ascending=False)

st.dataframe(
    df_sorted[[
        "account_name",
        "risk_score",
        "opp_score",
        "priority_score",
        "arr_gbp"
    ]],
    use_container_width=True
)

# 🔍 Drill-down
st.subheader("Account Detail")

selected_account = st.selectbox(
    "Select an account",
    df_sorted["account_name"]
)

account = df_sorted[df_sorted["account_name"] == selected_account].iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric("Risk Score", account["risk_score"])
    st.metric("Opportunity Score", account["opp_score"])

with col2:
    st.metric("ARR (£)", f"{int(account['arr_gbp']):,}")
    st.metric("Priority Score", account["priority_score"])

st.subheader("Why is this account prioritised?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚠️ Risk Drivers")
    for r in account["risk_reasons"]:
        st.write(f"- {r}")

with col2:
    st.markdown("### 🚀 Opportunity Drivers")
    for o in account["opp_reasons"]:
        st.write(f"- {o}")
