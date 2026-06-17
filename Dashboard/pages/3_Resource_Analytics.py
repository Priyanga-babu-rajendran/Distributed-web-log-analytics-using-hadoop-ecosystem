import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📄 Resource Analytics")

page_df = pd.read_csv(
    "pages.txt",
    sep="\t",
    names=["Page","Count"]
)

fig = px.bar(
    page_df.sort_values(
        "Count",
        ascending=False
    ).head(10),
    x="Count",
    y="Page",
    orientation="h",
    title="Top Resources"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
