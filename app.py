# -*- coding: utf-8 -*-
"""
Created on Thursday, July 2, 2026
@author: Rouzbeh
Project 4 - Step 7: Role-Based Access Controls & Security Toggles
"""
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Secure Risk Terminal", page_icon="🔒", layout="wide")

st.title("🔒 Secure Risk Terminal & Access Control")
st.subheader("Project 4: Enterprise Identity Simulation")
st.markdown("Authenticate your role session in the sidebar panel to unlock restricted infrastructure risk datasets.")

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
    "Earned Value ($M)": [4.0, 3.8, 6.0, 2.0],
    "Restricted Audit Note": [
        "⚠️ Structural variance detected. Subcontractor dispute ongoing.",
        "🟢 Concrete core samples passed safety compression matrix.",
        "🚨 Severe scope creep. Design team understaffed by 40%.",
        "🟢 Migration to new server architecture completed ahead of schedule."
    ]
}

df = pd.DataFrame(raw_data)

# Calculate Metrics
df["Calculated CPI"] = (df["Earned Value ($M)"] / df["Actual Cost ($M)"]).round(2)
df["Calculated SPI"] = (df["Earned Value ($M)"] / df["Planned Value ($M)"]).round(2)
df["AI Risk Status"] = df.apply(
    lambda row: "🚨 CRITICAL RISK" if row["Calculated CPI"] < 0.9 or row["Calculated SPI"] < 0.9 else "🟢 STABLE PIPELINE", 
    axis=1
)

# 3. Sidebar Controls & Security Simulation
st.sidebar.header("🔑 Authentication Gate")

# NEW: Security Credentials Selectbox
user_role = st.sidebar.selectbox(
    "Select Your Session Profile:",
    ["Standard Guest Analyst", "Authorized Risk Officer 💎"]
)

st.sidebar.divider()
st.sidebar.header("🕹️ Filter Options")

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

# Apply Core Filters
filtered_df = df.copy()
if selected_status != "All Statuses":
    filtered_df = filtered_df[filtered_df["AI Risk Status"] == selected_status]

filtered_df = filtered_df[
    (filtered_df["Planned Value ($M)"] >= budget_range[0]) & 
    (filtered_df["Planned Value ($M)"] <= budget_range[1])
]

# NEW: Security Column Slicing Logic
# If the user is just a standard guest, we strip out the confidential "Restricted Audit Note" column completely!
if user_role == "Standard Guest Analyst":
    display_df = filtered_df.drop(columns=["Restricted Audit Note"])
else:
    display_df = filtered_df.copy()

# 4. Interface Columns
c1, c2 = st.columns([1, 1])

with c1:
    st.markdown(f"### 📋 Filtered Data Grid ({user_role})")
    if display_df.empty:
        st.warning("⚠️ No projects match criteria.")
    else:
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.divider()
        csv_buffer = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Export Data Subset as CSV",
            data=csv_buffer,
            file_name="secure_risk_report.csv",
            mime="text/csv",
            use_container_width=True
        )

with c2:
    st.markdown(f"### 📊 Portfolio {chart_metric[-3:]} Comparison")
    if display_df.empty:
        st.info("Adjust filters to generate visual chart.")
    else:
        chart_data = display_df.set_index("Infrastructure Project Name")[[chart_metric]]
        st.bar_chart(chart_data)
        
        # NEW: Security Notice Box based on role permissions
        if user_role == "Authorized Risk Officer 💎":
            st.info("🔓 Privileged Access Granted: Displaying internal audit safety commentary notes inside your data grid.")
        else:
            st.warning("🔒 Confidential Columns Redacted: Elevate your session profile in the sidebar to view restricted audit commentary strings.")