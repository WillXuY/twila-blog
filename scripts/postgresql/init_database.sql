-- I. 创建数据库与用户 (!!! 需要修改密码 !!!)
-- 1. 创建 DBA 用户（拥有数据库）
-- 2. 创建程序用户
-- 3. 创建数据库并设置 owner 为 DBA

-- 先使用 podman 连接数据库
-- $ sudo podman exec -it pgsql psql -U postgres

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

-- II. 切换用户到 twila_blog 数据库来继续授权操作
\c twila_blog

GRANT CONNECT ON DATABASE twila_blog TO twila_app;

-- III. 创建 schema

CREATE SCHEMA IF NOT EXISTS twila_app;

-- 授权给 twila_admin（DBA 用户）：可以在该 schema 中创建、管理表和序列
GRANT CREATE, USAGE ON SCHEMA twila_app TO twila_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA twila_app TO twila_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA twila_app TO twila_admin;

-- 授权给 twila_app（程序用户）：只做增删改查，不创建表/序列
GRANT USAGE ON SCHEMA twila_app TO twila_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA twila_app TO twila_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA twila_app TO twila_app;

ALTER DEFAULT PRIVILEGES FOR USER twila_admin IN SCHEMA twila_app
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO twila_app;
ALTER DEFAULT PRIVILEGES FOR USER twila_admin IN SCHEMA twila_app
  GRANT USAGE, SELECT ON SEQUENCES TO twila_app;

ALTER ROLE twila_app SET search_path = twila_app;
