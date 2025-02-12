import pandas as pd
import re

def sanitize_text(input_text):
    """
    Cleans the input text by removing special characters and extra whitespace.
    """
    text = re.sub(r'[^a-zA-Z0-9\s]', '', input_text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def prepare_news_data(news_items):
    """
    Processes a list of news items by cleaning their summaries.
    """
    df = pd.DataFrame(news_items)
    df["cleaned_summary"] = df["summary"].apply(sanitize_text)
    return df

if __name__ == '__main__':
    sample_news = [
        {"title": "Air Pollution Rising", "summary": "Air quality index worsens in major cities due to emissions!"},
        {"title": "Deforestation Increasing", "summary": "Large-scale tree cutting leads to environmental damage..."}
    ]
    processed_df = prepare_news_data(sample_news)
    print(processed_df)
