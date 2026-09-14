import { useState } from 'react';

export default function RentAutomation() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState('');

  const callEndpoint = async (endpoint: string, label: string) => {
    setLoading(label);
    try {
      const res = await fetch(`/api/rent/auto/${endpoint}`, { method: 'POST' });
      const data = await res.json();
      setResult({ action: label, ...data });
    } catch (err) {
      setResult({ action: label, error: (err as Error).message });
    }
    setLoading('');
  };

  const actions = [
    { endpoint: 'generate', label: 'Generate Monthly Rent', icon: '📄', color: 'from-blue-500 to-indigo-600', shadow: 'shadow-blue-500/25', desc: 'Create rent records for all active tenants' },
    { endpoint: 'mark-overdue', label: 'Mark Overdue', icon: '⚠️', color: 'from-red-500 to-rose-600', shadow: 'shadow-red-500/25', desc: 'Mark overdue rent payments automatically' },
    { endpoint: 'send-reminders', label: 'Send Reminders', icon: '📧', color: 'from-green-500 to-emerald-600', shadow: 'shadow-green-500/25', desc: 'Send rent reminders to tenants' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Rent Automation</h1>
        <p className="text-gray-500 mt-1">Automate rent generation, reminders, and overdue tracking</p>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {actions.map((a) => (
          <button
            key={a.endpoint}
            onClick={() => callEndpoint(a.endpoint, a.label)}
            disabled={!!loading}
            className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-left hover:shadow-lg hover:-translate-y-1 transition-all duration-200 disabled:opacity-50"
          >
            <div className={`w-16 h-16 bg-gradient-to-br ${a.color} rounded-2xl flex items-center justify-center text-3xl text-white shadow-xl ${a.shadow} mb-4`}>
              {a.icon}
            </div>
            <h3 className="font-bold text-gray-900 text-lg">{a.label}</h3>
            <p className="text-sm text-gray-500 mt-1">{a.desc}</p>
          </button>
        ))}
      </div>

      {loading && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 text-center">
          <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-500">Running {loading}...</p>
        </div>
      )}

      {result && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100 bg-gray-50">
            <h3 className="font-bold text-gray-900">Result: {result.action}</h3>
          </div>
          <div className="p-6">
            <pre className="text-sm bg-gray-50 p-4 rounded-xl overflow-auto font-mono text-gray-700">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
