-- 1. 创建数据库
CREATE DATABASE htmx_flask_blog_data;

-- 2. 创建用户并设置密码
CREATE USER htmx_flask_blog_user WITH PASSWORD 'your_password';

-- 3. 赋予用户对数据库的所有权限
GRANT ALL PRIVILEGES ON DATABASE htmx_flask_blog_data TO htmx_flask_blog_user;

-- 4. 切换到新创建的数据库
\c htmx_flask_blog_data

-- 5. 创建 posts 表格
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL
);

-- 6. 为所有现有表格授予权限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO htmx_flask_blog_user;

-- 7. 为所有现有序列授予权限
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO htmx_flask_blog_user;

-- 8. 确保对将来创建的表和序列也有权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO htmx_flask_blog_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO htmx_flask_blog_user;

-- 9. 确保对将来创建的函数也有权限
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT EXECUTE ON FUNCTIONS TO htmx_flask_blog_user;
