import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Complaint } from '../types';

export default function Complaints() {
  const [complaints, setComplaints] = useState<Complaint[]>([]);

  useEffect(() => {
    api.getComplaints().then(setComplaints).catch(console.error);
  }, []);

  const statusConfig: Record<string, { bg: string; text: string; icon: string }> = {
    OPEN: { bg: 'bg-blue-50', text: 'text-blue-700', icon: '🔵' },
    ANALYZING: { bg: 'bg-purple-50', text: 'text-purple-700', icon: '🔍' },
    VENDOR_SEARCH: { bg: 'bg-indigo-50', text: 'text-indigo-700', icon: '🔎' },
    AWAITING_APPROVAL: { bg: 'bg-amber-50', text: 'text-amber-700', icon: '⏳' },
    VENDOR_ASSIGNED: { bg: 'bg-green-50', text: 'text-green-700', icon: '✅' },
    IN_PROGRESS: { bg: 'bg-orange-50', text: 'text-orange-700', icon: '🔧' },
    RESOLVED: { bg: 'bg-emerald-50', text: 'text-emerald-700', icon: '✔️' },
    CLOSED: { bg: 'bg-gray-50', text: 'text-gray-600', icon: '📁' },
  };

  const priorityConfig: Record<string, { bg: string; text: string }> = {
    LOW: { bg: 'bg-slate-100', text: 'text-slate-600' },
    MEDIUM: { bg: 'bg-amber-100', text: 'text-amber-700' },
    HIGH: { bg: 'bg-orange-100', text: 'text-orange-700' },
    URGENT: { bg: 'bg-red-100', text: 'text-red-700' },
  };

  const categoryIcons: Record<string, string> = {
    PLUMBING: '🚿', ELECTRICAL: '⚡', AC: '❄️', CLEANING: '🧹',
    FURNITURE: '🪑', INTERNET: '🌐', APPLIANCE: '🔌', SECURITY: '🔒', OTHER: '📋',
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Complaints</h1>
        <p className="text-gray-500 mt-1">{complaints.length} total complaints</p>
      </div>

      <div className="space-y-4">
        {complaints.map((c) => {
          const sCfg = statusConfig[c.status || 'OPEN'] || statusConfig.OPEN;
          const pCfg = priorityConfig[c.priority || 'MEDIUM'] || priorityConfig.MEDIUM;
          return (
            <div key={c.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className="text-3xl">{categoryIcons[c.category || 'OTHER']}</div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs text-gray-400 font-mono">#{c.id}</span>
                      <h3 className="font-bold text-gray-900">{c.title}</h3>
                    </div>
                    <p className="text-sm text-gray-500 line-clamp-1">{c.description}</p>
                    <div className="flex items-center gap-3 mt-2 text-xs text-gray-400">
                      <span>👤 {c.tenant?.name || 'Unknown'}</span>
                      <span>•</span>
                      <span>🚪 Room {c.room?.room_number || '-'}</span>
                      <span>•</span>
                      <span>📁 {c.source}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${pCfg.bg} ${pCfg.text}`}>
                    {c.priority}
                  </span>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${sCfg.bg} ${sCfg.text}`}>
                    {sCfg.icon} {c.status?.replace('_', ' ')}
                  </span>
                </div>
              </div>
              {c.ai_analysis && (
                <div className="mt-4 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
                  <div className="text-xs font-semibold text-blue-700 mb-1">🤖 AI Analysis</div>
                  <div className="text-sm text-blue-600">
                    Category: {String(c.ai_analysis.category)} • Confidence: {Math.round(((c.ai_analysis.confidence as number) || 0) * 100)}%
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
