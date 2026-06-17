import streamlit as st

st.title("🖥 Hadoop Cluster Health")

c1,c2,c3,c4 = st.columns(4)

c1.metric("DataNodes","2")
c2.metric("NodeManagers","2")
c3.metric("HDFS Capacity","47.9 GB")
c4.metric("DFS Used","58 MB")

st.success(
    "Cluster operating normally."
)
