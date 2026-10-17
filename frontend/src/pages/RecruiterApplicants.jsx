import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { applicationsAPI } from '../api/axios';

const STATUS_COLORS = {
  pending: '#f59e0b',
  shortlisted: '#10b981',
  rejected: '#ef4444',
};

export default function RecruiterApplicants() {
  const { jobId } = useParams();
  const [applicants, setApplicants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const fetchApplicants = async () => {
    try {
      const res = await applicationsAPI.listByJob(jobId);
      setApplicants(res.data);
    } catch {
      setError('Failed to load applicants.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchApplicants(); }, [jobId]);

  const handleStatusUpdate = async (appId, newStatus, name) => {
    try {
      await applicationsAPI.updateStatus(appId, newStatus);
      setMessage(`${name}'s application marked as ${newStatus}.`);
      fetchApplicants();
    } catch {
      setError('Failed to update status.');
    }
  };

  const jobTitle = applicants[0]?.job_title || 'Job';

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-profile">
          <div className="avatar">R</div>
          <span className="role-badge recruiter">Recruiter</span>
        </div>
        <nav className="sidebar-nav">
          <a href="/recruiter/dashboard" className="sidebar-link">💼 My Jobs</a>
          <a href="/recruiter/jobs/new" className="sidebar-link">➕ Post a Job</a>
        </nav>
      </aside>

      <main className="main-content">
        <div className="page-header">
          <div>
            <Link to="/recruiter/dashboard" className="back-link">← Back to Jobs</Link>
            <h1>Applicants for: {jobTitle}</h1>
            <p>Review AI match scores and shortlist candidates</p>
          </div>
        </div>

        {message && <div className="alert alert-success">{message}</div>}
        {error && <div className="alert alert-error">{error}</div>}

        {loading ? (
          <div className="loading-screen"><div className="spinner"></div></div>
        ) : applicants.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">👥</span>
            <p>No applicants yet for this job.</p>
          </div>
        ) : (
          <div className="applicants-table-wrapper">
            <div className="applicants-summary">
              <span>{applicants.length} applicant{applicants.length !== 1 ? 's' : ''}</span>
              <span className="shortlisted-count">
                ✅ {applicants.filter((a) => a.status === 'shortlisted').length} shortlisted
              </span>
            </div>
            <table className="applicants-table" id="applicants-table">
              <thead>
                <tr>
                  <th>Candidate</th>
                  <th>Email</th>
                  <th>AI Match Score</th>
                  <th>Status</th>
                  <th>Resume</th>
                  <th>Applied On</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {applicants.map((app) => (
                  <tr key={app.id} className={`applicant-row ${app.status}`}>
                    <td className="candidate-name">{app.candidate_name}</td>
                    <td className="candidate-email">{app.candidate_email}</td>
                    <td>
                      <div className="match-score-bar-wrapper">
                        <div
                          className="match-score-bar"
                          style={{
                            width: `${app.match_score}%`,
                            backgroundColor:
                              app.match_score >= 70 ? '#10b981'
                              : app.match_score >= 40 ? '#f59e0b'
                              : '#ef4444',
                          }}
                        />
                        <span className="match-score-label">{Math.round(app.match_score)}%</span>
                      </div>
                    </td>
                    <td>
                      <span
                        className="status-badge-inline"
                        style={{ color: STATUS_COLORS[app.status] || '#64748b' }}
                      >
                        {app.status}
                      </span>
                    </td>
                    <td>
                      {app.resume_url ? (
                        <a href={app.resume_url} target="_blank" rel="noreferrer" className="resume-link">
                          📄 View
                        </a>
                      ) : '—'}
                    </td>
                    <td>{new Date(app.applied_at).toLocaleDateString()}</td>
                    <td>
                      <div className="action-buttons">
                        <button
                          id={`shortlist-${app.id}`}
                          className="btn btn-success btn-xs"
                          disabled={app.status === 'shortlisted'}
                          onClick={() => handleStatusUpdate(app.id, 'shortlisted', app.candidate_name)}
                        >
                          ✅ Shortlist
                        </button>
                        <button
                          id={`reject-${app.id}`}
                          className="btn btn-danger btn-xs"
                          disabled={app.status === 'rejected'}
                          onClick={() => handleStatusUpdate(app.id, 'rejected', app.candidate_name)}
                        >
                          ❌ Reject
                        </button>
                      </div>
                    </td>
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
