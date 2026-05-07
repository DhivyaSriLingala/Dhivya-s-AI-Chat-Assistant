import { useEffect, useRef } from "react";
import Message from "./Message.jsx";

export default function ChatWindow({ messages, isLoading }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">🤖</div>
          <h2>Ask me anything about Dhivya Sri Lingala</h2>
          <p>I search her personal profile and Wikipedia to give you accurate, grounded answers.</p>
          <div className="suggestion-chips">
            <span className="chip">Who is Dhivya Sri Lingala?</span>
            <span className="chip">What does she work on at Stackyon?</span>
            <span className="chip">What are her technical skills?</span>
            <span className="chip">What is the Wikipedia AI Agent project?</span>
          </div>
        </div>
      )}

      {messages.map((msg, i) => (
        <Message key={i} message={msg} />
      ))}

      {isLoading && (
        <div className="message-row assistant-row">
          <div className="avatar assistant-avatar">D</div>
          <div className="message-bubble assistant-bubble typing-bubble">
            <span className="dot" />
            <span className="dot" />
            <span className="dot" />
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
