import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const TOOL_LABELS = {
  search_knowledge_base: { icon: "📋", label: "Searched personal profile" },
  search_wikipedia: { icon: "🌐", label: "Searched Wikipedia" },
};

export default function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`message-row ${isUser ? "user-row" : "assistant-row"}`}>
      {!isUser && (
        <div className="avatar assistant-avatar" title="Dhivya AI Agent">
          D
        </div>
      )}

      <div className={`message-bubble ${isUser ? "user-bubble" : "assistant-bubble"}`}>
        {/* Search action badges (shown on assistant messages) */}
        {!isUser && message.searchActions && message.searchActions.length > 0 && (
          <div className="search-actions">
            {message.searchActions.map((action, i) => {
              const meta = TOOL_LABELS[action.tool] || {
                icon: "🔍",
                label: action.tool,
              };
              return (
                <span key={i} className="search-badge" title={action.query}>
                  {meta.icon} {meta.label}: <em>{action.query}</em>
                </span>
              );
            })}
          </div>
        )}

        {/* Message content */}
        {isUser ? (
          <p className="user-text">{message.content}</p>
        ) : (
          <div className="assistant-text">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          </div>
        )}
      </div>

      {isUser && (
        <div className="avatar user-avatar" title="You">
          U
        </div>
      )}
    </div>
  );
}
