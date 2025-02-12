import requests
from bs4 import BeautifulSoup, NavigableString
from urllib.parse import urlparse
import string
import re

def retrieve_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    return domain.replace("www.", "")

def text_is_relevant(text):
    """
    Determines if the provided text is sufficiently meaningful.
    """
    cleaned_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    words = cleaned_text.split()
    
    # Skip very short or uninformative text
    if len(words) < 3:
        return False

    ignored_phrases = ["privacy policy", "terms", "cookie policy", "about", "contact", "subscribe", "follow us", "related topics"]
    if any(phrase in cleaned_text for phrase in ignored_phrases):
        return False
    
    return True

def find_representative_image(soup_obj):
    """
    Extracts a representative image URL from the BeautifulSoup object.
    """
    meta_img = soup_obj.find("meta", property="og:image")
    if meta_img and meta_img.get("content"):
        return meta_img["content"]

    fallback_img = soup_obj.find("img")
    if fallback_img and fallback_img.get("src"):
        return fallback_img["src"]

    return None

def fetch_environmental_news(search_topic):
    """
    Retrieves news articles related to the provided environmental topic.
    """
    urls = fetch_news_links(search_topic)
    articles = []

    for url in urls:
        print(f"Scraping article: {url}")
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error retrieving {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        article_text = extract_text_content(url)
        image_url = find_representative_image(soup)

        if article_text and len(article_text) > 100:
            # Assume the first line is the title and the next few lines form a summary
            title_line = article_text.split("\n")[0].replace("Title: ", "")
            summary_text = " ".join(article_text.split("\n")[1:5])
            articles.append({
                "title": title_line,
                "summary": summary_text,
                "link": url,
                "image": image_url if image_url else None
            })

    return articles

def extract_text_content(url):
    """
    Extracts meaningful text content from a webpage.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        print(f"Failed to retrieve {url}: {e}")
        return None

    if response.status_code != 200:
        print(f"Skipping {url} due to HTTP status: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    error_keywords = ["404 not found", "access denied", "error message", "page not available"]
    page_text = soup.get_text().lower()
    
    if any(error in page_text for error in error_keywords):
        print(f"Skipping {url}: error page detected")
        return None

    collected_text = []
    title = soup.title.string.strip() if soup.title else "No title found"
    collected_text.append(f"Title: {title}\n")

    main_content = soup.find('article') or soup.body
    if main_content is None:
        print(f"Skipping {url}: no main content found")
        return None

    for element in main_content.find_all(['h1', 'h2', 'h3', 'p']):
        snippet = element.get_text(strip=True)
        if text_is_relevant(snippet):
            collected_text.append(snippet)

    return "\n".join(collected_text) if collected_text else None

def fetch_news_links(query):
    """
    Uses a Google News search to find article URLs related to the query.
    """
    query_formatted = query.replace(" ", "+")
    search_url = f"https://www.google.com/search?q={query_formatted}+environmental+risk&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(search_url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"Failed to fetch search results: HTTP {resp.status_code}")
            return []

        soup = BeautifulSoup(resp.text, 'html.parser')
        links = []
        for tag in soup.select("a"):
            href = tag.get("href")
            if href and "/url?q=" in href:
                clean_link = href.split("/url?q=")[1].split("&")[0]
                if clean_link.startswith("http"):
                    links.append(clean_link)
        return links[:5]
    except Exception as err:
        print(f"Error during news link fetching: {err}")
        return []

if __name__ == "__main__":
    topic = "climate change"
    news_articles = fetch_environmental_news(topic)
    for article in news_articles:
        print(f"\nTitle: {article['title']}\nSummary: {article['summary']}\nLink: {article['link']}\n")
