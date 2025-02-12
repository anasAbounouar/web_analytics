from flask import Flask, render_template, request, redirect, url_for, jsonify
from scraper import fetch_environmental_news
from llm import analyze_risk, format_analysis_report
from visualization import generate_risk_bar_chart
import json

app = Flask(__name__)

# Temporary in-memory cache for search results
cache_results = {}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic_query = request.form.get("topic")
        if topic_query:
            return redirect(url_for("loading_page", topic=topic_query))
    return render_template("home.html")

@app.route("/loading/<topic>")
def loading_page(topic):
    return render_template("loading.html", topic=topic)

@app.route("/process/<topic>")
def process_data(topic):
    articles = fetch_environmental_news(topic)
    risk_data = []

    for article in articles:
        # Only process if the summary is of sufficient length
        if len(article["summary"]) > 50:
            ai_result = analyze_risk(article["summary"])
            risk_data.append({
                "project_overview": ai_result.get("project_overview", "No overview available."),
                "risk": ai_result.get("risk", "No risk identified."),
                "key_factors": ai_result.get("key_factors", ["No key factors found."]),
                "key_points": ai_result.get("key_points", ["No insights available."]),
                "severity": ai_result.get("severity", 5)
            })

    if risk_data:
        generate_risk_bar_chart(risk_data)

    cache_results[topic] = {"news": articles, "risks": risk_data}
    return jsonify({"status": "done"})

@app.route("/results/<topic>")
def display_results(topic):
    if not topic:
        return "⚠️ No topic provided.", 400

    data = cache_results.get(topic, {"news": [], "risks": []})
    risks = []
    for entry in data["risks"]:
        if isinstance(entry, str):
            try:
                entry = json.loads(entry)
            except json.JSONDecodeError:
                entry = {}
        risks.append({
            "project_overview": entry.get("project_overview", "No overview available."),
            "key_factors": entry.get("key_factors", ["No key factors found."]),
            "key_points": entry.get("key_points", ["No insights available."]),
            "severity": entry.get("severity", "N/A")
        })

    return render_template("results.html", topic=topic, news=data["news"], risks=risks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
