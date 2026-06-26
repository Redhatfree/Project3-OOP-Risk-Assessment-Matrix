# -*- coding: utf-8 -*-
"""
Created on Tuesday, June 23, 2026
@author: Rouzbeh
Project 4 - Step 3: Sidebar Controls & Portfolio Filtering
"""
# -*- coding: utf-8 -*-
"""
Created on Friday, June 26, 2026
@author: Rouzbeh
Project 4 - Step 4: Metric Toggles & Chart Visualizations
"""
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Risk & Performance Visualizer", page_icon="📈", layout="wide")

st.title("📈 Portfolio Risk & Performance Visualizer")
st.subheader("Project 4: Interactive Charts & Trend Lines")
st.markdown("Use the sidebar to slice the data and watch the performance charts update instantly.")

# 2. Dataset Setup
raw_data = {
    "Task ID": ["TSK-001", "TSK-002", "TSK-003", "TSK-004"],
    "Infrastructure Project Name": [
        "E6 Highway Tunnel Excavation", 
        "Bridge Foundation Concrete Pour", 
        "Front-End Design Quality Review", 
        "Signaling System Digital Upgrade"
    ],
    "Planned Value ($M)": [5.0, 3.5, 8.0, 2.0],
    "Actual Cost ($M)": [9.5, 3.1, 15.0, 1.8],
    "Earned Value ($M)": [4.0, 3.8, 6.0, 2.0]
}

df = pd.DataFrame(raw_data)

# Calculate Metrics
df["Calculated CPI"] = (df["Earned Value ($M)"] / df["Actual Cost ($M)"]).round(2)
df["Calculated SPI"] = (df["Earned Value ($M)"] / df["Planned Value ($M)"]).round(2)
df["AI Risk Status"] = df.apply(
    lambda row: "🚨 CRITICAL RISK" if row["Calculated CPI"] < 0.9 or row["Calculated SPI"] < 0.9 else "🟢 STABLE PIPELINE", 
    axis=1
)

# 3. Sidebar Controls
st.sidebar.header("🕹️ Control Panel")
status_options = ["All Statuses", "🚨 CRITICAL RISK", "🟢 STABLE PIPELINE"]
selected_status = st.sidebar.selectbox("Filter by Risk Profile:", status_options)

# NEW: Chart Metric Toggle Widget
chart_metric = st.sidebar.radio(
    "Choose Metric to Visualize:",
    ["Calculated CPI", "Calculated SPI"]
)

# Apply Data Filter
filtered_df = df.copy()
if selected_status != "All Statuses":
    filtered_df = filtered_df[filtered_df["AI Risk Status"] == selected_status]

# 4. Interface Columns
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown(f"### 📋 Filtered Data Grid")
    if filtered_df.empty:
        st.warning("⚠️ No projects match criteria.")
    else:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with c2:
    st.markdown(f"### 📊 Portfolio {chart_metric[-3:]} Comparison")
    if filtered_df.empty:
        st.info("Adjust filters to generate visual chart.")
    else:
        # Create a clean bar chart mapping projects to selected metric
        chart_data = filtered_df.set_index("Infrastructure Project Name")[[chart_metric]]
        st.bar_chart(chart_data)
        
        # Draw a baseline performance threshold line at 1.0
        st.caption("💡 Note: A value below 1.0 indicates a project is over budget (CPI) or behind schedule (SPI).")