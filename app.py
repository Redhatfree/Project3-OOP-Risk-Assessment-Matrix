

# -*- coding: utf-8 -*-
"""
Created on Wednesday, July 1, 2026
@author: Rouzbeh
Project 4 - Step 6: Memory Pipelines & CSV Export Engines
"""
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Risk Export Center", page_icon="💾", layout="wide")

st.title("💾 Enterprise Risk Center & Export Pipeline")
st.subheader("Project 4: In-Memory Data Compilation")
st.markdown("Slice your dataset using the control panel, then export the live filtered subset instantly to a CSV spreadsheet.")

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

budget_range = st.sidebar.slider(
    "Select Planned Value Budget Range ($M):",
    min_value=1.0,
    max_value=10.0,
    value=(1.0, 10.0),
    step=0.5
)

# Apply Filters
filtered_df = df.copy()
if selected_status != "All Statuses":
    filtered_df = filtered_df[filtered_df["AI Risk Status"] == selected_status]

filtered_df = filtered_df[
    (filtered_df["Planned Value ($M)"] >= budget_range[0]) & 
    (filtered_df["Planned Value ($M)"] <= budget_range[1])
]

# 4. Interface Columns
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown(f"### 📋 Filtered Data Grid")
    if filtered_df.empty:
        st.warning("⚠️ No projects match criteria.")
    else:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        
        st.divider()
        # ==========================================
        # NEW: IN-MEMORY CSV COMPILATION ENGINE
        # ==========================================
        # Convert the dynamic dataframe into a standard comma-separated text string string
        csv_buffer = filtered_df.to_csv(index=False).encode('utf-8')
        
        # Draw a physical file download button interface
        st.download_button(
            label="📥 Download Filtered Backlog as CSV",
            data=csv_buffer,
            file_name="filtered_portfolio_risk_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        # ==========================================

with c2:
    st.markdown(f"### 📊 Portfolio {chart_metric[-3:]} Comparison")
    if filtered_df.empty:
        st.info("Adjust filters to generate visual chart.")
    else:
        chart_data = filtered_df.set_index("Infrastructure Project Name")[[chart_metric]]
        st.bar_chart(chart_data)
        
        critical_count = int((filtered_df["AI Risk Status"] == "🚨 CRITICAL RISK").sum())
        if critical_count > 0:
            st.error(f"⚠️ Action Required: There are {critical_count} critical project bottlenecks visible in this view.")
        else:
            st.success("✅ Clean Slate: All current filtered projects are operating efficiently within normal bounds.")