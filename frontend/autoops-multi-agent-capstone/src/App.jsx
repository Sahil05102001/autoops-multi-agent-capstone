import React, { useState, useRef } from "react";
import ChatMessage from "./components/ChatMessage";
import SocialLinks from "./components/SocialLinks";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

export default function App() {
  const [messages, setMessages] = useState([
    { id: 1, role: "assistant", text: "Hi — ask me anything. I'll query the agents." }
  ]);
  const [input, setInput] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const lastId = useRef(2);

  const appendMessage = (msg) => setMessages((m) => [...m, msg]);

  const handleSubmit = async (e) => {
    e?.preventDefault();
    const text = input.trim();
    if (!text) return;

    const userMsg = { id: lastId.current++, role: "user", text };
    appendMessage(userMsg);
    setInput("");
    setIsStreaming(true);

    const assistantPlaceholder = { id: lastId.current++, role: "assistant", text: "" };
    appendMessage(assistantPlaceholder);

    try {
      const res = await fetch(`${BACKEND_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: text })
      });

      if (!res.ok) {
        const errText = await res.text();
        updateAssistant(assistantPlaceholder.id, `Error: ${res.status} - ${errText}`);
        setIsStreaming(false);
        return;
      }

      const data = await res.json();
      let assistantText = data.response || data.error || "No response";

      // Convert object responses to string for display
      if (typeof assistantText === "object") {
        assistantText = JSON.stringify(assistantText, null, 2);
      }

      updateAssistant(assistantPlaceholder.id, assistantText);
      setIsStreaming(false);

    } catch (err) {
      updateAssistant(assistantPlaceholder.id, `Error: ${err.message || err}`);
      setIsStreaming(false);
    }
  };

  const updateAssistant = (id, newText) => {
    setMessages((prev) =>
      prev.map((m) => (m.id === id ? { ...m, text: newText } : m))
    );
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="title">AutoOps — Agent Chat</div>
      </header>
            <SocialLinks/>
      <main className="chat-area">
        <div className="messages">
          {messages.map((m) => (
            <ChatMessage key={m.id} role={m.role} text={m.text} />
          ))}
        </div>
      </main>

      <form className="composer" onSubmit={handleSubmit}>
        <input
          className="input"
          placeholder="Type your prompt..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isStreaming}
          aria-label="Prompt"
        />
        <button className="send" type="submit" disabled={isStreaming || !input.trim()}>
          {isStreaming ? "Streaming…" : "Send"}
        </button>
      </form>
    </div>
  );
}