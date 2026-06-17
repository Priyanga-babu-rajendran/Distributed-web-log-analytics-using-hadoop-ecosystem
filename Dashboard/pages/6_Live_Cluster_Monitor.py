import streamlit as st
import subprocess
import re
import pandas as pd

st.set_page_config(page_title="Live Cluster Monitor", layout="wide")

st.title("🖥️ Live Hadoop Cluster Monitor")

# -----------------------------
# HDFS Metrics
# -----------------------------

def get_hdfs_report():
    try:
        return subprocess.check_output(
            ["hdfs", "dfsadmin", "-report"],
            text=True
        )
    except Exception as e:
        return str(e)

report = get_hdfs_report()

# Capacity
capacity_match = re.search(
    r"Configured Capacity:\s+\d+\s+\((.*?)\)",
    report
)

# Used
used_match = re.search(
    r"DFS Used:\s+\d+\s+\((.*?)\)",
    report
)

# DataNodes
datanodes = len(re.findall(r"Hostname:", report))

capacity = (
    capacity_match.group(1)
    if capacity_match else "N/A"
)

dfs_used = (
    used_match.group(1)
    if used_match else "N/A"
)

# -----------------------------
# YARN Metrics
# -----------------------------

try:
    yarn_output = subprocess.check_output(
        ["yarn", "node", "-list"],
        text=True
    )

    nodemanagers = len(
        [x for x in yarn_output.splitlines()
         if "RUNNING" in x]
    )

except:
    nodemanagers = "N/A"

# -----------------------------
# Metrics Row
# -----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Active DataNodes",
    datanodes
)

c2.metric(
    "NodeManagers",
    nodemanagers
)

c3.metric(
    "HDFS Capacity",
    capacity
)

c4.metric(
    "DFS Used",
    dfs_used
)

st.divider()

# -----------------------------
# Raw HDFS Report
# -----------------------------

st.subheader("📊 HDFS Cluster Report")

st.text(report)

# -----------------------------
# Raw YARN Report
# -----------------------------

st.subheader("⚙️ YARN Node Report")

try:
    yarn_report = subprocess.check_output(
        ["yarn", "node", "-list"],
        text=True
    )

    st.text(yarn_report)

except Exception as e:
    st.error(str(e))
