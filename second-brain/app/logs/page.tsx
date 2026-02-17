"use client";

import { useState, useEffect } from "react";

interface LogEntry {
  timestamp: string;
  category: string;
  message: string;
  level: "info" | "warning" | "error" | "success";
}

export default function LogsPage() {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    // Mock log data - in production, this would come from API
    const mockLogs: LogEntry[] = [
      {
        timestamp: new Date().toISOString(),
        category: "Morning Brief",
        message: "Posted daily brief to Discord #morning-brief",
        level: "success",
      },
      {
        timestamp: new Date(Date.now() - 3600000).toISOString(),
        category: "Trading",
        message: "18-agent deliberation completed for $ASTS",
        level: "info",
      },
      {
        timestamp: new Date(Date.now() - 7200000).toISOString(),
        category: "Social Arb",
        message: "Scanned Reddit wallstreetbets - 3 signals found",
        level: "info",
      },
      {
        timestamp: new Date(Date.now() - 10800000).toISOString(),
        category: "Weather Trading",
        message: "Checked Simmer portfolio - 2 positions open",
        level: "info",
      },
      {
        timestamp: new Date(Date.now() - 14400000).toISOString(),
        category: "System",
        message: "Memory file 2026-02-15.md created",
        level: "success",
      },
    ];

    setLogs(mockLogs);
  }, []);

  const formatTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const levelStyles = {
    info: "bg-blue-100 text-blue-800",
    success: "bg-green-100 text-green-800",
    warning: "bg-yellow-100 text-yellow-800",
    error: "bg-red-100 text-red-800",
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Daily Logs</h1>
        <p className="text-gray-600">Recent activity and system events</p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="space-y-3">
          {logs.map((log, index) => (
            <div
              key={index}
              className="flex items-start space-x-4 p-3 bg-gray-50 rounded-md hover:bg-gray-100 transition-colors"
            >
              <div className="text-xs text-gray-500 w-16 flex-shrink-0">
                {formatTime(log.timestamp)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <span
                    className={`text-xs px-2 py-1 rounded font-semibold ${
                      levelStyles[log.level]
                    }`}
                  >
                    {log.category}
                  </span>
                </div>
                <p className="text-sm text-gray-900">{log.message}</p>
              </div>
            </div>
          ))}
        </div>

        {logs.length === 0 && (
          <div className="text-center py-8 text-gray-600">
            No recent activity
          </div>
        )}
      </div>

      <div className="mt-6 text-xs text-gray-500 text-center">
        💡 Logs are aggregated from cron jobs, scripts, and system events
      </div>
    </div>
  );
}
