import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';

import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CandidateDashboard from './pages/CandidateDashboard';
import CandidateApplications from './pages/CandidateApplications';
import RecruiterDashboard from './pages/RecruiterDashboard';
import JobForm from './pages/JobForm';
import RecruiterApplicants from './pages/RecruiterApplicants';
import AdminDashboard from './pages/AdminDashboard';

function Unauthorized() {
  return (
    <div className="auth-container">
      <div className="auth-card" style={{ textAlign: 'center' }}>
        <div className="auth-logo">🚫</div>
        <h1 className="auth-title">Access Denied</h1>
        <p className="auth-subtitle">You don&apos;t have permission to view this page.</p>
        <a href="/login" className="btn btn-primary" style={{ marginTop: '1rem', display: 'inline-block' }}>
          Back to Login
        </a>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          {/* Public */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/unauthorized" element={<Unauthorized />} />
          <Route path="/" element={<Navigate to="/login" replace />} />

          {/* Candidate */}
          <Route
            path="/candidate/dashboard"
            element={<ProtectedRoute allowedRoles={['candidate']}><CandidateDashboard /></ProtectedRoute>}
          />
          <Route
            path="/candidate/applications"
            element={<ProtectedRoute allowedRoles={['candidate']}><CandidateApplications /></ProtectedRoute>}
          />

          {/* Recruiter */}
          <Route
            path="/recruiter/dashboard"
            element={<ProtectedRoute allowedRoles={['recruiter']}><RecruiterDashboard /></ProtectedRoute>}
          />
          <Route
            path="/recruiter/jobs/new"
            element={<ProtectedRoute allowedRoles={['recruiter']}><JobForm /></ProtectedRoute>}
          />
          <Route
            path="/recruiter/jobs/:id/edit"
            element={<ProtectedRoute allowedRoles={['recruiter']}><JobForm /></ProtectedRoute>}
          />
          <Route
            path="/recruiter/jobs/:jobId/applicants"
            element={<ProtectedRoute allowedRoles={['recruiter']}><RecruiterApplicants /></ProtectedRoute>}
          />

          {/* Admin */}
          <Route
            path="/admin/dashboard"
            element={<ProtectedRoute allowedRoles={['admin']}><AdminDashboard /></ProtectedRoute>}
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
