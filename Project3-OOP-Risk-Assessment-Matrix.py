# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 17:31:36 2026

@author: Rouzbeh
"""

# -*- coding: utf-8 -*-
"""
Created on Friday, June 19, 2026
@author: Rouzbeh
Project 3: Object-Oriented Project Delivery Suite with KNN Risk Classification & Excel Automation
"""
import numpy as np
import xlsxwriter
from sklearn.neighbors import KNeighborsClassifier

class EnterpriseProjectTask:
    """Class representing an independent project task tracking metrics and AI risk states."""
    def __init__(self, task_id, task_name, planned_value, actual_cost, earned_value):
        self.task_id = task_id
        self.task_name = task_name
        self.planned_value = float(planned_value)
        self.actual_cost = float(actual_cost)
        self.earned_value = float(earned_value)
        self.predicted_risk = "PENDING AI EVALUATION"

    def calculate_cost_variance(self):
        return self.earned_value - self.actual_cost

    def calculate_cpi(self):
        if self.actual_cost == 0: return 1.0
        return self.earned_value / self.actual_cost

    def calculate_spi(self):
        if self.planned_value == 0: return 1.0
        return self.earned_value / self.planned_value

    def generate_executive_row(self):
        cpi = self.calculate_cpi()
        spi = self.calculate_spi()
        print(f"{self.task_id:<8} | {self.task_name:<30} | {cpi:<6.2f} | {spi:<6.2f} | {self.predicted_risk}")


class TaskRiskClassifier:
    """Class handling the Machine Learning KNN model to evaluate project risk profiles."""
    def __init__(self, k_neighbors=3):
        self.model = KNeighborsClassifier(n_neighbors=k_neighbors)
        
    def train_model(self):
        print("🧠 AI ENGINE: Training KNN Classifier...")
        # Historical metrics baseline: [CPI, SPI]
        historical_features = np.array([
            [1.20, 1.15], [1.05, 1.10], [1.00, 1.00],  # Stable tasks
            [0.95, 0.90], [0.85, 0.88], [0.90, 0.80],  
            [0.60, 0.55], [0.50, 0.62], [0.45, 0.50]   # Critical risk tasks
        ])
        historical_labels = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1]) # 0=Stable, 1=Critical
        self.model.fit(historical_features, historical_labels)
        print("✔ AI ENGINE: Training complete.\n")

    def evaluate_task(self, task_object):
        cpi = task_object.calculate_cpi()
        spi = task_object.calculate_spi()
        input_data = np.array([[cpi, spi]])
        prediction = self.model.predict(input_data)[0]
        if prediction == 1:
            task_object.predicted_risk = "🚨 CRITICAL RISK"
        else:
            task_object.predicted_risk = "🟢 STABLE PIPELINE"


class CorporateExcelExporter:
    """Class managing automated, executive-ready Excel file generation and formatting."""
    def __init__(self, filename="Project_Risk_Executive_Report.xlsx"):
        self.filename = filename

    def export_backlog(self, task_list):
        print(f"📊 EXCEL ENGINE: Generating automated report: {self.filename}...")
        workbook = xlsxwriter.Workbook(self.filename)
        worksheet = workbook.add_worksheet("Operational Performance")
        
        # Structure columns
        worksheet.set_column('B:B', 12)
        worksheet.set_column('C:C', 35)
        worksheet.set_column('D:F', 15)

        # Executive Formatting Styles
        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#1F4E78'})
        header_format = workbook.add_format({'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white', 'border': 1, 'align': 'center'})
        data_format = workbook.add_format({'border': 1, 'align': 'left'})
        num_format = workbook.add_format({'border': 1, 'num_format': '0.00', 'align': 'right'})
        alert_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'border': 1, 'align': 'center'})

        # Write Headers
        worksheet.write('B2', "Enterprise Risk Management Dashboard", title_format)
        worksheet.write('B3', "Operational Risk Evaluation Pipeline Powered by KNN Machine Learning")

        headers = ["Task ID", "Project Task Name", "Calculated CPI", "Calculated SPI", "AI Risk Assessment"]
        for col_num, header_title in enumerate(headers, start=1):
            worksheet.write(5, col_num, header_title, header_format)

        # Write Data
        start_row = 6
        for idx, task in enumerate(task_list):
            current_row = start_row + idx
            worksheet.write(current_row, 1, task.task_id, data_format)
            worksheet.write(current_row, 2, task.task_name, data_format)
            worksheet.write(current_row, 3, task.calculate_cpi(), num_format)
            worksheet.write(current_row, 4, task.calculate_spi(), num_format)
            if "CRITICAL" in task.predicted_risk:
                worksheet.write(current_row, 5, task.predicted_risk, alert_format)
            else:
                worksheet.write(current_row, 5, task.predicted_risk, data_format)
                
        workbook.close()
        print("✔ EXCEL ENGINE: Report generation complete.\n")


# Execution block to run everything smoothly
if __name__ == "__main__":
    print("=" * 85)
    ai_brain = TaskRiskClassifier(k_neighbors=3)
    ai_brain.train_model()

    project_backlog = [
        EnterpriseProjectTask("TSK-001", "Database Migration Phase 1", planned_value=5000, actual_cost=9500, earned_value=4000),
        EnterpriseProjectTask("TSK-002", "API Gateway Integration", planned_value=3500, actual_cost=3100, earned_value=3800),
        EnterpriseProjectTask("TSK-003", "Frontend Dashboard Refactor", planned_value=8000, actual_cost=15000, earned_value=6000),
        EnterpriseProjectTask("TSK-004", "Security Compliance Audit", planned_value=2000, actual_cost=1800, earned_value=2000)
    ]

    print(f"{'ID':<8} | {'Task Name':<30} | {'CPI':<6} | {'SPI':<6} | {'AI Risk Assessment'}")
    print("-" * 85)
    for task in project_backlog:
        ai_brain.evaluate_task(task)
        task.generate_executive_row()
    print("-" * 85)

    exporter = CorporateExcelExporter()
    exporter.export_backlog(project_backlog)
    print("=" * 85)