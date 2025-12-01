import React from "react";

const ChatMessage = ({ role, text }) => {
  const isUser = role === "user";

  // Convert non-string types (objects) to string safely
  const displayText =
    typeof text === "string" ? text : JSON.stringify(text, null, 2);

  return (
    <div className={`message-row ${isUser ? "user" : "assistant"}`}>
      <div className="bubble">
        <pre className="bubble-text">{displayText}</pre>
      </div>
    </div>
  );
};

export default ChatMessage;