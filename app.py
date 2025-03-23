import streamlit as st
from newsletter_utils import (
    fetch_articles,
    predict_article_categories,
    categorize_articles,
    summarize_article,
    build_markdown_newsletter,
    users,
)

# Configure the Streamlit page.
st.set_page_config(page_title="AI-Powered Personalized Newsletter", page_icon="📰", layout="wide")
st.title("📰 Personalized AI-Powered Newsletter")

# Sidebar: Allow user to select a persona.
persona = st.sidebar.selectbox("Select User Persona", list(users.keys()))
st.subheader(f"Delivering curated content for **{persona}**")

# ------------------------------------------------------------------------------
# Cache the article fetching and prediction process for all personas once.
# This ensures the heavy computation is done only once per session.
# ------------------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def get_all_articles_and_predictions():
    all_articles = {}
    for p in users.keys():
        articles = fetch_articles(p)
        predict_article_categories(articles)
        all_articles[p] = articles
    return all_articles

all_articles = get_all_articles_and_predictions()
# Retrieve articles for the selected persona.
articles = all_articles[persona]

# Categorize articles using the updated function.
categorized = categorize_articles(articles, users[persona]["preferences"])

# Summarize each article's summary text.
for category, art_list in categorized.items():
    for article in art_list:
        article['summary'] = summarize_article(article['summary'])

# Build the Markdown newsletter.
newsletter_md = build_markdown_newsletter(persona, categorized)

# Display the newsletter.
st.markdown(newsletter_md, unsafe_allow_html=True)
st.success("Newsletter generated successfully!")

# Download button to save the newsletter as a Markdown (.md) file.
st.download_button(
    label="Download Newsletter as MD",
    data=newsletter_md,
    file_name=f"{persona}_newsletter.md",
    mime="text/markdown"
)
