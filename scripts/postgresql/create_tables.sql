-- 使用 twila_admin 用户来操作

CREATE TABLE twila_app.conversations (
    id UUID PRIMARY KEY,
    title TEXT DEFAULT 'New Chat',
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
