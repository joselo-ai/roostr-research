import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "roostr Capital - Mission Control",
  description: "Autonomous AI hedge fund that compounds capital 24/7",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
