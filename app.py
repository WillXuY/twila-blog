from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import psycopg2
import markdown

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index_juejin.html")

@app.route("/posts")
def get_posts():
    page = int(request.args.get("page", 1))
    limit = 5
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, LEFT(content, 100) FROM posts ORDER BY id DESC LIMIT %s OFFSET %s", (limit, offset))
    posts = cursor.fetchall()
    conn.close()

    html_response = ""
    for post_id, title, preview in posts:
        html_response += f"""
        <div class="post card">
            <h3>{title}</h3>
            <p class="truncate">{preview}...</p>
            <a href="/post/{post_id}" class="btn blue">阅读更多</a>
        </div>
        """

    return html_response

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post:
        return render_template("post_detail.html", post={
            "title": post[0],
            "content": markdown.markdown(post[1])
        })
    else:
        return "文章未找到", 404

@app.route("/add_post", methods=["POST"])
def add_post():
    title = request.form["title"]
    content = request.form["content"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id;", (title, content))
    post_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return f"""
    <div class="post card">
        <h3>{title}</h3>
        <p class="truncate">{content[:100]}...</p>
        <a href="/post/{post_id}" class="btn blue">阅读更多</a>
    </div>
    """

@app.route("/posts_json")
def get_posts_json():
    page = int(request.args.get("page", 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, LEFT(content, 100) FROM posts ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
    rows = cursor.fetchall()
    conn.close()

    posts = [{"id": r[0], "title": r[1], "preview": r[2]} for r in rows]
    return {"posts": posts}

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
