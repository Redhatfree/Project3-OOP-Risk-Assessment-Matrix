

# -*- coding: utf-8 -*-
"""
Created on Tuesday, June 30, 2026
@author: Rouzbeh
Project 4 - Step 5: Range Sliders & Styled Conditional Alerts
"""
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Strategic Risk Matrix", page_icon="🎛️", layout="wide")

st.title("🎛️ Strategic Risk Matrix & Range Filtering")
st.subheader("Project 4: Multi-Dimensional Input Slicing")
st.markdown("Use the control panel below to fine-tune your financial performance thresholds and visualize risk impact.")

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

chart_metric = st.sidebar.radio(
    "Choose Metric to Visualize:",
    ["Calculated CPI", "Calculated SPI"]
)

# NEW: Numeric Range Filter Slider
budget_range = st.sidebar.slider(
    "Select Planned Value Budget Range ($M):",
    min_value=1.0,
    max_value=10.0,
    value=(1.0, 10.0),  # Tuple indicates a two-sided range slider
    step=0.5
)

# Apply Data Filters (Status + Budget Range)
filtered_df = df.copy()
if selected_status != "All Statuses":
    filtered_df = filtered_df[filtered_df["AI Risk Status"] == selected_status]

# Filtering rows that fall WITHIN the chosen range slider min/max boundaries
filtered_df = filtered_df[
    (filtered_df["Planned Value ($M)"] >= budget_range[0]) & 
    (filtered_df["Planned Value ($M)"] <= budget_range[1])
]

# 4. Interface Columns
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown(f"### 📋 Filtered Data Grid")
    if filtered_df.empty:
        st.warning("⚠️ No projects match criteria. Adjust sliders.")
    else:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with c2:
    st.markdown(f"### 📊 Portfolio {chart_metric[-3:]} Comparison")
    if filtered_df.empty:
        st.info("Adjust filters to generate visual chart.")
    else:
        chart_data = filtered_df.set_index("Infrastructure Project Name")[[chart_metric]]
        st.bar_chart(chart_data)
        
        # NEW: Conditional Status Warning Display Box
        critical_count = int((filtered_df["AI Risk Status"] == "🚨 CRITICAL RISK").sum())
        if critical_count > 0:
            st.error(f"⚠️ Action Required: There are {critical_count} critical project bottlenecks visible in this view.")
        else:
            st.success("✅ Clean Slate: All current filtered projects are operating efficiently within normal bounds.")