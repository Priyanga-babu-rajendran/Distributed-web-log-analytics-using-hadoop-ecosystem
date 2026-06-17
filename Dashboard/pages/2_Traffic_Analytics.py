import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📈 Traffic Analytics")

hour_df = pd.read_csv(
    "hourly.txt",
    sep="\t",
    names=["Hour","Count"]
)

fig = px.line(
    hour_df,
    x="Hour",
    y="Count",
    markers=True,
    title="Hourly Traffic Pattern"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

peak = hour_df.loc[
    hour_df["Count"].idxmax()
]

st.info(
    f"🔥 Peak Traffic Hour: {peak['Hour']} ({peak['Count']} requests)"
)
