-- I. 创建数据库与用户 (!!! 需要修改密码 !!!)
-- 1. 创建 DBA 用户（拥有数据库）
-- 2. 创建程序用户
-- 3. 创建数据库并设置 owner 为 DBA

CREATE USER twila_admin WITH
  LOGIN
  ENCRYPTED PASSWORD 'password.';

CREATE USER twila_app WITH
  LOGIN
  ENCRYPTED PASSWORD 'pw.';

CREATE DATABASE twila_blog
  OWNER twila_admin
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8'
  TEMPLATE template0;

-- II. 授权
-- 1. 授予程序用户访问数据库权限
-- 2. 授予 public schema 使用权限
-- 3. 授权现有对象（仅限已有的）
-- 4. 设置未来默认权限（由 twila_admin 创建的表/序列，自动授权给 twila_app）

\connect twila_blog

GRANT CONNECT ON DATABASE twila_blog TO twila_app;

GRANT USAGE ON SCHEMA public TO twila_app;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO twila_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO twila_app;

ALTER DEFAULT PRIVILEGES FOR USER twila_admin IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO twila_app;

ALTER DEFAULT PRIVILEGES FOR USER twila_admin IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO twila_app;
