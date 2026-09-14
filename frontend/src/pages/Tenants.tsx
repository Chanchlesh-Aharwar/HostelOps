import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Tenant, Room } from '../types';

interface FormData {
  name: string;
  phone: string;
  email: string;
  room_id: string;
  emergency_contact_name: string;
  emergency_contact_phone: string;
  rent_due_day: number;
}

const emptyForm: FormData = {
  name: '', phone: '', email: '', room_id: '',
  emergency_contact_name: '', emergency_contact_phone: '', rent_due_day: 5,
};

export default function Tenants() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const load = () => {
    api.getTenants().then(setTenants).catch(console.error);
    api.getRooms().then(setRooms).catch(console.error);
  };

  useEffect(() => { load(); }, []);

  const openAdd = () => {
    setForm(emptyForm);
    setEditingId(null);
    setError('');
    setShowModal(true);
  };

  const openEdit = (t: Tenant) => {
    setForm({
      name: t.name,
      phone: t.phone,
      email: t.email || '',
      room_id: t.room_id?.toString() || '',
      emergency_contact_name: t.emergency_contact_name || '',
      emergency_contact_phone: t.emergency_contact_phone || '',
      rent_due_day: t.rent_due_day || 5,
    });
    setEditingId(t.id);
    setError('');
    setShowModal(true);
  };

  const handleSubmit = async () => {
    if (!form.name || !form.phone) {
      setError('Name and phone are required');
      return;
    }
    setLoading(true);
    try {
      const data = {
        ...form,
        room_id: form.room_id ? parseInt(form.room_id) : null,
      };
      if (editingId) {
        await api.updateTenant(editingId, data);
      } else {
        await api.createTenant(data);
      }
      setShowModal(false);
      load();
    } catch (err) {
      setError((err as Error).message);
    }
    setLoading(false);
  };

  const handleDelete = async (id: number, name: string) => {
    if (!confirm(`Deactivate tenant "${name}"?`)) return;
    try {
      await api.deleteTenant(id);
      load();
    } catch (err) {
      alert((err as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tenants</h1>
          <p className="text-gray-500 mt-1">{tenants.length} active tenants</p>
        </div>
        <button onClick={openAdd} className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25">
          + Add Tenant
        </button>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-100">
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Tenant</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Contact</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Room</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Rent</th>
              <th className="text-left px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Status</th>
              <th className="text-right px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {tenants.map((t) => (
              <tr key={t.id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      {t.name.charAt(0)}
                    </div>
                    <div>
                      <div className="font-semibold text-gray-900">{t.name}</div>
                      <div className="text-xs text-gray-400">ID: #{t.id}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-700">{t.phone}</div>
                  <div className="text-xs text-gray-400">{t.email || '-'}</div>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm font-bold text-gray-900">{t.room?.room_number || '-'}</span>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm font-bold text-gray-900">₹{t.room?.rent_amount?.toLocaleString() || '-'}</span>
                </td>
                <td className="px-6 py-4">
                  <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${
                    t.status === 'ACTIVE' ? 'bg-emerald-50 text-emerald-700' : 'bg-gray-100 text-gray-600'
                  }`}>
                    <span className={`w-1.5 h-1.5 rounded-full ${t.status === 'ACTIVE' ? 'bg-emerald-400' : 'bg-gray-400'}`}></span>
                    {t.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex items-center justify-end gap-2">
                    <button onClick={() => openEdit(t)} className="px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-xs font-medium hover:bg-blue-100 transition">
                      Edit
                    </button>
                    <button onClick={() => handleDelete(t.id, t.name)} className="px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100 transition">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              {editingId ? 'Edit Tenant' : 'Add New Tenant'}
            </h2>

            {error && (
              <div className="bg-red-50 text-red-700 p-3 rounded-xl text-sm mb-4">{error}</div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <label className="text-xs text-gray-500 font-medium">Full Name *</label>
                <input type="text" value={form.name} onChange={e => setForm({...form, name: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="Amit Verma" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Phone *</label>
                <input type="text" value={form.phone} onChange={e => setForm({...form, phone: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="9800000001" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Email</label>
                <input type="email" value={form.email} onChange={e => setForm({...form, email: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="amit@email.com" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Assign Room</label>
                <select value={form.room_id} onChange={e => setForm({...form, room_id: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="">No room</option>
                  {rooms.filter(r => r.status === 'VACANT' || r.status === 'PARTIALLY_OCCUPIED' || (editingId && r.id.toString() === form.room_id)).map(r => (
                    <option key={r.id} value={r.id}>{r.room_number} - Floor {r.floor} ({r.status})</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Rent Due Day</label>
                <input type="number" value={form.rent_due_day} onChange={e => setForm({...form, rent_due_day: parseInt(e.target.value) || 5})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" min="1" max="28" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Emergency Contact Name</label>
                <input type="text" value={form.emergency_contact_name} onChange={e => setForm({...form, emergency_contact_name: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Emergency Contact Phone</label>
                <input type="text" value={form.emergency_contact_phone} onChange={e => setForm({...form, emergency_contact_phone: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button onClick={() => setShowModal(false)} className="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 rounded-xl font-medium hover:bg-gray-50 transition">
                Cancel
              </button>
              <button onClick={handleSubmit} disabled={loading}
                className="flex-1 px-4 py-2.5 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-indigo-700 transition disabled:opacity-50">
                {loading ? 'Saving...' : editingId ? 'Update' : 'Add Tenant'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
