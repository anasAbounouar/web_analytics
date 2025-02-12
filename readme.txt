Project Title: Web Data Scraping and Risk Analysis Using Python and GenAI

Overview:
-------------
This project combines web data scraping with Generative AI to perform environmental risk assessments.
It scrapes environmental news from multiple sources, processes and analyzes the data using a GenAI model,
and visualizes risk severity using interactive charts. The project integrates web scraping, AI analysis, 
and data visualization into a Flask-based web application.

Features:
-------------
• Web Scraping:
  - Utilizes Python libraries (BeautifulSoup, requests) to scrape news articles related to environmental topics.
  - Extracts meaningful content such as titles, summaries, and representative images.

• Data Preprocessing:
  - Cleans and structures scraped data for effective analysis.
  - Filters out irrelevant content and formats data for the AI analysis.

• Generative AI Risk Analysis:
  - Uses a prebuilt GenAI model to assess environmental risks from article summaries.
  - Outputs a structured risk analysis (project overview, key risk factors, critical insights, and severity).

• Visualization:
  - Generates interactive charts (bar chart and trend line chart) using matplotlib and seaborn.
  - Visualizes the risk severity levels to provide clear insights.

• Web Application:
  - A Flask web application that handles data collection, processing, and results display.
  - Provides an interactive user interface with multiple pages including home, loading, and results.

Installation:
-------------
1. Clone the repository:
   git clone https://github.com/anasAbounouar/web_analytics

2. Navigate to the project directory:
   cd web_analytics

3. Install the required dependencies:
   pip install -r requirements.txt

4. Run the Flask application:
   python app.py

Usage:
-------------
• To perform an environmental risk analysis, visit the home page, enter a topic (e.g., “climate change”), 
  and submit your query.
• The application will scrape relevant news articles, analyze risks using GenAI, and display detailed results 
  along with visualizations.

Deployment:
-------------
• Live Deployment Link:
  https://web-analytics-jkpn.onrender.com

GitHub Repository:
-------------
• Repository URL:
  https://github.com/anasAbounouar/web_analytics

