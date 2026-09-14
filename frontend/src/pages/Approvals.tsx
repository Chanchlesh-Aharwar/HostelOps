import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Approval } from '../types';

export default function Approvals() {
  const [approvals, setApprovals] = useState<Approval[]>([]);

  const load = () => api.getApprovals().then(setApprovals).catch(console.error);
  useEffect(() => { load(); }, []);

  const handleApprove = async (id: number) => {
    await api.approveAction(id, 'Approved by owner');
    load();
  };

  const handleReject = async (id: number) => {
    await api.rejectAction(id, 'Rejected by owner');
    load();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Pending Approvals</h1>
        <p className="text-gray-500 mt-1">{approvals.length} actions awaiting your decision</p>
      </div>

      {approvals.length === 0 ? (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 text-center">
          <div className="text-6xl mb-4">✅</div>
          <h3 className="text-lg font-bold text-gray-900">All caught up!</h3>
          <p className="text-gray-500 mt-1">No pending approvals right now.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {approvals.map((a) => (
            <div key={a.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow">
              <div className="h-1 bg-gradient-to-r from-amber-400 to-orange-500"></div>
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-gradient-to-br from-amber-400 to-orange-500 rounded-xl flex items-center justify-center text-2xl text-white">
                      ⏳
                    </div>
                    <div>
                      <span className="text-xs bg-amber-100 text-amber-700 px-3 py-1 rounded-full font-medium">
                        {a.action_type.replace('_', ' ')}
                      </span>
                      <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full ml-2">
                        {a.entity_type} #{a.entity_id}
                      </span>
                    </div>
                  </div>
                  <span className="text-xs text-gray-400">
                    {a.created_at?.slice(0, 16).replace('T', ' ')}
                  </span>
                </div>

                <p className="text-gray-700 mb-6 leading-relaxed">{a.reason}</p>

                <div className="flex gap-3">
                  <button
                    onClick={() => handleApprove(a.id)}
                    className="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-medium hover:from-green-600 hover:to-emerald-700 transition-all shadow-lg shadow-green-500/25 hover:shadow-xl hover:shadow-green-500/30"
                  >
                    ✓ Approve
                  </button>
                  <button
                    onClick={() => handleReject(a.id)}
                    className="flex-1 px-6 py-3 bg-gradient-to-r from-red-500 to-rose-600 text-white rounded-xl font-medium hover:from-red-600 hover:to-rose-700 transition-all shadow-lg shadow-red-500/25 hover:shadow-xl hover:shadow-red-500/30"
                  >
                    ✕ Reject
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
