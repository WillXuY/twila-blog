-- 使用 twila_admin 用户来操作
-- $ podman exec -it pgsql psql -U postgres
-- 在数据库中操作： \c twila_blog twila_admin

CREATE TABLE twila_app.conversations (
    id UUID PRIMARY KEY,
    title TEXT DEFAULT 'New Chat',
    user_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE twila_app.messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES twila_app.conversations(id) ON DELETE CASCADE,
    role TEXT CHECK (role IN ('user', 'assistant')) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
