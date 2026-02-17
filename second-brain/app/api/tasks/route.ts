import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const WORKSPACE = path.resolve(process.cwd(), "..");

interface Task {
  text: string;
  source: string;
  completed: boolean;
}

export async function GET() {
  try {
    const tasks: Task[] = [];

    // Extract from HEARTBEAT.md
    const heartbeatPath = path.join(WORKSPACE, "HEARTBEAT.md");
    if (fs.existsSync(heartbeatPath)) {
      const content = fs.readFileSync(heartbeatPath, "utf-8");
      const lines = content.split("\n");
      lines.forEach((line) => {
        if (line.includes("When to run:") || line.includes("When to check:")) {
          // Extract check times
          const match = line.match(/\d{1,2}\s*(AM|PM)/gi);
          if (match) {
            match.forEach((time) => {
              tasks.push({
                text: `Check at ${time}`,
                source: "HEARTBEAT.md",
                completed: false,
              });
            });
          }
        }
      });
    }

    // Extract from MEMORY.md
    const memoryPath = path.join(WORKSPACE, "MEMORY.md");
    if (fs.existsSync(memoryPath)) {
      const content = fs.readFileSync(memoryPath, "utf-8");
      const lines = content.split("\n");
      lines.forEach((line) => {
        if (line.includes("TODO") || line.includes("[ ]")) {
          tasks.push({
            text: line.replace(/[-*]\s*\[([ x])\]/, "").trim(),
            source: "MEMORY.md",
            completed: line.includes("[x]"),
          });
        }
      });
    }

    // Extract from today's memory file
    const today = new Date().toISOString().split("T")[0];
    const todayPath = path.join(WORKSPACE, "memory", `${today}.md`);
    if (fs.existsSync(todayPath)) {
      const content = fs.readFileSync(todayPath, "utf-8");
      const lines = content.split("\n");
      lines.forEach((line) => {
        if (line.includes("TODO") || line.includes("[ ]")) {
          tasks.push({
            text: line.replace(/[-*]\s*\[([ x])\]/, "").trim(),
            source: `memory/${today}.md`,
            completed: line.includes("[x]"),
          });
        }
      });
    }

    // Add some hardcoded tasks from MEMORY.md context
    tasks.push(
      {
        text: "Run social arb scan (9 AM daily)",
        source: "HEARTBEAT.md",
        completed: false,
      },
      {
        text: "Check Simmer weather opportunities (9 AM, 1 PM, 7 PM)",
        source: "HEARTBEAT.md",
        completed: false,
      },
      {
        text: "Monitor Phase 1 paper trading (target: >20% returns, <15% drawdown)",
        source: "MEMORY.md",
        completed: false,
      },
      {
        text: "Review 18-agent deliberation logs",
        source: "Daily Routine",
        completed: false,
      }
    );

    return NextResponse.json({ tasks });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to extract tasks" },
      { status: 500 }
    );
  }
}
