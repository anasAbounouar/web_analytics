import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib
import os


matplotlib.use("Agg")

matplotlib.rcParams["font.family"] = "DejaVu Sans"

def generate_risk_bar_chart(risk_items):
    """
    Generates a bar chart displaying environmental risk severity.
    """
    if not risk_items:
        print("⚠️ No risk information provided.")
        return

    risk_df = pd.DataFrame(risk_items)

    # Check that the expected columns exist
    if "risk" not in risk_df.columns or "severity" not in risk_df.columns:
        print("⚠️ Data missing required columns 'risk' or 'severity':", risk_df)
        return

    # If a risk is a list, explode it so each factor has its own row
    risk_df = risk_df.explode("risk")

    plt.figure(figsize=(12, 6))
    sns.barplot(x="risk", y="severity", data=risk_df, palette="coolwarm")
    plt.xticks(rotation=45)
    plt.xlabel("Risk Factors")
    plt.ylabel("Severity Level")
    plt.title("Environmental Risk Assessment")
    plt.tight_layout()
    os.makedirs("static", exist_ok=True)
    plt.savefig("static/risk_chart.png")
    print("✅ Risk chart generated and saved successfully.")

def generate_trend_line_chart(trend_info):
    """
    Creates a line chart to display the trend of an environmental risk over time.
    """
    trend_df = pd.DataFrame(trend_info)
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='date', y='impact', data=trend_df, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Impact Level")
    plt.title("Trend of Environmental Risk Impact Over Time")
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    sample_risks = [
        {"risk": "Air Pollution", "severity": 8},
        {"risk": "Deforestation", "severity": 7},
        {"risk": "Climate Change", "severity": 9},
        {"risk": "Water Scarcity", "severity": 6}
    ]
    generate_risk_bar_chart(sample_risks)
    
    sample_trend = [
        {"date": "2024-01", "impact": 5},
        {"date": "2024-02", "impact": 6},
        {"date": "2024-03", "impact": 8},
        {"date": "2024-04", "impact": 9}
    ]
    generate_trend_line_chart(sample_trend)
