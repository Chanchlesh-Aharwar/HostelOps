import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Room } from '../types';

interface FormData {
  room_number: string;
  floor: string;
  room_type: string;
  capacity: string;
  rent_amount: string;
  security_deposit: string;
}

const emptyForm: FormData = {
  room_number: '', floor: '', room_type: 'SINGLE',
  capacity: '1', rent_amount: '', security_deposit: '0',
};

export default function Rooms() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [filter, setFilter] = useState('ALL');
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState<FormData>(emptyForm);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const load = () => api.getRooms().then(setRooms).catch(console.error);
  useEffect(() => { load(); }, []);

  const statusConfig: Record<string, { bg: string; text: string; dot: string }> = {
    VACANT: { bg: 'bg-emerald-50', text: 'text-emerald-700', dot: 'bg-emerald-400' },
    OCCUPIED: { bg: 'bg-red-50', text: 'text-red-700', dot: 'bg-red-400' },
    PARTIALLY_OCCUPIED: { bg: 'bg-amber-50', text: 'text-amber-700', dot: 'bg-amber-400' },
    MAINTENANCE: { bg: 'bg-orange-50', text: 'text-orange-700', dot: 'bg-orange-400' },
  };

  const filtered = filter === 'ALL' ? rooms : rooms.filter(r => r.status === filter);

  const openAdd = () => {
    setForm(emptyForm);
    setEditingId(null);
    setError('');
    setShowModal(true);
  };

  const openEdit = (r: Room) => {
    setForm({
      room_number: r.room_number,
      floor: r.floor?.toString() || '',
      room_type: r.room_type || 'SINGLE',
      capacity: r.capacity?.toString() || '1',
      rent_amount: r.rent_amount.toString(),
      security_deposit: r.security_deposit?.toString() || '0',
    });
    setEditingId(r.id);
    setError('');
    setShowModal(true);
  };

  const handleSubmit = async () => {
    if (!form.room_number || !form.rent_amount) {
      setError('Room number and rent amount are required');
      return;
    }
    setLoading(true);
    try {
      const data = {
        room_number: form.room_number,
        floor: form.floor ? parseInt(form.floor) : null,
        room_type: form.room_type,
        capacity: parseInt(form.capacity),
        rent_amount: parseFloat(form.rent_amount),
        security_deposit: parseFloat(form.security_deposit),
      };
      if (editingId) {
        await api.updateRoom(editingId, data);
      } else {
        await api.createRoom(data);
      }
      setShowModal(false);
      load();
    } catch (err) {
      setError((err as Error).message);
    }
    setLoading(false);
  };

  const handleDelete = async (id: number, roomNumber: string) => {
    if (!confirm(`Delete room ${roomNumber}?`)) return;
    try {
      await api.deleteRoom(id);
      load();
    } catch (err) {
      alert((err as Error).message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Rooms</h1>
          <p className="text-gray-500 mt-1">Manage room inventory across all floors</p>
        </div>
        <button onClick={openAdd} className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-indigo-700 transition-all shadow-lg shadow-blue-500/25">
          + Add Room
        </button>
      </div>

      <div className="flex gap-2">
        {['ALL', 'VACANT', 'OCCUPIED', 'PARTIALLY_OCCUPIED', 'MAINTENANCE'].map(s => (
          <button key={s} onClick={() => setFilter(s)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
              filter === s ? 'bg-gray-900 text-white shadow-lg' : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
            }`}>
            {s === 'ALL' ? 'All' : s.replace('_', ' ')}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-5 gap-4">
        {filtered.map((room) => {
          const cfg = statusConfig[room.status] || statusConfig.VACANT;
          return (
            <div key={room.id} className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 hover:shadow-lg hover:-translate-y-1 transition-all duration-200">
              <div className="flex items-center justify-between mb-3">
                <span className="text-2xl font-bold text-gray-900">{room.room_number}</span>
                <span className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${cfg.bg} ${cfg.text}`}>
                  <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot}`}></span>
                  {room.status.replace('_', ' ')}
                </span>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-gray-500">
                  <span>Floor {room.floor}</span>
                  <span>{room.room_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Rent</span>
                  <span className="font-bold text-gray-900">₹{room.rent_amount.toLocaleString()}</span>
                </div>
                <div className="flex justify-between text-gray-500">
                  <span>Capacity</span>
                  <span>{room.tenants.length}/{room.capacity}</span>
                </div>
              </div>
              {room.tenants.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                  <div className="flex flex-wrap gap-1">
                    {room.tenants.map(t => (
                      <span key={t.id} className="text-xs bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full">{t.name}</span>
                    ))}
                  </div>
                </div>
              )}
              <div className="mt-3 pt-3 border-t border-gray-100 flex gap-2">
                <button onClick={() => openEdit(room)} className="flex-1 px-3 py-1.5 bg-blue-50 text-blue-600 rounded-lg text-xs font-medium hover:bg-blue-100 transition">
                  Edit
                </button>
                <button onClick={() => handleDelete(room.id, room.room_number)} className="flex-1 px-3 py-1.5 bg-red-50 text-red-600 rounded-lg text-xs font-medium hover:bg-red-100 transition">
                  Delete
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              {editingId ? 'Edit Room' : 'Add New Room'}
            </h2>

            {error && (
              <div className="bg-red-50 text-red-700 p-3 rounded-xl text-sm mb-4">{error}</div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-gray-500 font-medium">Room Number *</label>
                <input type="text" value={form.room_number} onChange={e => setForm({...form, room_number: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="101" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Floor</label>
                <input type="number" value={form.floor} onChange={e => setForm({...form, floor: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="1" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Room Type</label>
                <select value={form.room_type} onChange={e => setForm({...form, room_type: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option value="SINGLE">Single</option>
                  <option value="DOUBLE">Double</option>
                  <option value="TRIPLE">Triple</option>
                  <option value="DORMITORY">Dormitory</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Capacity</label>
                <input type="number" value={form.capacity} onChange={e => setForm({...form, capacity: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" min="1" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Rent Amount (₹) *</label>
                <input type="number" value={form.rent_amount} onChange={e => setForm({...form, rent_amount: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="8000" />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium">Security Deposit (₹)</label>
                <input type="number" value={form.security_deposit} onChange={e => setForm({...form, security_deposit: e.target.value})}
                  className="w-full mt-1 px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" placeholder="8000" />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button onClick={() => setShowModal(false)} className="flex-1 px-4 py-2.5 border border-gray-200 text-gray-600 rounded-xl font-medium hover:bg-gray-50 transition">
                Cancel
              </button>
              <button onClick={handleSubmit} disabled={loading}
                className="flex-1 px-4 py-2.5 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-medium hover:from-blue-600 hover:to-indigo-700 transition disabled:opacity-50">
                {loading ? 'Saving...' : editingId ? 'Update' : 'Add Room'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
