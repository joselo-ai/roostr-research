"use client";

import { useState, useEffect } from "react";

export default function MemoriesPage() {
  const [content, setContent] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMemory();
  }, []);

  const fetchMemory = async () => {
    try {
      const response = await fetch("/api/memory");
      const data = await response.json();
      setContent(data.content);
      setLoading(false);
    } catch (error) {
      console.error("Failed to fetch memory:", error);
      setLoading(false);
    }
  };

  const saveMemory = async () => {
    setIsSaving(true);
    try {
      await fetch("/api/memory", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
      });
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to save memory:", error);
      alert("Failed to save changes");
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading memory...</div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Long-Term Memory
          </h1>
          <div className="space-x-2">
            {isEditing ? (
              <>
                <button
                  onClick={() => {
                    setIsEditing(false);
                    fetchMemory();
                  }}
                  className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
                >
                  Cancel
                </button>
                <button
                  onClick={saveMemory}
                  disabled={isSaving}
                  className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
                >
                  {isSaving ? "Saving..." : "Save"}
                </button>
              </>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 text-white bg-gray-900 rounded-md hover:bg-gray-800"
              >
                Edit
              </button>
            )}
          </div>
        </div>

        <div className="text-sm text-gray-600 mb-4">
          <strong>File:</strong> MEMORY.md
        </div>

        {isEditing ? (
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full h-[600px] p-4 border border-gray-300 rounded-md font-mono text-sm"
            placeholder="Edit your long-term memory..."
          />
        ) : (
          <div className="prose max-w-none">
            <pre className="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-4 rounded-md overflow-auto max-h-[600px]">
              {content}
            </pre>
          </div>
        )}

        <div className="mt-4 text-xs text-gray-500">
          💡 Tip: This is your curated long-term memory. Daily files are in
          memory/YYYY-MM-DD.md
        </div>
      </div>
    </div>
  );
}
