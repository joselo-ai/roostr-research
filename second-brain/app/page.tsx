import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to 2nd Brain Dashboard
        </h1>
        <p className="text-lg text-gray-600">
          Your central hub for memories, tasks, and trading intelligence
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <DashboardCard
          title="Memories"
          description="View and edit long-term memory (MEMORY.md)"
          href="/memories"
          icon="🧠"
        />
        <DashboardCard
          title="Documents"
          description="Browse daily memory files in timeline view"
          href="/documents"
          icon="📄"
        />
        <DashboardCard
          title="Tasks"
          description="Aggregated task list from all sources"
          href="/tasks"
          icon="✅"
        />
        <DashboardCard
          title="Trading Signals"
          description="18-agent deliberations and conviction scores"
          href="/trading"
          icon="📊"
        />
        <DashboardCard
          title="Daily Logs"
          description="Recent activity and session notes"
          href="/logs"
          icon="📋"
        />
        <DashboardCard
          title="Search"
          description="Search across all memory files"
          href="/search"
          icon="🔍"
        />
      </div>

      <div className="bg-white rounded-lg shadow p-6 mt-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Quick Stats
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <StatItem label="Memory Files" value="13" />
          <StatItem label="Active Tasks" value="8" />
          <StatItem label="Trading Signals" value="5" />
          <StatItem label="Last Updated" value="Today" />
        </div>
      </div>
    </div>
  );
}

function DashboardCard({
  title,
  description,
  href,
  icon,
}: {
  title: string;
  description: string;
  href: string;
  icon: string;
}) {
  return (
    <Link
      href={href}
      className="block bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6"
    >
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </Link>
  );
}

function StatItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-center">
      <div className="text-2xl font-bold text-gray-900">{value}</div>
      <div className="text-sm text-gray-600">{label}</div>
    </div>
  );
}
