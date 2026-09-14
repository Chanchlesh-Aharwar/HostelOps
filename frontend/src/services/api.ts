const API_BASE = '/api';

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(error.detail || 'API error');
  }
  return res.json();
}

export const api = {
  // Dashboard
  getDashboard: () => fetchJSON<any>('/dashboard/'),

  // Rooms
  getRooms: () => fetchJSON<any[]>('/rooms/'),
  getRoom: (id: number) => fetchJSON<any>(`/rooms/${id}`),
  getAvailableRooms: () => fetchJSON<any[]>('/rooms/available/'),
  createRoom: (data: any) =>
    fetchJSON<any>('/rooms/', { method: 'POST', body: JSON.stringify(data) }),
  updateRoom: (id: number, data: any) =>
    fetchJSON<any>(`/rooms/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteRoom: (id: number) =>
    fetchJSON<any>(`/rooms/${id}`, { method: 'DELETE' }),

  // Tenants
  getTenants: () => fetchJSON<any[]>('/tenants/'),
  getTenant: (id: number) => fetchJSON<any>(`/tenants/${id}`),
  createTenant: (data: any) =>
    fetchJSON<any>('/tenants/', { method: 'POST', body: JSON.stringify(data) }),
  updateTenant: (id: number, data: any) =>
    fetchJSON<any>(`/tenants/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  deleteTenant: (id: number) =>
    fetchJSON<any>(`/tenants/${id}`, { method: 'DELETE' }),

  // Vendors
  getVendors: (category?: string) => {
    const params = category ? `?category=${category}` : '';
    return fetchJSON<any[]>(`/vendors/${params}`);
  },
  getVendor: (id: number) => fetchJSON<any>(`/vendors/${id}`),

  // Complaints
  getComplaints: () => fetchJSON<any[]>('/complaints/'),
  getComplaint: (id: number) => fetchJSON<any>(`/complaints/${id}`),
  createComplaint: (data: any) =>
    fetchJSON<any>('/complaints/', { method: 'POST', body: JSON.stringify(data) }),

  // Rent
  getRentSummary: () => fetchJSON<any>('/rent/summary'),
  getRentPayments: () => fetchJSON<any[]>('/rent/payments'),

  // Approvals
  getApprovals: () => fetchJSON<any[]>('/approvals/'),
  approveAction: (id: number, notes?: string) =>
    fetchJSON<any>(`/approvals/${id}/approve`, {
      method: 'POST',
      body: JSON.stringify({ decision_notes: notes }),
    }),
  rejectAction: (id: number, notes?: string) =>
    fetchJSON<any>(`/approvals/${id}/reject`, {
      method: 'POST',
      body: JSON.stringify({ decision_notes: notes }),
    }),

  // Agent
  getAgentActions: () => fetchJSON<any[]>('/agent/actions/'),
  chatWithAgent: (message: string, tenantPhone?: string) =>
    fetchJSON<any>('/agent/chat', {
      method: 'POST',
      body: JSON.stringify({ message, tenant_phone: tenantPhone }),
    }),
};
