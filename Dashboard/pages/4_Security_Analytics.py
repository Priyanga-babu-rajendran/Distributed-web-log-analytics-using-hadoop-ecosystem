import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🛡 Security Analytics")

ip_df = pd.read_csv(
    "ips.txt",
    sep="\t",
    names=["IP","Count"]
)

top = ip_df.sort_values(
    "Count",
    ascending=False
).head(10)

fig = px.bar(
    top,
    x="Count",
    y="IP",
    orientation="h",
    title="Most Active Clients"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.warning(
    "High-frequency IPs may indicate crawler or bot activity."
)
