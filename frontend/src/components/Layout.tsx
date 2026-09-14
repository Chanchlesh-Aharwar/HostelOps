import { NavLink, Outlet } from 'react-router-dom';

const navItems = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/rooms', label: 'Rooms', icon: '🏠' },
  { to: '/tenants', label: 'Tenants', icon: '👤' },
  { to: '/complaints', label: 'Complaints', icon: '🔧' },
  { to: '/vendors', label: 'Vendors', icon: '🛠' },
  { to: '/rent', label: 'Rent', icon: '💰' },
  { to: '/rent-automation', label: 'Rent Auto', icon: '⚡' },
  { to: '/approvals', label: 'Approvals', icon: '✅' },
  { to: '/agent', label: 'AI Agent', icon: '🤖' },
  { to: '/whatsapp', label: 'WhatsApp', icon: '📱' },
  { to: '/activity', label: 'AI Activity', icon: '📋' },
];

export default function Layout() {
  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Sidebar */}
      <aside className="w-72 bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white flex flex-col shadow-2xl">
        {/* Logo */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center text-lg font-bold shadow-lg">
              H
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight">HostelOps</h1>
              <p className="text-xs text-gray-400">AI Operations Manager</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl text-sm transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg shadow-blue-500/25'
                    : 'text-gray-300 hover:bg-white/10 hover:text-white hover:translate-x-1'
                }`
              }
            >
              <span className="text-lg">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center text-xs font-bold">
              RS
            </div>
            <div>
              <p className="text-sm font-medium">Rahul Sharma</p>
              <p className="text-xs text-gray-400">Sunshine PG</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
