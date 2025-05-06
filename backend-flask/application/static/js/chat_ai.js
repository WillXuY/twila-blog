// 获取 DOM 元素
const userInput = document.getElementById("userInput");
const sendBtn   = document.getElementById("sendBtn");
const chatBox   = document.getElementById("chat");

// 发送消息
function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    appendToChat("You", message);
    userInput.value = "";

    // 显示 AI 前缀和回复容器
    const aiPrefix = document.createElement("strong");
    aiPrefix.innerText = "AI: ";
    chatBox.appendChild(aiPrefix);

    const replySpan = document.createElement("span");
    chatBox.appendChild(replySpan);
    chatBox.appendChild(document.createElement("br"));
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");

        function read() {
            reader.read().then(({ done, value }) => {
                if (done) return;
                const text = decoder.decode(value, { stream: true });
                replySpan.textContent += text;
                chatBox.scrollTop = chatBox.scrollHeight;
                read();
            });
        }

        read();
    }).catch(err => {
        appendToChat("Error", err.toString());
    });
}

// 在聊天框追加消息
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

// 事件监听
sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", e => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});
