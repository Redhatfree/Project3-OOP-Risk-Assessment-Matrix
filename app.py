# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 20:13:42 2026

@author: Rouzbeh
"""

# -*- coding: utf-8 -*-
"""
Created on Monday, June 22, 2026
@author: Rouzbeh
Project 4: Enterprise Risk Management Interactive Streamlit Web Application
"""
import streamlit as st

# 1. Configure Web Page Window Settings
st.set_page_config(page_title="Corporate Risk App", page_icon="🚀", layout="wide")

# 2. Add Executive Header Dashboard Titles
st.title("🚀 Enterprise Risk Management Dashboard")
st.subheader("Project 4: Interactive Operational Risk Pipeline")
st.markdown("Welcome back, Rouzbeh! Adjust the sliders on the sidebar to dynamically calculate project health metrics in real-time.")

st.divider()

# 3. Create Interactive Left Sidebar Sliders
st.sidebar.header("📊 Task Financial Inputs")
planned_value = st.sidebar.slider("Planned Value ($)", min_value=1000, max_value=20000, value=5000, step=500)
actual_cost = st.sidebar.slider("Actual Cost ($)", min_value=1000, max_value=20000, value=9500, step=500)
earned_value = st.sidebar.slider("Earned Value ($)", min_value=1000, max_value=20000, value=4000, step=500)

# 4. Core Math Calculations
cpi = earned_value / actual_cost if actual_cost > 0 else 1.0
spi = earned_value / planned_value if planned_value > 0 else 1.0

# 5. Display Interactive Screen Columns & Metric Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Cost Performance Index (CPI)", value=f"{cpi:.2f}", delta="- Over Budget" if cpi < 1.0 else "✔ Within Budget")

with col2:
    st.metric(label="Schedule Performance Index (SPI)", value=f"{spi:.2f}", delta="- Behind Schedule" if spi < 1.0 else "✔ On Schedule")

with col3:
    # Rule-Based UI Status Color Evaluator
    if cpi < 0.9 or spi < 0.9:
        st.error("🚨 CRITICAL RISK PROFILE DETECTED")
    else:
        st.success("🟢 STABLE WORKSPACE PIPELINE")

st.divider()
st.info("💡 Pro-Tip: Drag those side sliders around to watch the web layout recalculate numbers instantly!")