"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface Document {
  name: string;
  path: string;
  size: number;
  modified: string;
  preview: string;
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDoc, setSelectedDoc] = useState<string | null>(null);
  const [docContent, setDocContent] = useState("");

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await fetch("/api/documents");
      const data = await response.json();
      setDocuments(data.documents);
      setLoading(false);
    } catch (error) {
      console.error("Failed to fetch documents:", error);
      setLoading(false);
    }
  };

  const viewDocument = async (name: string) => {
    try {
      const response = await fetch(`/api/document/${name}`);
      const data = await response.json();
      setDocContent(data.content);
      setSelectedDoc(name);
    } catch (error) {
      console.error("Failed to fetch document:", error);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const formatSize = (bytes: number) => {
    return (bytes / 1024).toFixed(1) + " KB";
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading documents...</div>
      </div>
    );
  }

  if (selectedDoc) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-900">{selectedDoc}</h1>
            <button
              onClick={() => setSelectedDoc(null)}
              className="px-4 py-2 text-white bg-gray-900 rounded-md hover:bg-gray-800"
            >
              ← Back to List
            </button>
          </div>
          <div className="prose max-w-none">
            <pre className="whitespace-pre-wrap font-mono text-sm bg-gray-50 p-4 rounded-md overflow-auto max-h-[600px]">
              {docContent}
            </pre>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Daily Memory Files
        </h1>
        <p className="text-gray-600">
          Timeline view of all memory files ({documents.length} total)
        </p>
      </div>

      <div className="space-y-4">
        {documents.map((doc) => (
          <div
            key={doc.name}
            className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 cursor-pointer"
            onClick={() => viewDocument(doc.name)}
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {doc.name}
                </h3>
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                  {doc.preview}
                </p>
                <div className="flex space-x-4 text-xs text-gray-500">
                  <span>📅 {formatDate(doc.modified)}</span>
                  <span>📄 {formatSize(doc.size)}</span>
                </div>
              </div>
              <button className="ml-4 text-blue-600 hover:text-blue-800">
                View →
              </button>
            </div>
          </div>
        ))}
      </div>

      {documents.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-600">No memory files found</p>
        </div>
      )}
    </div>
  );
}
