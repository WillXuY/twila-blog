from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST")
    )

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/posts")
def get_posts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM posts")
    posts = cursor.fetchall()
    conn.close()

    # 确保返回的 HTML 结构和 `#post-list` 里的一致
    html_response = ""
    for title, content in posts:
        html_response += f"""
        <div class="post">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """

    return html_response

@app.route("/add_post", methods=["POST"])
def add_post():
    title = request.form["title"]
    content = request.form["content"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id;", (title, content))
    conn.commit()
    conn.close()

    return f"""
    <div class="post">
        <h3>{title}</h3>
        <p>{content}</p>
    </div>
    """

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

