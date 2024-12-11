
import time
import pyshorteners



POLL_INTERVAL = 3 
DATABASE = "articles.db"

def setup_database():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY, post_id INTEGER UNIQUE, url TEXT, caption TEXT, short_url TEXT)''')
    conn.commit()
    conn.close()

def save_if_not_present(post_id, url, caption):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE post_id = ?", (post_id,))
    existing_post = c.fetchone()

    if existing_post:
        c.execute("UPDATE articles SET caption = ?, short_url = ? WHERE post_id = ?", (caption, short_url, post_id))
        conn.commit()
        return False
    else:
        c.execute("INSERT INTO articles (post_id, url, caption, short_url) VALUES (?, ?, ?, ?)", (post_id, url, caption, short_url))
        conn.commit()
        return True

    conn.close()

def get_recent_posts():
    # url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media"
    # params = {"fields": "id,caption,media_type,media_url,timestamp", "access_token": ACCESS_TOKEN}
    # response = requests.get(url, params=params)
    # if response.status_code != 200:
    #     raise Exception(f"Error fetching posts: {response.json()}")
    # return response.json().get("data", [])
    objects = [
    {"id": 1, "caption": "This is a caption", "long_url": "https://example.com/article1"},
    {"id": 2, "caption": "Another caption", "long_url": "https://example.com/article2"},
    # ... more objects
    ]
    return objects

def publish_to_instagram(image_url, caption):
    upload_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {"image_url": image_url, "caption": caption, "access_token": ACCESS_TOKEN}
    upload_response = requests.post(upload_url, data=payload)
    if upload_response.status_code != 200:
        raise Exception(f"Error uploading image: {upload_response.json()}")
    media_id = upload_response.json().get("id")

    # Publish post
    publish_url = f"https://graph.facebook.com/v17.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_payload = {"creation_id": media_id, "access_token": ACCESS_TOKEN}
    publish_response = requests.post(publish_url, data=publish_payload)
    if publish_response.status_code != 200:
        raise Exception(f"Error publishing post: {publish_response.json()}")

    print("Post published successfully!")

def shorten_url(url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)

def monitor_and_automate():
    while True:
        try:
            posts = get_recent_posts()
            for post in posts:
                if save_if_not_present(post["id"], post["long_url"], post["caption"]):
                    publish_to_instagram(post["long_url"], post["caption"])
                else:
                    print("Post already exists in database.")
            print("running...", posts)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    monitor_and_automate()