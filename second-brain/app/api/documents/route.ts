import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const WORKSPACE = path.resolve(process.cwd(), "..");

export async function GET() {
  try {
    const memoryDir = path.join(WORKSPACE, "memory");
    const files = fs.readdirSync(memoryDir);

    const documents = files
      .filter((file) => file.endsWith(".md"))
      .map((file) => {
        const filePath = path.join(memoryDir, file);
        const stats = fs.statSync(filePath);
        const content = fs.readFileSync(filePath, "utf-8");

        return {
          name: file,
          path: filePath,
          size: stats.size,
          modified: stats.mtime.toISOString(),
          preview: content.slice(0, 200) + "...",
        };
      })
      .sort((a, b) => b.name.localeCompare(a.name)); // Sort by date descending

    return NextResponse.json({ documents });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to read documents" },
      { status: 500 }
    );
  }
}
