"use client";

import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false); 

  const sendQuery = async () => {
    if (!query.trim()) {
      alert("Please enter a question!");
      return;
    }

    setLoading(true); 
    setResponse(""); 

    try {
      console.log("📡 Sending request to FastAPI:", query);
      const res = await axios.post("http://localhost:8000/query", { query });

      console.log("✅ AI Response:", res.data.response);
      setResponse(res.data.response);
    } catch (error: any) {
      console.error("❌ API Error:", error);
      setResponse("Failed to fetch response from AI.");
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen p-5 bg-gray-100">
      <h1 className="text-3xl font-bold mb-5">LMS AI Chat</h1>

      <textarea
        className="w-2/3 p-3 border rounded-md"
        placeholder="Ask a question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />

      <button
        onClick={sendQuery}
        className="mt-3 px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
        disabled={loading} 
      >
        {loading ? "Thinking..." : "Ask AI"} 
      </button>

      {loading && (
        <div className="mt-3 text-gray-600 italic">🤖 AI is thinking...</div> 
      )}

      {response && (
        <div className="mt-4 p-4 w-2/3 bg-white shadow rounded-md max-h-[500px] overflow-auto border border-gray-300">
          <h2 className="font-semibold">Response:</h2>
          <ReactMarkdown className="text-justify text-gray-900 leading-relaxed">
            {response}
          </ReactMarkdown>
        </div>
      )}
    </div>
  );
}
