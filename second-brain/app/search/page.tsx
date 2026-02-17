"use client";

import { useState } from "react";

interface SearchResult {
  file: string;
  line: number;
  content: string;
  context: string;
}

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [searching, setSearching] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setSearching(true);
    // TODO: Implement actual search API
    // For now, show placeholder
    setTimeout(() => {
      setResults([
        {
          file: "MEMORY.md",
          line: 42,
          content: "Example search result containing the query...",
          context: "...surrounding context...",
        },
      ]);
      setSearching(false);
    }, 500);
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Search Memory Files
        </h1>
        <p className="text-gray-600">
          Search across MEMORY.md and all daily memory files
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="flex space-x-2 mb-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
            placeholder="Search for keywords, names, dates..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSearch}
            disabled={searching || !query.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {searching ? "Searching..." : "Search"}
          </button>
        </div>

        {results.length > 0 && (
          <div className="space-y-4">
            <div className="text-sm text-gray-600 mb-3">
              Found {results.length} results for "{query}"
            </div>
            {results.map((result, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start mb-2">
                  <span className="font-semibold text-gray-900">
                    {result.file}
                  </span>
                  <span className="text-xs text-gray-500">
                    Line {result.line}
                  </span>
                </div>
                <p className="text-sm text-gray-700 bg-gray-50 p-2 rounded">
                  {result.content}
                </p>
                <p className="text-xs text-gray-500 mt-2">{result.context}</p>
              </div>
            ))}
          </div>
        )}

        {!searching && results.length === 0 && query && (
          <div className="text-center py-8 text-gray-600">
            No results found for "{query}"
          </div>
        )}
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">
          Search Tips
        </h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Use quotes for exact phrases: "Phase 1"</li>
          <li>• Search is case-insensitive</li>
          <li>• Searches across MEMORY.md and memory/*.md files</li>
        </ul>
      </div>
    </div>
  );
}
