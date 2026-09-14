import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { RentPayment, RentSummary } from '../types';

export default function Rent() {
  const [summary, setSummary] = useState<RentSummary | null>(null);
  const [payments, setPayments] = useState<RentPayment[]>([]);

  useEffect(() => {
    Promise.all([api.getRentSummary(), api.getRentPayments()]).then(([s, p]) => {
      setSummary(s);
      setPayments(p);
    }).catch(console.error);
  }, []);

  const statusConfig: Record<string, { bg: string; text: string; dot: string }> = {
    PAID: { bg: 'bg-emerald-50', text: 'text-emerald-700', dot: 'bg-emerald-400' },
    PENDING: { bg: 'bg-amber-50', text: 'text-amber-700', dot: 'bg-amber-400' },
    OVERDUE: { bg: 'bg-red-50', text: 'text-red-700', dot: 'bg-red-400' },
    PARTIAL: { bg: 'bg-orange-50', text: 'text-orange-700', dot: 'bg-orange-400' },
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Rent Management</h1>
        <p className="text-gray-500 mt-1">Track payments and collections</p>
      </div>

      {summary && (
        <div className="grid grid-cols-4 gap-6">
          <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-6 text-white shadow-xl shadow-blue-500/25">
            <div className="text-blue-100 text-sm font-medium">Total Expected</div>
            <div className="text-3xl font-bold mt-2">₹{summary.total_expected.toLocaleString()}</div>
          </div>
          <div className="bg-gradient-to-br from-emerald-500 to-green-600 rounded-2xl p-6 text-white shadow-xl shadow-green-500/25">
            <div className="text-green-100 text-sm font-medium">Collected</div>
            <div className="text-3xl font-bold mt-2">₹{summary.total_paid.toLocaleString()}</div>
            <div className="text-xs text-green-200 mt-1">{summary.paid_count} tenants paid</div>
          </div>
          <div className="bg-gradient-to-br from-amber-500 to-orange-600 rounded-2xl p-6 text-white shadow-xl shadow-orange-500/25">
            <div className="text-orange-100 text-sm font-medium">Pending</div>
            <div className="text-3xl font-bold mt-2">₹{summary.total_pending.toLocaleString()}</div>
            <div className="text-xs text-orange-200 mt-1">{summary.pending_count} tenants</div>
          </div>
          <div className="bg-gradient-to-br from-red-500 to-rose-600 rounded-2xl p-6 text-white shadow-xl shadow-red-500/25">
            <div className="text-red-100 text-sm font-medium">Overdue</div>
            <div className="text-3xl font-bold mt-2">₹{summary.total_overdue.toLocaleString()}</div>
            <div className="text-xs text-red-200 mt-1">{summary.overdue_count} tenants</div>
          </div>
        </div>
      )}

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-100">
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Tenant</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Amount</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Due Date</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Paid Date</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Status</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Method</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {payments.map((p) => {
              const cfg = statusConfig[p.status || ''] || statusConfig.PENDING;
              return (
                <tr key={p.id} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                        {p.tenant?.name?.charAt(0) || '?'}
                      </div>
                      <span className="font-medium text-gray-900">{p.tenant?.name || '-'}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 font-bold text-gray-900">₹{p.amount.toLocaleString()}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{p.due_date}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{p.paid_date || '-'}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${cfg.bg} ${cfg.text}`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot}`}></span>
                      {p.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">{p.payment_method || '-'}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
