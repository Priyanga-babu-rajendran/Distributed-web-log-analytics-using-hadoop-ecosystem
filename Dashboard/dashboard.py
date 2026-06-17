import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NASA Distributed Web Analytics Platform",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 NASA Distributed Web Analytics Platform")

st.caption(
    "Powered by HDFS • MapReduce • Apache Spark • Streamlit"
)

st.markdown("""
### Architecture

NASA Logs → HDFS → MapReduce → Spark Analytics → Dashboard
""")

status_df = pd.read_csv(
    "status.txt",
    sep="\t",
    names=["Status","Count"]
)

ip_df = pd.read_csv(
    "ips.txt",
    sep="\t",
    names=["IP","Count"]
)

hour_df = pd.read_csv(
    "hourly.txt",
    sep="\t",
    names=["Hour","Count"]
)

total_requests = int(status_df["Count"].sum())
unique_ips = len(ip_df)

success = status_df[
    status_df["Status"].astype(str).str.startswith("2")
]["Count"].sum()

client_error = status_df[
    status_df["Status"].astype(str).str.startswith("4")
]["Count"].sum()

server_error = status_df[
    status_df["Status"].astype(str).str.startswith("5")
]["Count"].sum()

success_rate = round(
    success * 100 / total_requests,
    2
)

error_rate = round(
    (client_error + server_error)
    * 100 / total_requests,
    2
)

peak = hour_df.loc[
    hour_df["Count"].idxmax()
]

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Requests", total_requests)
c2.metric("Unique IPs", unique_ips)
c3.metric("Success %", success_rate)
c4.metric("Error %", error_rate)
c5.metric("Peak Hour", str(peak["Hour"]))

st.markdown("---")

st.subheader("Analytics Modules")

col1,col2,col3 = st.columns(3)

with col1:
    st.page_link(
        "pages/1_HTTP_Analytics.py",
        label="🌐 HTTP Analytics"
    )

with col2:
    st.page_link(
        "pages/2_Traffic_Analytics.py",
        label="📈 Traffic Analytics"
    )

with col3:
    st.page_link(
        "pages/3_Resource_Analytics.py",
        label="📄 Resource Analytics"
    )

col4,col5 = st.columns(2)

with col4:
    st.page_link(
        "pages/4_Security_Analytics.py",
        label="🛡 Security Analytics"
    )

with col5:
    st.page_link(
        "pages/5_Cluster_Health.py",
        label="🖥 Cluster Health"
    )

st.success(
    "Distributed Analytics Pipeline Executed Successfully"
)
