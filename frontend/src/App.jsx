import { useState } from "react";
import ChatWindow from "./components/ChatWindow.jsx";
import InputBar from "./components/InputBar.jsx";

// In dev, Vite proxies /api → localhost:8000. In production, set VITE_API_URL to your Render backend URL.
const API_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/chat`
  : "/api/chat";

const SUGGESTED_QUESTIONS = [
  "Who is Dhivya Sri Lingala?",
  "What does she work on at Stackyon?",
  "What are her technical skills?",
  "What is the Wikipedia AI Agent project?",
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async (userText) => {
    setError(null);

    const userMessage = { role: "user", content: userText };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error: ${response.status}`);
      }

      const data = await response.json();

      setMessages([
        ...updatedMessages,
        {
          role: "assistant",
          content: data.response,
          searchActions: data.search_actions || [],
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChipClick = (question) => {
    if (!isLoading) sendMessage(question);
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-left">
          <div className="header-avatar">D</div>
          <div>
            <h1 className="header-title">Dhivya AI Agent</h1>
            <p className="header-subtitle">Powered by Claude + RAG · Wikipedia & Personal Profile</p>
          </div>
        </div>
        <button className="clear-button" onClick={clearChat} disabled={messages.length === 0}>
          New Chat
        </button>
      </header>

      {/* Suggestion chips (shown when chat is empty) */}
      {messages.length === 0 && (
        <div className="suggestions-bar">
          {SUGGESTED_QUESTIONS.map((q, i) => (
            <button
              key={i}
              className="chip"
              onClick={() => handleChipClick(q)}
              disabled={isLoading}
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Chat area */}
      <main className="main">
        <ChatWindow messages={messages} isLoading={isLoading} />
      </main>

      {/* Error banner */}
      {error && (
        <div className="error-banner">
          <span>⚠ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {/* Input */}
      <footer className="footer">
        <InputBar onSend={sendMessage} disabled={isLoading} />
        <p className="footer-note">
          Sources: Personal Knowledge Base · Wikipedia · Claude claude-sonnet-4-6
        </p>
      </footer>
    </div>
  );
}
