from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
BASE_DIR=Path(__file__).resolve().parent.parent

st.title("🌐 HTTP Analytics")

status_df = pd.read_csv(
    f"{BASE_DIR}/status.txt",
    sep="\t",
    names=["Status","Count"]
)
status_df["Status"]=status_df["Status"].astype(str)
fig = px.pie(
    status_df,
    names="Status",
    values="Count",
    title="HTTP Status Code Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

success = status_df[
    status_df["Status"].astype(str).str.startswith("2")
]["Count"].sum()

redirect = status_df[
    status_df["Status"].astype(str).str.startswith("3")
]["Count"].sum()

client_error = status_df[
    status_df["Status"].astype(str).str.startswith("4")
]["Count"].sum()

server_error = status_df[
    status_df["Status"].astype(str).str.startswith("5")
]["Count"].sum()

quality_df = pd.DataFrame({
    "Type":[
        "Success",
        "Redirect",
        "Client Error",
        "Server Error"
    ],
    "Count":[
        success,
        redirect,
        client_error,
        server_error
    ]
})

fig = px.pie(
    quality_df,
    values="Count",
    names="Type",
    title="Traffic Quality Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
