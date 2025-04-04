# HTMX + Flask + PostgreSQL 项目搭建指南

## 1. 安装依赖
首先，确保你已经安装了 Python 和 PostgreSQL。

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# 安装 Flask 及相关依赖
pip install flask flask_sqlalchemy psycopg2 htmx
```

## 2. 创建 Flask 应用

## 3. 配置数据库

```bash
# 创建 PostgreSQL 用户和数据库
sudo -u postgres psql
CREATE DATABASE blog;
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE blog TO username;
```

## 4. 创建前端页面

### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>博客</title>
    <script src="https://unpkg.com/htmx.org@1.9.6"></script>
</head>
<body>
    <h1>博客文章</h1>
    <div id="post-list" hx-get="/posts" hx-trigger="load" hx-swap="innerHTML"></div>
    <h2>添加文章</h2>
    <form hx-post="/add_post" hx-target="#post-list" hx-swap="beforeend">
        <input type="text" name="title" placeholder="标题" required>
        <textarea name="content" placeholder="内容" required></textarea>
        <button type="submit">提交</button>
    </form>
</body>
</html>
```

### `templates/posts.html`

```html
{% for post in posts %}
    <div>
        <h3>{{ post.title }}</h3>
        <p>{{ post.content }}</p>
    </div>
{% endfor %}
```

### `templates/post_item.html`

```html
<div>
    <h3>{{ post.title }}</h3>
    <p>{{ post.content }}</p>
</div>
```

## 5. 运行项目

```bash
flask run
```

项目将会运行在 `http://127.0.0.1:5000/`。
