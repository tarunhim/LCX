import feedparser
import requests
from openai import OpenAI
import pyshorteners
import sqlite3
from flask import Flask, render_template
import time

RSS_FEED = "http://rss.cnn.com/rss/edition.rss" 
OPENAI_API_KEY = "your_openai_api_key"
DATABASE = "articles.db"


app = Flask(__name__)


def setup_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, url TEXT UNIQUE)''')
    conn.commit()
    conn.close()

def is_new_article(url):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE url = ?", (url,))
    result = c.fetchone()
    conn.close()
    return result is None

def save_article(url):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO articles (url) VALUES (?)", (url,))
    conn.commit()
    conn.close()

def fetch_latest_articles():
    feed = feedparser.parse(RSS_FEED)
    articles = []
    # print("feed", feed.entries[0])
    for entry in feed.entries:
        # print("entry", entry.title)
        if is_new_article(entry.link):
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "summary": entry.title,
            })
            save_article(entry.link)
    return articles

def generate_caption(title, summary):
    # prompt = f"Write a 2-3 sentence caption for an article titled '{title}' with the summary: {summary}"
    # headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    # response = requests.post("https://api.openai.com/v1/completions", json={
    #     "model": "text-davinci-003",
    #     "prompt": prompt,
    #     "max_tokens": 50
    # }, headers=headers)
    # return response.json()['choices'][0]['text'].strip()
    return title

def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

# def generate_image(prompt):
#     headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
#     response = requests.post("https://api.openai.com/v1/images/generations", json={
#         "prompt": prompt,
#         "n": 1,
#         "size": "1024x1024"
#     }, headers=headers)
#     return response.json()['data'][0]['url']

def fetch_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    return c.fetchall()

@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM articles")
    data = c.fetchall()
    conn.close()
    return render_template("index.html", articles=data)

def automation_process():
    while True:
        setup_database()
        articles = fetch_latest_articles()
        for article in articles:
            caption = generate_caption(article["title"], article["summary"]) # currently return title itself as need open api key for caption generation for which i didn't got the time to R&D about
            short_url = shorten_url(article["url"])
            # image_url = generate_image(article["title"]) As i don't have dall e api key currently
            with open("static/uploads.txt", "a") as file:
                file.write(f"{caption} - {short_url}\n")
        print("Automation complete.")
        # print(len(fetch_data()))
        time.sleep(10)


if __name__ == "__main__":
    automation_process()
    app.run(port=8088)