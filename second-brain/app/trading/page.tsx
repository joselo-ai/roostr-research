"use client";

import { useState, useEffect } from "react";

export default function TradingPage() {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Trading Signals & Analysis
        </h1>
        <p className="text-gray-600">
          18-agent deliberations and conviction scores
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Phase 1 Status
          </h3>
          <div className="space-y-3">
            <StatRow label="Portfolio Size" value="$1M Paper" />
            <StatRow label="Target Returns" value=">20%" />
            <StatRow label="Max Drawdown" value="<15%" />
            <StatRow label="Win Rate Target" value=">60%" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Allocation Strategy
          </h3>
          <div className="space-y-3">
            <AllocationRow label="Value Investing" value="40%" color="blue" />
            <AllocationRow
              label="Social Arbitrage"
              value="30%"
              color="green"
            />
            <AllocationRow
              label="Crypto Fundamentals"
              value="20%"
              color="purple"
            />
            <AllocationRow
              label="Opportunistic"
              value="10%"
              color="orange"
            />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Full Trading Dashboard
        </h3>
        <p className="text-gray-600 mb-4">
          Access the complete trading dashboard with live data, signals, and
          18-agent deliberations:
        </p>
        <a
          href="../trading/dashboard.html"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
        >
          Open Trading Dashboard →
        </a>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Recent Signals
        </h3>
        <div className="space-y-4">
          <SignalCard
            ticker="$ASTS"
            conviction={6.8}
            status="YELLOW"
            notes="Waiting for FCC approval + pullback"
          />
          <SignalCard
            ticker="EURUSD (Riz)"
            conviction={8.5}
            status="GREEN"
            notes="Monitoring for next setup"
          />
          <SignalCard
            ticker="$AS"
            conviction={4.2}
            status="RED"
            notes="Correctly avoided - weak fundamentals"
          />
        </div>
      </div>

      <div className="mt-6 text-xs text-gray-500 text-center">
        💡 Data sources: Yieldschool, Dumb Money, Chart Fanatics, DEX Scanners
      </div>
    </div>
  );
}

function StatRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-gray-600">{label}:</span>
      <span className="font-semibold text-gray-900">{value}</span>
    </div>
  );
}

function AllocationRow({
  label,
  value,
  color,
}: {
  label: string;
  value: string;
  color: string;
}) {
  const colorClasses = {
    blue: "bg-blue-200",
    green: "bg-green-200",
    purple: "bg-purple-200",
    orange: "bg-orange-200",
  }[color];

  return (
    <div>
      <div className="flex justify-between mb-1 text-sm">
        <span className="text-gray-700">{label}</span>
        <span className="font-semibold text-gray-900">{value}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`${colorClasses} h-2 rounded-full`}
          style={{ width: value }}
        ></div>
      </div>
    </div>
  );
}

function SignalCard({
  ticker,
  conviction,
  status,
  notes,
}: {
  ticker: string;
  conviction: number;
  status: string;
  notes: string;
}) {
  const statusColors = {
    GREEN: "bg-green-100 text-green-800",
    YELLOW: "bg-yellow-100 text-yellow-800",
    RED: "bg-red-100 text-red-800",
  }[status];

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <div className="font-semibold text-gray-900">{ticker}</div>
        <div className="flex items-center space-x-2">
          <span
            className={`px-2 py-1 rounded text-xs font-semibold ${statusColors}`}
          >
            {status}
          </span>
          <span className="text-sm font-bold text-gray-900">
            {conviction.toFixed(1)}/10
          </span>
        </div>
      </div>
      <p className="text-sm text-gray-600">{notes}</p>
    </div>
  );
}
