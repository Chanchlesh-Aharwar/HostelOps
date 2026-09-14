import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { DashboardStats } from '../types';

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  const load = () => {
    api.getDashboard().then(setStats).catch(console.error);
    setLastRefresh(new Date());
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 10000);
    return () => clearInterval(interval);
  }, []);

  if (!stats) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
    </div>
  );

  const occupancyRate = stats.total_rooms > 0 ? Math.round((stats.occupied_rooms / stats.total_rooms) * 100) : 0;
  const collectionRate = stats.total_expected_rent > 0 ? Math.round(((stats.total_expected_rent - stats.total_pending_rent) / stats.total_expected_rent) * 100) : 0;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">Welcome back, Rahul. Here's your hostel overview.</p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          Live • Last updated {lastRefresh.toLocaleTimeString()}
        </div>
      </div>

      {/* Hero Stats */}
      <div className="grid grid-cols-4 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-xl shadow-blue-500/25 hover:scale-105 transition-transform">
          <div className="text-blue-100 text-sm font-medium">Total Rooms</div>
          <div className="text-4xl font-bold mt-2">{stats.total_rooms}</div>
          <div className="mt-3 flex items-center gap-2">
            <div className="h-2 flex-1 bg-white/20 rounded-full overflow-hidden">
              <div className="h-full bg-white rounded-full" style={{ width: `${occupancyRate}%` }}></div>
            </div>
            <span className="text-xs text-blue-100">{occupancyRate}% occupied</span>
          </div>
        </div>

        <div className="bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl p-6 text-white shadow-xl shadow-green-500/25 hover:scale-105 transition-transform">
          <div className="text-green-100 text-sm font-medium">Active Tenants</div>
          <div className="text-4xl font-bold mt-2">{stats.total_tenants}</div>
          <div className="mt-3 text-xs text-green-100">
            {stats.occupied_rooms} rooms occupied • {stats.vacant_rooms} vacant
          </div>
        </div>

        <div className="bg-gradient-to-br from-amber-500 to-orange-600 rounded-2xl p-6 text-white shadow-xl shadow-orange-500/25 hover:scale-105 transition-transform">
          <div className="text-orange-100 text-sm font-medium">Pending Rent</div>
          <div className="text-4xl font-bold mt-2">₹{(stats.total_pending_rent / 1000).toFixed(0)}K</div>
          <div className="mt-3 flex items-center gap-2">
            <div className="h-2 flex-1 bg-white/20 rounded-full overflow-hidden">
              <div className="h-full bg-white rounded-full" style={{ width: `${collectionRate}%` }}></div>
            </div>
            <span className="text-xs text-orange-100">{collectionRate}% collected</span>
          </div>
        </div>

        <div className="bg-gradient-to-br from-red-500 to-rose-600 rounded-2xl p-6 text-white shadow-xl shadow-red-500/25 hover:scale-105 transition-transform">
          <div className="text-red-100 text-sm font-medium">Open Complaints</div>
          <div className="text-4xl font-bold mt-2">{stats.open_complaints}</div>
          <div className="mt-3 text-xs text-red-100">
            {stats.active_maintenance_jobs} active jobs • {stats.pending_approvals} pending approvals
          </div>
        </div>
      </div>

      {/* Secondary Stats */}
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center text-2xl">🛠</div>
            <div>
              <div className="text-sm text-gray-500">Maintenance Jobs</div>
              <div className="text-2xl font-bold text-gray-900">{stats.active_maintenance_jobs}</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center text-2xl">⏳</div>
            <div>
              <div className="text-sm text-gray-500">Pending Approvals</div>
              <div className="text-2xl font-bold text-gray-900">{stats.pending_approvals}</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center text-2xl">💰</div>
            <div>
              <div className="text-sm text-gray-500">Total Expected Rent</div>
              <div className="text-2xl font-bold text-gray-900">₹{stats.total_expected_rent.toLocaleString()}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent AI Actions */}
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-gray-900">Recent AI Actions</h2>
            <p className="text-sm text-gray-500">Agent activity timeline</p>
          </div>
          <span className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium">
            {stats.recent_agent_actions.length} actions
          </span>
        </div>
        <div className="divide-y divide-gray-50">
          {stats.recent_agent_actions.length === 0 ? (
            <div className="px-6 py-12 text-center text-gray-400">
              <div className="text-4xl mb-2">🤖</div>
              <p>No AI actions yet. Send a complaint to see the agent in action.</p>
            </div>
          ) : (
            stats.recent_agent_actions.map((action) => (
              <div key={action.id} className="px-6 py-4 flex items-center gap-4 hover:bg-gray-50 transition-colors">
                <div className={`w-2 h-2 rounded-full ${
                  action.status === 'SUCCESS' ? 'bg-green-400' :
                  action.status === 'WAITING_APPROVAL' ? 'bg-yellow-400' :
                  action.status === 'FAILED' ? 'bg-red-400' : 'bg-blue-400'
                }`}></div>
                <span className="text-xs text-gray-400 w-16 font-mono">
                  {action.created_at?.slice(11, 16)}
                </span>
                <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded font-mono">
                  {action.agent_name}
                </span>
                <span className="text-sm font-medium text-gray-700">{action.action_type}</span>
                {action.entity_type && (
                  <span className="text-xs text-gray-400">
                    → {action.entity_type} #{action.entity_id}
                  </span>
                )}
                <span className={`ml-auto text-xs px-3 py-1 rounded-full font-medium ${
                  action.status === 'SUCCESS' ? 'bg-green-100 text-green-700' :
                  action.status === 'WAITING_APPROVAL' ? 'bg-yellow-100 text-yellow-700' :
                  action.status === 'FAILED' ? 'bg-red-100 text-red-700' :
                  'bg-blue-100 text-blue-700'
                }`}>
                  {action.status}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
