from groq import Groq
import json


def analyze_risk(summary_text):
    """
    Uses an AI model to analyze environmental risk from a summary.
    Returns a structured JSON object.
    """
    result = ""
    try:
        if summary_text:
            system_prompt = """
            You are an AI assistant analyzing environmental risks.
            Return a **valid JSON object** with the following structure:
            {
                "project_overview": "Brief description of the environmental topic.",
                "risk": "Main environmental risk identified (max 3 words)",
                "key_factors": ["Factor 1", "Factor 2", "Factor 3"],
                "key_points": ["Insight 1", "Insight 2"],
                "severity": 1-10
            }
            Do not include any extra text.
            """
            user_prompt = f"Analyze the following summary and return structured JSON:\n{summary_text}"
            full_prompt = f"{system_prompt}\n{user_prompt}"
            client = Groq(
                api_key="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"
            )
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
                model="llama3-70b-8192",
            )
            result = response.choices[0].message.content
            return json.loads(result)
    except Exception as e:
        print(f"Error during risk analysis: {e}")
        return {
            "project_overview": "⚠️ No analysis available.",
            "key_factors": ["Error processing data"],
            "key_points": ["Please try again later."],
            "severity": 5,
        }
    return result


def format_analysis_report(analysis_raw):
    """
    Formats the risk analysis output into a human-readable report.
    """
    try:
        if not analysis_raw or not analysis_raw.strip():
            return "⚠️ No risk analysis available."

        try:
            risk_info = json.loads(analysis_raw)
        except json.JSONDecodeError:
            print("Warning: Received non-JSON response from AI.")
            return f"**Risk Analysis Report**\n\n{analysis_raw}"

        report = "**🌍 Risk Analysis Report**\n\n"
        report += f"📌 **Project Overview:**\n{risk_info.get('project_overview', 'No description provided.')}\n\n"
        report += "**🔹 Key Environmental Risk Factors:**\n"
        for factor in risk_info.get("key_factors", []):
            report += f"- {factor}\n"
        report += "\n**📊 Key Insights:**\n"
        for point in risk_info.get("key_points", []):
            report += f"- {point}\n"
        report += f"\n⚠️ **Severity Level:** {risk_info.get('severity', 'N/A')} (Scale: 1-10)\n"
        return report
    except Exception as ex:
        print(f"Error formatting analysis report: {ex}")
        return "⚠️ Error processing risk analysis."


if __name__ == "__main__":
    sample_summary = (
        "Recent wildfires in California have increased air pollution levels significantly, "
        "leading to public health concerns."
    )
    print(analyze_risk(sample_summary))
