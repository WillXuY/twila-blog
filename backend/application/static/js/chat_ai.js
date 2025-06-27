const STORAGE_USER = "twila_user_id";
let userId = localStorage.getItem(STORAGE_USER);

if (!userId) {
  const serverUserId = document.body.dataset.serverUserId;
  userId = serverUserId;
  localStorage.setItem(STORAGE_USER, userId);
}
// 每次刷新都重置新的会话
let conversationId = null;

const userInput = document.getElementById("userInput");
const sendBtn   = document.getElementById("sendBtn");
const chatBox   = document.getElementById("chat");

function appendToChat(sender, text) {
  const label = document.createElement("strong");
  label.innerText = sender + ": ";
  chatBox.appendChild(label);
  const span = document.createElement("span");
  span.innerText = text;
  chatBox.appendChild(span);
  chatBox.appendChild(document.createElement("br"));
  chatBox.scrollTop = chatBox.scrollHeight;
}

// === 侧边栏加载历史并渲染主界面 ===
document.getElementById("sidebar-toggle").addEventListener("click", loadHistoryList);
document.getElementById("sidebar-close").addEventListener("click", () => {
  document.getElementById("sidebar").classList.add("hidden");
});

function loadHistoryList() {
  fetch(`/chat/conversations?user_id=${userId}`)
    .then(res => res.json())
    .then(data => {
      const sidebar = document.getElementById("sidebar");
      const content = document.getElementById("sidebar-content");
      content.innerHTML = "";

      if (data.history.length) {
        data.history.forEach(item => {
          const div = document.createElement("div");
          div.textContent = item.title || "Untitled Chat";
          div.style.padding = "8px 0";
          div.style.borderBottom = "1px solid #eee";
          div.dataset.convId = item.id;              // 存储 conversation_id
          div.addEventListener("click", () => {
            // 选中会话，加载该会话的消息
            conversationId = item.id;
            loadConversation(conversationId);
            sidebar.classList.add("hidden");
          });
          content.appendChild(div);
        });
      } else {
        const empty = document.createElement("div");
        empty.textContent = "暂无聊天记录";
        empty.style.color = "#999";
        empty.style.padding = "1rem";
        content.appendChild(empty);
      }

      sidebar.classList.remove("hidden");
    })
    .catch(err => console.error("加载历史记录失败:", err));
}

// === 加载指定会话的所有消息到主界面 ===
function loadConversation(convId) {
  // 1. 清空当前聊天
  chatBox.innerHTML = "";

  // 2. 请求历史消息接口
  fetch(`/chat/conversations/${conversationId}/messages?user_id=${userId}`)
    .then(res => res.json())
    .then(data => {
      // 假设后端返回 { messages: [ { role, content, created_at }, ... ] }
      data.messages.forEach(msg => {
        const sender = msg.role === 'user' ? 'You' : 'AI';
        appendToChat(sender, msg.content);
      });
    })
    .catch(err => {
      console.error("加载会话消息失败:", err);
      appendToChat("Error", "无法加载会话历史");
    });
}

// === 发送新消息逻辑保持不变，只要 conversationId 可能为 null 即可 ===
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", e => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendToChat("You", message);
  userInput.value = "";

  const payload = { user_id: userId, message };
  if (conversationId) payload.conversation_id = conversationId;

  // 准备接收 AI 流式回复
  const aiPrefix = document.createElement("strong");
  aiPrefix.innerText = "AI: ";
  chatBox.appendChild(aiPrefix);
  const replySpan = document.createElement("span");
  chatBox.appendChild(replySpan);
  chatBox.appendChild(document.createElement("br"));
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    // 更新会话 ID
    const newConv = res.headers.get("X-Conversation-Id");
    if (newConv) conversationId = newConv;

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;
    while (!done) {
      const { value, done: d } = await reader.read();
      done = d;
      if (value) {
        replySpan.textContent += decoder.decode(value, { stream: true });
        chatBox.scrollTop = chatBox.scrollHeight;
      }
    }
  } catch (err) {
    appendToChat("Error", err.toString());
  }
}
