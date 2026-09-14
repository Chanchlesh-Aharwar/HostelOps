import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Rooms from './pages/Rooms';
import Tenants from './pages/Tenants';
import Complaints from './pages/Complaints';
import Vendors from './pages/Vendors';
import Rent from './pages/Rent';
import RentAutomation from './pages/RentAutomation';
import Approvals from './pages/Approvals';
import AgentChat from './pages/AgentChat';
import WhatsApp from './pages/WhatsApp';
import Activity from './pages/Activity';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/rooms" element={<Rooms />} />
          <Route path="/tenants" element={<Tenants />} />
          <Route path="/complaints" element={<Complaints />} />
          <Route path="/vendors" element={<Vendors />} />
          <Route path="/rent" element={<Rent />} />
          <Route path="/rent-automation" element={<RentAutomation />} />
          <Route path="/approvals" element={<Approvals />} />
          <Route path="/agent" element={<AgentChat />} />
          <Route path="/whatsapp" element={<WhatsApp />} />
          <Route path="/activity" element={<Activity />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
