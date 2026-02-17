"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navigation() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Dashboard" },
    { href: "/memories", label: "Memories" },
    { href: "/documents", label: "Documents" },
    { href: "/tasks", label: "Tasks" },
    { href: "/trading", label: "Trading Signals" },
    { href: "/logs", label: "Daily Logs" },
  ];

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex space-x-8">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-gray-900">🧠</span>
              <span className="ml-2 text-xl font-semibold text-gray-900">
                2nd Brain
              </span>
            </div>
            <div className="hidden sm:flex sm:space-x-4 sm:items-center">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    pathname === link.href
                      ? "bg-gray-900 text-white"
                      : "text-gray-700 hover:bg-gray-100"
                  }`}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
