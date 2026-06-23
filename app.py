# -*- coding: utf-8 -*-
"""
Created on Tuesday, June 23, 2026
@author: Rouzbeh
Project 4 - Step 3: Sidebar Controls & Portfolio Filtering
"""
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Advanced Portfolio Filters", page_icon="🎛️", layout="wide")

st.title("🎛️ Dynamic Portfolio Filter Suite")
st.subheader("Project 4: Interactive Inputs & Data Slicing")
st.markdown("Use the controls on the left sidebar to slice and filter your project risk matrix in real-time.")

# 2. Hardcoded Dataset
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

# Calculate Core Metrics
df["Calculated CPI"] = (df["Earned Value ($M)"] / df["Actual Cost ($M)"]).round(2)
df["Calculated SPI"] = (df["Earned Value ($M)"] / df["Planned Value ($M)"]).round(2)
df["AI Risk Status"] = df.apply(
    lambda row: "🚨 CRITICAL RISK" if row["Calculated CPI"] < 0.9 or row["Calculated SPI"] < 0.9 else "🟢 STABLE PIPELINE", 
    axis=1
)

# ==========================================
# 3. SIDEBAR CONTROLS (Today's Addition)
# ==========================================
st.sidebar.header("🕹️ Control Panel")

# Filter 1: Dropdown selector for Risk Status
status_options = ["All Statuses", "🚨 CRITICAL RISK", "🟢 STABLE PIPELINE"]
selected_status = st.sidebar.selectbox("Filter by Risk Profile:", status_options)

# Filter 2: Slider for Minimum Budget (Planned Value)
min_budget = st.sidebar.slider(
    "Minimum Planned Value Budget ($M):", 
    min_value=1.0, 
    max_value=10.0, 
    value=1.0, 
    step=0.5
)

# Apply Sidebar Filters to the Dataframe
filtered_df = df[df["Planned Value ($M)"] >= min_budget]

if selected_status != "All Statuses":
    filtered_df = filtered_df[filtered_df["AI Risk Status"] == selected_status]

# ==========================================

# 4. Display Summary KPIs for FILTERED data
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.metric("Filtered Portfolio Budget", f"${filtered_df['Planned Value ($M)'].sum():.1f} Million")
with c2:
    critical_count = int((filtered_df["AI Risk Status"] == "🚨 CRITICAL RISK").sum())
    st.metric("Visible Critical Risks", f"{critical_count} Tasks")

st.divider()

# 5. Render the Filtered Grid
if filtered_df.empty:
    st.warning("⚠️ No projects match your active sidebar filter criteria! Adjust the controls to see data.")
else:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)