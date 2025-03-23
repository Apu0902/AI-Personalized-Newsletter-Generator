# AI-Powered Personalized Newsletter Generator

This project is a Streamlit application that generates personalized newsletters based on RSS feed articles. It uses zero-shot classification and keyword matching to categorize articles into topics that match each user persona's interests. In case of insufficient matches, backup articles are used to ensure that the newsletter has enough content.

## Features

- **Personalized Content:** Curates articles based on user-defined interests.
- **RSS Feed Integration:** Fetches articles from multiple RSS sources.
- **Zero-Shot Classification:** Uses a PyTorch-based zero-shot classifier (`joeddav/xlm-roberta-large-xnli`) to assign articles to relevant categories.
- **Keyword Matching:** Supplements classifier predictions with keyword matching for better accuracy.
- **Summarization:** Summarizes long article texts using a PyTorch-based summarization model (Facebook's BART).
- **Downloadable Newsletter:** Users can download the generated newsletter as a Markdown file.
- **Docker Support:** Containerized using a Dockerfile for easy deployment.

## Files Included

- **app.py**  
  The main Streamlit application file that displays the newsletter and provides a download button.

- **newsletter_utils.py**  
  Contains functions for fetching articles from RSS feeds, predicting and categorizing articles, summarizing content, and building the final Markdown newsletter.

- **backup_articles.json**  
  A sample JSON file with backup articles for each persona in case RSS feeds return too few articles.

- **requirements.txt**  
  Lists all required Python dependencies:
    streamlit 
    feedparser 
    transformers 
    torch 
    sentence-transformers

- **Dockerfile**  
Docker configuration file for containerizing the application.

- **README.md**  
This documentation file.

## Installation

1. **Clone the repository:**

 ```bash
 git clone <repository_url>
 cd AI-Personalized-Newsletter-Generator
 
2. **Install dependencies:**

Make sure you have Python 3.9 or later installed, then run:

pip install -r requirements.txt

Running the Application

Locally via Streamlit

1. Start the Streamlit app by running:

    streamlit run app.py

2. A web browser will open with the application interface. Use the sidebar to select a user persona and view the personalized newsletter. You can also download the newsletter as a Markdown file.

Via Docker

1. Build the Docker image:

    docker build -t newsletter-app .

2.Run the Docker container:

    docker run -p 8501:8501 newsletter-app

3. Open your browser and navigate to http://localhost:8501 to see the app.

Project Structure

    AI-Personalized-Newsletter-Generator/
    ├── app.py
    ├── newsletter_utils.py
    ├── backup_articles.json
    ├── requirements.txt
    ├── Dockerfile
    └── README.md

Acknowledgements
Streamlit for the interactive UI.

Hugging Face Transformers and Sentence-Transformers for the NLP models.

The various news sources whose RSS feeds are used to curate content.


This README should provide a clear overview of your project, installation steps, and usage instructions. Feel free to modify or extend it as needed!






You said:
Give me the readme file in a single document
ChatGPT said:
Reasoned for a second
Below is the complete README file as a single document. You can copy and save it as README.md.

markdown
Copy
Edit
# AI-Powered Personalized Newsletter Generator

This project is a Streamlit application that generates personalized newsletters based on RSS feed articles. It uses zero-shot classification and keyword matching to categorize articles into topics that match each user persona's interests. In case of insufficient matches, backup articles are used to ensure that the newsletter has enough content.

## Features

- **Personalized Content:** Curates articles based on user-defined interests.
- **RSS Feed Integration:** Fetches articles from multiple RSS sources.
- **Zero-Shot Classification:** Uses a PyTorch-based zero-shot classifier (`joeddav/xlm-roberta-large-xnli`) to assign articles to relevant categories.
- **Keyword Matching:** Supplements classifier predictions with keyword matching for better accuracy.
- **Summarization:** Summarizes long article texts using a PyTorch-based summarization model (Facebook's BART).
- **Downloadable Newsletter:** Users can download the generated newsletter as a Markdown file.
- **Docker Support:** Containerized using a Dockerfile for easy deployment.

## Files Included

- **app.py**  
  The main Streamlit application file that displays the newsletter and provides a download button.

- **newsletter_utils.py**  
  Contains functions for fetching articles from RSS feeds, predicting and categorizing articles, summarizing content, and building the final Markdown newsletter.

- **backup_articles.json**  
  A sample JSON file with backup articles for each persona in case RSS feeds return too few articles.

- **requirements.txt**  
  Lists all required Python dependencies:
streamlit feedparser transformers torch sentence-transformers

markdown
Copy
Edit

- **Dockerfile**  
Docker configuration file for containerizing the application.

- **README.md**  
This documentation file.

## Installation

1. **Clone the repository:**

 ```bash
 git clone <repository_url>
 cd AI-Personalized-Newsletter-Generator
Install dependencies:

Make sure you have Python 3.9 or later installed, then run:

bash
Copy
Edit
pip install -r requirements.txt
Running the Application
Locally via Streamlit
Start the Streamlit app by running:

bash
Copy
Edit
streamlit run app.py
A web browser will open with the application interface. Use the sidebar to select a user persona and view the personalized newsletter. You can also download the newsletter as a Markdown file.

Via Docker
Build the Docker image:

bash
Copy
Edit
docker build -t newsletter-app .
Run the Docker container:

bash
Copy
Edit
docker run -p 8501:8501 newsletter-app
Open your browser and navigate to http://localhost:8501 to see the app.

Project Structure
javascript
Copy
Edit
AI-Personalized-Newsletter-Generator/
├── app.py
├── newsletter_utils.py
├── backup_articles.json
├── requirements.txt
├── Dockerfile
└── README.md
License
[Include your chosen license here.]

Acknowledgements
Streamlit for the interactive UI.

Hugging Face Transformers and Sentence-Transformers for the NLP models.

The various news sources whose RSS feeds are used to curate content.

yaml
Copy
Edit

---

Feel free to adjust any sections as needed. This README file provides a complete overview, installation instructions, and usage guidelines for your project.










