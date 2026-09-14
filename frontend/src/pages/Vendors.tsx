import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Vendor } from '../types';

export default function Vendors() {
  const [vendors, setVendors] = useState<Vendor[]>([]);

  useEffect(() => {
    api.getVendors().then(setVendors).catch(console.error);
  }, []);

  const availabilityConfig: Record<string, { bg: string; text: string; dot: string }> = {
    AVAILABLE: { bg: 'bg-emerald-50', text: 'text-emerald-700', dot: 'bg-emerald-400' },
    BUSY: { bg: 'bg-amber-50', text: 'text-amber-700', dot: 'bg-amber-400' },
    UNAVAILABLE: { bg: 'bg-red-50', text: 'text-red-700', dot: 'bg-red-400' },
  };

  const categoryColors: Record<string, string> = {
    PLUMBING: 'from-blue-400 to-blue-600',
    ELECTRICAL: 'from-yellow-400 to-amber-500',
    AC: 'from-cyan-400 to-blue-500',
    CLEANING: 'from-green-400 to-emerald-500',
    CARPENTRY: 'from-amber-400 to-orange-500',
    GENERAL: 'from-gray-400 to-gray-600',
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Vendors</h1>
        <p className="text-gray-500 mt-1">{vendors.length} active service providers</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {vendors.map((v) => {
          const aCfg = availabilityConfig[v.availability] || availabilityConfig.AVAILABLE;
          const gradient = categoryColors[v.category] || 'from-gray-400 to-gray-600';
          const successRate = v.total_jobs > 0 ? Math.round((v.successful_jobs / v.total_jobs) * 100) : 0;

          return (
            <div key={v.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg transition-all duration-200">
              <div className={`h-2 bg-gradient-to-r ${gradient}`}></div>
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{v.name}</h3>
                    <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{v.category}</span>
                  </div>
                  <span className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${aCfg.bg} ${aCfg.text}`}>
                    <span className={`w-1.5 h-1.5 rounded-full ${aCfg.dot}`}></span>
                    {v.availability}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-xl p-3">
                    <div className="text-xs text-amber-600 font-medium">Rating</div>
                    <div className="flex items-center gap-1 mt-1">
                      <span className="text-lg font-bold text-amber-600">⭐ {v.rating}</span>
                      <span className="text-xs text-amber-500">/5</span>
                    </div>
                  </div>
                  <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-3">
                    <div className="text-xs text-green-600 font-medium">Avg Cost</div>
                    <div className="text-lg font-bold text-green-600 mt-1">₹{v.average_cost}</div>
                  </div>
                </div>

                <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                  <span>📍 {v.service_area}</span>
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <div className="text-xs text-gray-400">
                    {v.total_jobs} jobs • {successRate}% success
                  </div>
                  <div className="text-xs text-gray-400">📞 {v.phone}</div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
