
"use client";

import { useState } from "react";

interface Source {
  doc_id: string;
  title: string;
  chunk_index: number;
  score: number;
  text: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
}

export default function Home() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  async function sendMessage() {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userQuestion },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get a response from the server.");
      }

      const data = await response.json();

      // Save the session ID returned by the backend
      setSessionId(data.session_id);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error("Chat API error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Unable to connect to the backend. Please ensure FastAPI is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // Render basic bold Markdown (**text**)
  function renderAnswer(text: string) {
    return text.split(/(\*\*.*?\*\*)/g).map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={index}>
            {part.slice(2, -2)}
          </strong>
        );
      }

      return <span key={index}>{part}</span>;
    });
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white flex flex-col">
      <header className="border-b border-slate-800 p-5">
        <h1 className="text-2xl font-bold">
          Docs Q&A Assistant
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Ask questions about your documentation
        </p>
      </header>

      <section className="flex-1 w-full max-w-4xl mx-auto p-5 space-y-5">
        {messages.length === 0 && (
          <div className="text-center mt-32">
            <h2 className="text-3xl font-semibold">
              How can I help you?
            </h2>
            <p className="text-slate-400 mt-3">
              Ask anything about the available documentation.
            </p>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`rounded-xl p-4 ${
              message.role === "user"
                ? "bg-blue-600 ml-12"
                : "bg-slate-800 mr-12"
            }`}
          >
            <p className="text-xs uppercase text-slate-300 mb-2">
              {message.role}
            </p>

            <p className="whitespace-pre-wrap">
              {message.role === "assistant"
                ? renderAnswer(message.content)
                : message.content}
            </p>

            {message.sources && message.sources.length > 0 && (
              <div className="mt-4 border-t border-slate-600 pt-3">
                <h3 className="font-semibold text-sm mb-2">
                  Sources
                </h3>

                {message.sources.map((source, i) => (
                  <div
                    key={`${source.doc_id}-${source.chunk_index}-${i}`}
                    className="bg-slate-700 rounded-lg p-3 mb-2 text-sm"
                  >
                    <p className="font-medium">
                      {source.doc_id} — {source.title}
                    </p>

                    <p className="text-slate-400 mt-1">
                      Relevance score: {source.score.toFixed(3)}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <p className="text-slate-400 animate-pulse">
            Assistant is thinking...
          </p>
        )}
      </section>

      <footer className="sticky bottom-0 bg-slate-950 border-t border-slate-800 p-4">
        <div className="max-w-4xl mx-auto flex gap-3">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
            placeholder="Ask a question..."
            disabled={loading}
            className="flex-1 rounded-xl bg-slate-800 border border-slate-700 p-4 outline-none focus:border-blue-500"
          />

          <button
            onClick={sendMessage}
            disabled={loading || !question.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-40 rounded-xl px-6 font-semibold"
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </div>
      </footer>
    </main>
  );
}
