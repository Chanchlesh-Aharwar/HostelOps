import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { AgentAction } from '../types';

export default function Activity() {
  const [actions, setActions] = useState<AgentAction[]>([]);

  useEffect(() => {
    api.getAgentActions().then(setActions).catch(console.error);
  }, []);

  const statusConfig: Record<string, { bg: string; text: string; icon: string }> = {
    SUCCESS: { bg: 'bg-green-50', text: 'text-green-700', icon: '✓' },
    FAILED: { bg: 'bg-red-50', text: 'text-red-700', icon: '✕' },
    WAITING_APPROVAL: { bg: 'bg-amber-50', text: 'text-amber-700', icon: '⏳' },
    STARTED: { bg: 'bg-blue-50', text: 'text-blue-700', icon: '●' },
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI Activity Timeline</h1>
        <p className="text-gray-500 mt-1">Chronological log of all agent actions</p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
        {actions.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📋</div>
            <h3 className="text-lg font-bold text-gray-900">No activity yet</h3>
            <p className="text-gray-500 mt-1">Actions will appear here as the agent works</p>
          </div>
        ) : (
          <div className="relative">
            <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-blue-200 via-indigo-200 to-purple-200"></div>
            <div className="space-y-6">
              {actions.map((a) => {
                const cfg = statusConfig[a.status || 'STARTED'] || statusConfig.STARTED;
                return (
                  <div key={a.id} className="relative flex items-start gap-4 pl-2">
                    <div className={`relative z-10 w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
                      a.status === 'SUCCESS' ? 'bg-green-100 text-green-600' :
                      a.status === 'WAITING_APPROVAL' ? 'bg-amber-100 text-amber-600' :
                      a.status === 'FAILED' ? 'bg-red-100 text-red-600' :
                      'bg-blue-100 text-blue-600'
                    }`}>
                      {cfg.icon}
                    </div>
                    <div className="flex-1 bg-gray-50 rounded-xl p-4 hover:bg-gray-100 transition-colors">
                      <div className="flex items-center justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono text-gray-400">{a.created_at?.slice(11, 16)}</span>
                          <span className="text-xs bg-gray-200 text-gray-600 px-2 py-0.5 rounded font-mono">{a.agent_name}</span>
                          <span className="text-sm font-bold text-gray-900">{a.action_type}</span>
                        </div>
                        <span className={`text-xs px-3 py-1 rounded-full font-medium ${cfg.bg} ${cfg.text}`}>
                          {a.status}
                        </span>
                      </div>
                      {a.entity_type && (
                        <div className="text-xs text-gray-500">
                          Entity: {a.entity_type} #{a.entity_id}
                        </div>
                      )}
                      {a.output_data && (
                        <div className="mt-2 text-xs bg-white rounded-lg p-2 border border-gray-100 font-mono text-gray-600">
                          {JSON.stringify(a.output_data).slice(0, 120)}...
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
