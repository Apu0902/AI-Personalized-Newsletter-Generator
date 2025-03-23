import os
import torch
from collections import defaultdict
from transformers import pipeline
import feedparser
from sentence_transformers import SentenceTransformer, util

# Prevent TensorFlow/Keras code paths from triggering since we're using PyTorch only.
os.environ["USE_TF"] = "0"

# ------------------------------------------------------------------------------
# Set up the summarization pipeline using a PyTorch-based model.
# Using Facebook's BART model for summarization.
# ------------------------------------------------------------------------------
summarizer_pipeline = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    framework="pt",
    device=0  # Use GPU if available.
)

# ------------------------------------------------------------------------------
# Set up the zero-shot classification pipeline using a PyTorch model.
# We're using the "joeddav/xlm-roberta-large-xnli" model which is fully PyTorch.
# ------------------------------------------------------------------------------
classifier = pipeline(
    "zero-shot-classification",
    model="joeddav/xlm-roberta-large-xnli",
    framework="pt",
    device=0,
    use_fast=False  # Disable the fast tokenizer
)


# ------------------------------------------------------------------------------
# Define user personas along with their dedicated RSS feed URLs and interest preferences.
# This dictionary is used to determine which topics are of interest for each persona.
# ------------------------------------------------------------------------------
users = {
    "Alex Parker": {
        "rss_feeds": [
            "https://www.wired.com/feed/category/ai/latest/rss",
            "https://techcrunch.com/feed/",
            "https://www.technologyreview.com/feed/"
        ],
        "preferences": ["Artificial Intelligence", "Cybersecurity", "Blockchain", "Startups", "Programming"]
    },
    "Priya Sharma": {
        "rss_feeds": [
            "https://www.cnbc.com/id/10000664/device/rss/rss.html",
            "https://feeds.finance.yahoo.com/rss/2.0/headline?s=yhoo&region=US&lang=en-US"
        ],
        "preferences": ["Markets", "Finance", "Fintech", "Cryptocurrency", "Economy"]
    },
    "Marco Rossi": {
        "rss_feeds": [
            "https://www.espn.com/espn/rss/news",
            "https://www.skysports.com/rss/12040"
        ],
        "preferences": ["Football", "F1", "NBA", "Olympics", "Esports"]
    },
    "Lisa Thompson": {
        "rss_feeds": [
            "https://variety.com/v/entertainment/feed/",
            "https://www.billboard.com/feed/",
            "https://www.rollingstone.com/feed/",
            "https://ew.com/entertainment/rss"
        ],
        "preferences": ["Movies", "Celebrity News", "TV Shows", "Music", "Books"]
    },
    "David Martinez": {
        "rss_feeds": [
            "https://www.nasa.gov/rss/dyn/breaking_news.rss",
            "https://www.sciencedaily.com/rss/top/science.xml",
            "https://www.technologyreview.com/feed/",
            "https://www.nature.com/subjects/artificial-intelligence.rss"
        ],
        "preferences": ["Space Exploration", "Artificial Intelligence", "Biotech", "Physics", "Renewable Energy"]
    }
}

# ------------------------------------------------------------------------------
# Function: fetch_rss_articles
# Description: Given a list of RSS feed URLs, this function uses feedparser to parse
# each feed and extract articles with their title, link, summary, published date, and source.
# ------------------------------------------------------------------------------
def fetch_rss_articles(feed_urls):
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'summary': entry.summary if "summary" in entry else "",
                'published': entry.published if "published" in entry else "",
                'source': url
            })
    return articles

# ------------------------------------------------------------------------------
# Function: fetch_articles
# Description: Fetches articles for a given persona using the RSS feeds defined in the users dictionary.
# ------------------------------------------------------------------------------
def fetch_articles(persona):
    feeds = users[persona]["rss_feeds"]
    articles = fetch_rss_articles(feeds)
    return articles

# ------------------------------------------------------------------------------
# Global dictionary to cache article predictions (to avoid duplicate computations).
# ------------------------------------------------------------------------------
article_predictions = {}

