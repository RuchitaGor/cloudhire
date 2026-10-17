import { useState, useEffect } from 'react';
import { applicationsAPI } from '../api/axios';
import { useAuth } from '../context/AuthContext';

const STATUS_CONFIG = {
  pending: { label: 'Under Review', color: '#f59e0b', icon: '⏳' },
  shortlisted: { label: 'Shortlisted', color: '#10b981', icon: '✅' },
  rejected: { label: 'Not Selected', color: '#ef4444', icon: '❌' },
};

export default function CandidateApplications() {
  const { user } = useAuth();
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    applicationsAPI.listMy()
      .then((res) => setApplications(res.data))
      .catch(() => setApplications([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-profile">
          <div className="avatar">{user?.full_name?.[0]?.toUpperCase()}</div>
          <h3>{user?.full_name}</h3>
          <span className="role-badge candidate">Candidate</span>
        </div>
        <nav className="sidebar-nav">
          <a href="/candidate/dashboard" className="sidebar-link">🔍 Job Search</a>
          <a href="/candidate/applications" className="sidebar-link active">📋 My Applications</a>
        </nav>
      </aside>

      {/* Main */}
      <main className="main-content">
        <div className="page-header">
          <h1>My Applications</h1>
          <p>Track the status of all your job applications</p>
        </div>

        {loading ? (
          <div className="loading-screen"><div className="spinner"></div></div>
        ) : applications.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">📭</span>
            <p>You haven&apos;t applied for any jobs yet.</p>
            <a href="/candidate/dashboard" className="btn btn-primary">Browse Jobs</a>
          </div>
        ) : (
          <div className="applications-list">
            {applications.map((app) => {
              const cfg = STATUS_CONFIG[app.status] || STATUS_CONFIG.pending;
              return (
                <div key={app.id} className="application-card">
                  <div className="application-card-left">
                    <h3 className="application-job-title">{app.job_title}</h3>
                    <p className="application-date">
                      Applied on {new Date(app.applied_at).toLocaleDateString()}
                    </p>
                    {app.resume_url && (
                      <a href={app.resume_url} target="_blank" rel="noreferrer" className="resume-link">
                        📄 View Resume
                      </a>
                    )}
                  </div>
                  <div className="application-card-right">
                    <div className="match-score-circle">
                      <svg viewBox="0 0 36 36" className="score-svg">
                        <path
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none"
                          stroke="#e2e8f0"
                          strokeWidth="3"
                        />
                        <path
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                          fill="none"
                          stroke="#6366f1"
                          strokeWidth="3"
                          strokeDasharray={`${app.match_score}, 100`}
                        />
                      </svg>
                      <div className="score-text">
                        <span className="score-number">{Math.round(app.match_score)}%</span>
                        <span className="score-label">Match</span>
                      </div>
                    </div>
                    <div className="status-badge" style={{ borderColor: cfg.color, color: cfg.color }}>
                      {cfg.icon} {cfg.label}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}
