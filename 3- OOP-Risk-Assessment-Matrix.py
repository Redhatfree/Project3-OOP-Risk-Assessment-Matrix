# -*- coding: utf-8 -*-
"""
Created on June 17, 2026
@author: Rouzbeh
Project 3 - Milestone 1: Object-Oriented Earned Value Management (EVM) Engine
"""

# ========================================================
# 1. THE DOMAIN OBJECT BLUEPRINT (OOP CLASS)
# ========================================================
class EnterpriseProjectTask:
    """
    Enterprise-level blueprint to instantiate and manage individual project 
    tasks with integrated Earned Value Management (EVM) analytics.
    """
    def __init__(self, task_id, task_name, planned_value, actual_cost, earned_value):
        self.task_id = task_id
        self.task_name = task_name
        self.planned_value = float(planned_value)
        self.actual_cost = float(actual_cost)
        self.earned_value = float(earned_value)

    def calculate_cost_variance(self):
        """Calculates Cost Variance (CV = EV - AC). Positive is good, negative is over budget."""
        return self.earned_value - self.actual_cost

    def calculate_schedule_variance(self):
        """Calculates Schedule Variance (SV = EV - PV). Positive is good, negative is delayed."""
        return self.earned_value - self.self.planned_value if hasattr(self, 'planned_value') else self.earned_value - self.planned_value

    def calculate_cpi(self):
        """Calculates Cost Performance Index (CPI = EV / AC). Guarded against DivisionByZero."""
        if self.actual_cost == 0:
            return 1.0  # Safe default if no cost has been recorded yet
        return self.earned_value / self.actual_cost

    def calculate_spi(self):
        """Calculates Schedule Performance Index (SPI = EV / PV). Guarded against DivisionByZero."""
        if self.planned_value == 0:
            return 1.0  # Safe default if nothing was planned yet
        return self.earned_value / self.planned_value

    def generate_executive_row(self):
        """Processes internal EVM metrics and prints a clean, column-aligned terminal row."""
        cpi = self.calculate_cpi()
        spi = self.calculate_spi()
        cv = self.calculate_cost_variance()
        
        # Determine human-readable cost status from variance math
        if cv < 0:
            cost_status = " OVER BUDGET"
        else:
            cost_status = " WITHIN BUDGET"
            
        # Formatting parameters: 
        # ID: 8 chars left-aligned, Name: 30 chars left-aligned, CPI/SPI: 6 chars with 2 decimal precision
        print(f"{self.task_id:<8} | {self.task_name:<30} | {cpi:<6.2f} | {spi:<6.2f} | {cost_status}")


# ========================================================
# 2. LIVE CONSULTING PIPELINE EXECUTION (RUNNING THE CODE)
# ========================================================
if __name__ == "__main__":
    print("=" * 80)
    print("   ENTERPRISE OPERATIONAL ANALYTICS: EVM PERFORMANCE PIPELINE ENGINE")
    print("=" * 80)

    # Simulate raw tracking data ingestion from an enterprise corporate system
    project_backlog = [
        EnterpriseProjectTask("TSK-001", "Database Migration Phase 1", planned_value=5000, actual_cost=6200, earned_value=4800),
        EnterpriseProjectTask("TSK-002", "API Gateway Integration", planned_value=3500, actual_cost=3100, earned_value=3800),
        EnterpriseProjectTask("TSK-003", "Frontend Dashboard Refactor", planned_value=8000, actual_cost=9500, earned_value=7200),
        EnterpriseProjectTask("TSK-004", "Security Compliance Audit", planned_value=2000, actual_cost=1800, earned_value=2000)
    ]

    # Print Dashboard Column Headers
    print(f"{'ID':<8} | {'Task Name':<30} | {'CPI':<6} | {'SPI':<6} | {'Cost Status'}")
    print("-" * 80)

    # Execute the Object Loop to process and display the data matrix
    for task in project_backlog:
        task.generate_executive_row()

    print("=" * 80)
