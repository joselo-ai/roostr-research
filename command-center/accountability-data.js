// Accountability Dashboard Data Aggregation
// Auto-generated on 2026-02-08 22:20:23

window.AccountabilityData = {
  "decisions": [
    {
      "time": "20:32 EST",
      "icon": "\ud83c\udfaf",
      "title": "DEPLOYMENT DECISION",
      "severity": "critical",
      "details": [
        "What: Deploy $45k Monday 9:30 AM (3 stocks)",
        "Why: ALL scored 10/10 (highest ever), replaced ACGL (8.5/10)",
        "Alternatives: Original plan (ACGL $12k, KTB $10k = $22k)",
        "Confidence: 9/10",
        "Approved: YES (G confirmed \"Ok\")",
        "Outcome: Pending (executes Monday)"
      ]
    }
  ],
  "cost": {
    "tokensUsed": 30500,
    "tokensPct": 15,
    "costToday": 0.09,
    "budgetPct": 1,
    "byAgent": [
      {
        "name": "Main (Joselo)",
        "tokens": 9150,
        "cost": 0.03
      },
      {
        "name": "Subagents",
        "tokens": 15250,
        "cost": 0.05
      },
      {
        "name": "Cron Jobs",
        "tokens": 6100,
        "cost": 0.02
      }
    ],
    "warnings": [
      "Monitor token usage to stay under $5/day budget"
    ]
  },
  "autonomousActions": [],
  "approvalQueue": [
    {
      "priority": "MEDIUM",
      "icon": "\ud83d\udfe1",
      "title": "Set up Stripe for signal feed",
      "status": "AWAITING APPROVAL",
      "details": [
        "Revenue: $99-999/mo potential",
        "Time: 2 hours",
        "Risk: Low (standard integration)"
      ],
      "buttons": [
        {
          "text": "Approve",
          "class": "btn-approve"
        },
        {
          "text": "Reject",
          "class": "btn-reject"
        },
        {
          "text": "More Info",
          "class": "btn-info"
        }
      ]
    }
  ],
  "risks": [
    {
      "severity": "medium",
      "title": "Token Budget Risk",
      "details": [
        "Current usage: 30,500 tokens",
        "Cost: $0.09",
        "Monitor to stay under daily limit"
      ]
    }
  ],
  "auditTrail": [
    {
      "time": "16:20",
      "category": "trading",
      "action": "Portfolio initialized",
      "user": "main",
      "details": "Status: success | {\"deployed\": \",500\", \"positions\": 2}"
    },
    {
      "time": "16:20",
      "category": "trading",
      "action": "TAO position opened",
      "user": "main",
      "details": "Status: success | {\"entry\": \".05\", \"qty\": 56.8, \"risk\": \",408\"}"
    },
    {
      "time": "16:20",
      "category": "trading",
      "action": "SOL position opened",
      "user": "main",
      "details": "Status: success | {\"entry\": \".51\", \"qty\": 86.7, \"risk\": \"\"}"
    },
    {
      "time": "16:20",
      "category": "marketing",
      "action": "Twitter thread complete",
      "user": "main",
      "details": "Status: success | {\"tweets\": 8, \"url\": \"https://x.com/roostrcapital\"}"
    },
    {
      "time": "16:20",
      "category": "marketing",
      "action": "Automation deployed",
      "user": "main",
      "details": "Status: success | {\"frequency\": \"4x daily\", \"crons\": 4}"
    },
    {
      "time": "16:20",
      "category": "research",
      "action": "ACGL conviction doc",
      "user": "main",
      "details": "Status: success | {\"rating\": \"8.5/10\", \"words\": 17000, \"deploy\": \"k\"}"
    },
    {
      "time": "16:20",
      "category": "research",
      "action": "KTB conviction doc",
      "user": "main",
      "details": "Status: success | {\"rating\": \"7.5/10\", \"words\": 15000, \"deploy\": \"k\"}"
    },
    {
      "time": "16:20",
      "category": "automation",
      "action": "Price updater deployed",
      "user": "main",
      "details": "Status: success | {\"frequency\": \"every 5min\", \"status\": \"active\"}"
    },
    {
      "time": "16:20",
      "category": "automation",
      "action": "Signal scraper deployed",
      "user": "main",
      "details": "Status: success | {\"frequency\": \"every 6h\", \"status\": \"active\"}"
    },
    {
      "time": "16:20",
      "category": "automation",
      "action": "Daily summary deployed",
      "user": "main",
      "details": "Status: success | {\"frequency\": \"daily 8AM\", \"status\": \"active\"}"
    },
    {
      "time": "16:20",
      "category": "decision",
      "action": "Strategic pivot",
      "user": "main",
      "details": "Status: success | {\"from\": \"Riz EURUSD (40%)\", \"to\": \"Value Stocks (40%)\", \"reason\": \"Constant deal flow\"}"
    },
    {
      "time": "16:20",
      "category": "decision",
      "action": "Allocation finalized",
      "user": "main",
      "details": "Status: success | {\"buckets\": 4, \"total\": \"k\", \"phase\": \"Phase 1\"}"
    },
    {
      "time": "16:20",
      "category": "decision",
      "action": "GitHub repo public",
      "user": "main",
      "details": "Status: success | {\"url\": \"https://github.com/joselo-ai/roostr-research\", \"visibility\": \"public\"}"
    },
    {
      "time": "16:20",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 165.83, \"SOL\": 87.12, \"P&L\": -527.6089999999986}"
    },
    {
      "time": "16:21",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 165.97, \"SOL\": 87.13, \"P&L\": -518.79}"
    },
    {
      "time": "16:23",
      "category": "trading",
      "action": "Crypto tracker initialized",
      "user": "main",
      "details": "Status: success | {\"coins\": [\"NANO\", \"BAN\", \"TAO\", \"SOL\"], \"refresh\": \"30s\"}"
    },
    {
      "time": "16:27",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 165.42, \"SOL\": 87.19, \"P&L\": -544.8280000000013}"
    },
    {
      "time": "16:59",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.44, \"SOL\": 86.47, \"P&L\": -719.7159999999994}"
    },
    {
      "time": "17:02",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.63, \"SOL\": 86.5, \"P&L\": -706.3230000000003}"
    },
    {
      "time": "17:06",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.98, \"SOL\": 86.6, \"P&L\": -677.773000000002}"
    },
    {
      "time": "17:15",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 164.06, \"SOL\": 86.78, \"P&L\": -657.6229999999996}"
    },
    {
      "time": "17:25",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.88, \"SOL\": 86.93, \"P&L\": -654.8419999999987}"
    },
    {
      "time": "17:31",
      "category": "decision",
      "action": "Command Center upgraded",
      "user": "main",
      "details": "Status: success | {\"new_sections\": [\"Today Scorecard\", \"Achievements\", \"Opportunities\", \"Goals Progress\"], \"purpose\": \"Daily review sessions with G\", \"features\": [\"Live P&L\", \"Actions completed\", \"Goal tracking\", \"Opportunity pipeline\"]}"
    },
    {
      "time": "17:51",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.51, \"SOL\": 86.87, \"P&L\": -681.0600000000004}"
    },
    {
      "time": "20:55",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.86, \"SOL\": 86.28, \"P&L\": -712.3329999999996}"
    },
    {
      "time": "21:00",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.92, \"SOL\": 86.33, \"P&L\": -704.590000000001}"
    },
    {
      "time": "21:05",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.56, \"SOL\": 86.33, \"P&L\": -725.0379999999996}"
    },
    {
      "time": "21:10",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.37, \"SOL\": 86.42, \"P&L\": -728.027}"
    },
    {
      "time": "21:15",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.02, \"SOL\": 86.48, \"P&L\": -742.704999999999}"
    },
    {
      "time": "21:20",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.18, \"SOL\": 86.48, \"P&L\": -733.6169999999993}"
    },
    {
      "time": "21:25",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.05, \"SOL\": 86.54, \"P&L\": -735.7989999999991}"
    },
    {
      "time": "21:30",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.29, \"SOL\": 86.55, \"P&L\": -721.3000000000002}"
    },
    {
      "time": "21:35",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.71, \"SOL\": 86.61, \"P&L\": -692.2420000000002}"
    },
    {
      "time": "21:40",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 163.59, \"SOL\": 86.7, \"P&L\": -691.2549999999992}"
    },
    {
      "time": "21:45",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 164.51, \"SOL\": 87.11, \"P&L\": -603.4520000000002}"
    },
    {
      "time": "21:50",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 165.16, \"SOL\": 87.23, \"P&L\": -556.1279999999997}"
    },
    {
      "time": "21:55",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 164.87, \"SOL\": 87.27, \"P&L\": -569.1319999999996}"
    },
    {
      "time": "22:00",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 164.61, \"SOL\": 87.14, \"P&L\": -595.1709999999994}"
    },
    {
      "time": "22:10",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 164.58, \"SOL\": 87.04, \"P&L\": -605.5449999999992}"
    },
    {
      "time": "22:15",
      "category": "trading",
      "action": "Price update",
      "user": "main",
      "details": "Status: success | {\"TAO\": 164.62, \"SOL\": 86.94, \"P&L\": -611.9430000000002}"
    }
  ]
};

// Helper function to calculate real-time token costs
function updateRealTimeCosts() {
    console.log('Real-time cost update triggered');
}

// Calculate token costs based on model pricing
function calculateCost(tokens, model = 'claude-sonnet-4') {
    const inputPricePerMillion = 3.00;
    const outputPricePerMillion = 15.00;
    
    const inputTokens = tokens * 0.7;
    const outputTokens = tokens * 0.3;
    
    const inputCost = (inputTokens / 1000000) * inputPricePerMillion;
    const outputCost = (outputTokens / 1000000) * outputPricePerMillion;
    
    return inputCost + outputCost;
}

// Auto-update costs every 10 seconds
setInterval(updateRealTimeCosts, 10000);
