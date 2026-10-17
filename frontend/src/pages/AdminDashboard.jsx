import { useState, useEffect } from 'react';
import { adminAPI } from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function AdminDashboard() {
  const { user } = useAuth();
  const [users, setUsers] = useState([]);
  const [report, setReport] = useState([]);
  const [tab, setTab] = useState('users');
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const fetchData = async () => {
    setLoading(true);
    try {
      const [usersRes, reportRes] = await Promise.all([
        adminAPI.listUsers(),
        adminAPI.getReport(),
      ]);
      setUsers(usersRes.data);
      setReport(reportRes.data);
    } catch {
      setError('Failed to load data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchData(); }, []);

  const handleDeleteUser = async (id, name) => {
    if (!window.confirm(`Delete user "${name}"? This cannot be undone.`)) return;
    try {
      await adminAPI.deleteUser(id);
      setMessage(`User "${name}" removed.`);
      fetchData();
    } catch {
      setError('Failed to delete user.');
    }
  };

  const stats = {
    total: users.length,
    candidates: users.filter((u) => u.role === 'candidate').length,
    recruiters: users.filter((u) => u.role === 'recruiter').length,
    applications: report.length,
    shortlisted: report.filter((a) => a.status === 'shortlisted').length,
  };

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-profile">
          <div className="avatar">{user?.full_name?.[0]?.toUpperCase()}</div>
          <h3>{user?.full_name}</h3>
          <span className="role-badge admin">Admin</span>
        </div>
        <nav className="sidebar-nav">
          <button onClick={() => setTab('users')} className={`sidebar-link ${tab === 'users' ? 'active' : ''}`}>
            👥 Manage Users
          </button>
          <button onClick={() => setTab('report')} className={`sidebar-link ${tab === 'report' ? 'active' : ''}`}>
            📊 System Report
          </button>
        </nav>
      </aside>

      {/* Main */}
      <main className="main-content">
        <div className="page-header">
          <h1>Admin Dashboard</h1>
          <p>Manage users and monitor system activity</p>
        </div>

        {/* Stats */}
        <div className="stats-row">
          {[
            { label: 'Total Users', value: stats.total, icon: '👥' },
            { label: 'Candidates', value: stats.candidates, icon: '🎓' },
            { label: 'Recruiters', value: stats.recruiters, icon: '💼' },
            { label: 'Applications', value: stats.applications, icon: '📋' },
            { label: 'Shortlisted', value: stats.shortlisted, icon: '✅' },
          ].map((s) => (
            <div key={s.label} className="stat-card">
              <span className="stat-icon">{s.icon}</span>
              <span className="stat-value">{s.value}</span>
              <span className="stat-label">{s.label}</span>
            </div>
          ))}
        </div>

        {message && <div className="alert alert-success">{message}</div>}
        {error && <div className="alert alert-error">{error}</div>}

        {loading ? (
          <div className="loading-screen"><div className="spinner"></div></div>
        ) : tab === 'users' ? (
          /* Users Table */
          <div className="table-wrapper">
            <h2 className="section-title">All Users</h2>
            <table className="data-table" id="users-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Active</th>
                  <th>Joined</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>{u.full_name}</td>
                    <td>{u.email}</td>
                    <td><span className={`role-badge ${u.role}`}>{u.role}</span></td>
                    <td>{u.is_active ? '✅' : '❌'}</td>
                    <td>{new Date(u.date_joined).toLocaleDateString()}</td>
                    <td>
                      <button
                        id={`delete-user-${u.id}`}
                        className="btn btn-danger btn-xs"
                        onClick={() => handleDeleteUser(u.id, u.full_name)}
                      >
                        🗑 Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          /* System Report */
          <div className="table-wrapper">
            <h2 className="section-title">System Report — All Applications</h2>
            <table className="data-table" id="report-table">
              <thead>
                <tr>
                  <th>Candidate</th>
                  <th>Job</th>
                  <th>AI Match Score</th>
                  <th>Status</th>
                  <th>Applied On</th>
                </tr>
              </thead>
              <tbody>
                {report.map((app) => (
                  <tr key={app.id}>
                    <td>{app.candidate_name}<br /><small>{app.candidate_email}</small></td>
                    <td>{app.job_title}</td>
                    <td>
                      <span className="score-pill">{Math.round(app.match_score)}%</span>
                    </td>
                    <td>
                      <span className={`status-chip ${app.status}`}>{app.status}</span>
                    </td>
                    <td>{new Date(app.applied_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}
