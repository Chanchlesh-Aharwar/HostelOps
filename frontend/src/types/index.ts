export interface Room {
  id: number;
  hostel_id: number;
  room_number: string;
  floor: number | null;
  room_type: string | null;
  capacity: number | null;
  rent_amount: number;
  security_deposit: number;
  status: string;
  created_at: string | null;
  updated_at: string | null;
  tenants: TenantBrief[];
}

export interface TenantBrief {
  id: number;
  name: string;
  phone: string;
  status: string;
}

export interface Tenant {
  id: number;
  room_id: number | null;
  name: string;
  phone: string;
  email: string | null;
  emergency_contact_name: string | null;
  emergency_contact_phone: string | null;
  move_in_date: string | null;
  move_out_date: string | null;
  rent_due_day: number | null;
  status: string;
  created_at: string | null;
  updated_at: string | null;
  room: Room | null;
}

export interface Vendor {
  id: number;
  name: string;
  phone: string;
  email: string | null;
  category: string;
  rating: number;
  average_cost: number;
  service_area: string | null;
  availability: string;
  total_jobs: number;
  successful_jobs: number;
  status: string;
  created_at: string | null;
  updated_at: string | null;
}

export interface Complaint {
  id: number;
  tenant_id: number;
  room_id: number | null;
  title: string;
  description: string;
  category: string | null;
  priority: string | null;
  status: string | null;
  source: string | null;
  image_url: string | null;
  ai_analysis: Record<string, unknown> | null;
  created_at: string | null;
  updated_at: string | null;
  resolved_at: string | null;
  tenant: TenantBrief | null;
  room: { room_number: string } | null;
}

export interface RentPayment {
  id: number;
  tenant_id: number;
  amount: number;
  due_date: string;
  paid_date: string | null;
  status: string | null;
  payment_method: string | null;
  transaction_reference: string | null;
  notes: string | null;
  created_at: string | null;
  updated_at: string | null;
  tenant: TenantBrief | null;
}

export interface RentSummary {
  total_expected: number;
  total_paid: number;
  total_pending: number;
  total_overdue: number;
  paid_count: number;
  pending_count: number;
  overdue_count: number;
}

export interface Approval {
  id: number;
  action_type: string;
  entity_type: string;
  entity_id: number;
  requested_by: string | null;
  reason: string;
  status: string | null;
  approved_by: number | null;
  decision_notes: string | null;
  created_at: string | null;
  decision_at: string | null;
}

export interface AgentAction {
  id: number;
  agent_name: string;
  action_type: string;
  entity_type: string | null;
  entity_id: number | null;
  input_data: Record<string, unknown> | null;
  output_data: Record<string, unknown> | null;
  status: string | null;
  error_message: string | null;
  created_at: string | null;
  completed_at: string | null;
}

export interface DashboardStats {
  total_rooms: number;
  occupied_rooms: number;
  vacant_rooms: number;
  total_tenants: number;
  total_expected_rent: number;
  total_pending_rent: number;
  open_complaints: number;
  active_maintenance_jobs: number;
  pending_approvals: number;
  recent_agent_actions: AgentAction[];
}

export interface AgentChatResponse {
  response: string;
  complaint_id: number | null;
  actions: AgentAction[];
}