# ------------------------------------------------------------------------------
# Function: predict_article_categories
# Description: For each article, use the zero-shot classifier to predict the most relevant category.
# The function stores predictions (predicted label and score) in the global article_predictions dictionary.
# ------------------------------------------------------------------------------
def predict_article_categories(articles):
    # Build the set of all labels from all personas' preferences.
    all_labels = list({label for persona_data in users.values() for label in persona_data["preferences"]})
    for article in articles:
        article_text = article['title'] + ". " + article['summary']
        result = classifier(article_text, all_labels)
        article_predictions[article['title']] = {
            'predicted_label': result['labels'][0],
            'score': result['scores'][0]
        }
        print(f"Predicted: {result['labels'][0]} ({result['scores'][0]:.2f}) for Article: {article['title'][:50]}...")
    return article_predictions

# ------------------------------------------------------------------------------
# Function: categorize_articles
# Description: Assigns each article to one category based on a combined scoring system:
# - Uses the classifier's predicted label (if confident enough).
# - Adds a keyword bonus if the article text contains the interest.
# - Selects the best matching category for each article.
# - Defaults to "General Updates" if no category meets the threshold.
# Deduplication is applied so each article appears only once.
# ------------------------------------------------------------------------------
def categorize_articles(articles, user_preferences):
    # Define a threshold for assignment.
    THRESHOLD = 0.5
    # Bonus added if keyword is found.
    KEYWORD_BONUS = 0.1

    final_assignment = {}
    
    for article in articles:
        article_text = (article['title'] + " " + article['summary']).lower()
        prediction = article_predictions.get(article['title'], None)
        # Initialize scores for each preference.
        scores = {pref: 0.0 for pref in user_preferences}
        
        # If the classifier predicted a label among the user's preferences, add its score.
        if prediction and prediction['predicted_label'] in user_preferences:
            scores[prediction['predicted_label']] = prediction['score']
        
        # Add a keyword bonus if the article text contains the preference.
        for pref in user_preferences:
            if pref.lower() in article_text:
                scores[pref] += KEYWORD_BONUS
        
        # Choose the interest with the highest score.
        best_pref = max(scores, key=lambda x: scores[x])
        best_score = scores[best_pref]
        
        # If the best score is below the threshold, assign to "General Updates".
        assigned_category = best_pref if best_score >= THRESHOLD else "General Updates"
        
        # Ensure each article appears only once (using title as key).
        if article['title'] not in final_assignment:
            final_assignment[article['title']] = assigned_category

    # Build the final categorized dictionary.
    categorized = defaultdict(list)
    for article in articles:
        cat = final_assignment.get(article['title'], "General Updates")
        categorized[cat].append(article)
    
    return categorized

# ------------------------------------------------------------------------------
# Function: summarize_article
# Description: Uses the summarization pipeline to generate a summary for the given article text.
# ------------------------------------------------------------------------------
def summarize_article(article_text):
    try:
        summary = summarizer_pipeline(article_text[:1024], max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        return summary
    except Exception:
        return article_text[:200] + '...'

# ------------------------------------------------------------------------------
# Function: build_markdown_newsletter
# Description: Generates a Markdown-formatted newsletter by combining categorized articles.
# ------------------------------------------------------------------------------
def build_markdown_newsletter(user, categorized_articles):
    md = f"# Personalized Newsletter for {user}\n\n"
    md += "## Highlights\n\n"
    # Build a highlights section using the first two articles of each category.
    for category, articles in categorized_articles.items():
        md += f"### {category}\n"
        for article in articles[:2]:
            md += f"- [{article['title']}]({article['link']})\n"
        md += "\n"
    md += "---\n\n"
    # Build detailed sections for each category.
    for category, articles in categorized_articles.items():
        md += f"## {category}\n"
        for article in articles:
            md += f"### [{article['title']}]({article['link']})\n"
            md += f"*{article['published']} - {article['source']}*\n\n"
            md += f"{article['summary']}\n\n"
        md += "\n"
    return md
