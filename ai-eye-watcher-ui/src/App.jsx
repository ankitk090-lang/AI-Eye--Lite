import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import DashboardPage from './pages/DashboardPage';
import AlertsPage from './pages/AlertsPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<DashboardPage />} />
        {/* Placeholder routes for other pages */}
        <Route path="/network" element={<div>Network Activity Page (Coming Soon)</div>} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/policies" element={<div>Policy Management Page (Coming Soon)</div>} />
        <Route path="/devices" element={<div>Devices Page (Coming Soon)</div>} />
        <Route path="/settings" element={<div>Settings Page (Coming Soon)</div>} />
      </Route>
    </Routes>
  );
}

export default App;
