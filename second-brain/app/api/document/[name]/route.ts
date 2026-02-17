import { NextResponse } from "next/server";
import fs from "fs";
import path from "path";

const WORKSPACE = path.resolve(process.cwd(), "../..");

export async function GET(
  request: Request,
  { params }: { params: Promise<{ name: string }> }
) {
  try {
    const { name } = await params;
    const filePath = path.join(WORKSPACE, "memory", name);
    const content = fs.readFileSync(filePath, "utf-8");
    return NextResponse.json({ content, name });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to read document" },
      { status: 500 }
    );
  }
}
