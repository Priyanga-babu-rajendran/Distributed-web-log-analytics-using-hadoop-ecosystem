# Dashboard User Guide

## Overview

The Streamlit dashboard visualizes insights generated from Hadoop MapReduce and Apache Spark analytics.

## Launching the Dashboard

```bash
cd Dashboard
streamlit run dashboard.py
```

Open:

```text
http://localhost:8501
```

## Dashboard Modules

- **Home Dashboard** – Project summary and key metrics
- **HTTP Analytics** – Status code and traffic analysis
- **Traffic Analytics** – Request trends and client activity
- **Resource Analytics** – Most accessed resources
- **Security Analytics** – Suspicious activity monitoring
- **Cluster Health** – HDFS and YARN status
- **Live Cluster Monitor** – Real-time cluster information

## Technology Stack

- HDFS
- YARN
- MapReduce
- Apache Spark
- Streamlit
- Plotly
