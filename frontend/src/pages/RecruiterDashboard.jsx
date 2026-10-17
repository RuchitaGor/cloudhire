import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { jobsAPI } from '../api/axios';
import { useAuth } from '../context/AuthContext';

export default function RecruiterDashboard() {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const fetchJobs = async () => {
    try {
      const res = await jobsAPI.listMy();
      setJobs(res.data);
    } catch {
      setError('Failed to load jobs.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchJobs(); }, []);

  const handleStatusChange = async (job, newStatus) => {
    try {
      await jobsAPI.update(job.id, { status: newStatus });
      setMessage(`"${job.title}" status updated to ${newStatus}.`);
      fetchJobs();
    } catch {
      setError('Failed to update status.');
    }
  };

  const handleDelete = async (job) => {
    if (!window.confirm(`Delete "${job.title}"?`)) return;
    try {
      await jobsAPI.remove(job.id);
      setMessage(`"${job.title}" deleted.`);
      fetchJobs();
    } catch {
      setError('Failed to delete job.');
    }
  };

  const stats = {
    total: jobs.length,
    published: jobs.filter((j) => j.status === 'published').length,
    draft: jobs.filter((j) => j.status === 'draft').length,
    archived: jobs.filter((j) => j.status === 'archived').length,
  };

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-profile">
          <div className="avatar">{user?.full_name?.[0]?.toUpperCase()}</div>
          <h3>{user?.full_name}</h3>
          <span className="role-badge recruiter">Recruiter</span>
        </div>
        <nav className="sidebar-nav">
          <a href="/recruiter/dashboard" className="sidebar-link active">💼 My Jobs</a>
          <a href="/recruiter/jobs/new" className="sidebar-link">➕ Post a Job</a>
        </nav>
      </aside>

      {/* Main */}
      <main className="main-content">
        <div className="page-header">
          <div>
            <h1>Recruiter Dashboard</h1>
            <p>Manage your job postings and review applicants</p>
          </div>
          <Link to="/recruiter/jobs/new" className="btn btn-primary">+ Post New Job</Link>
        </div>

        {/* Stats */}
        <div className="stats-row">
          {[
            { label: 'Total Jobs', value: stats.total, icon: '💼' },
            { label: 'Published', value: stats.published, icon: '🟢' },
            { label: 'Drafts', value: stats.draft, icon: '📝' },
            { label: 'Archived', value: stats.archived, icon: '📦' },
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
        ) : jobs.length === 0 ? (
          <div className="empty-state">
            <span className="empty-icon">💼</span>
            <p>No jobs posted yet.</p>
            <Link to="/recruiter/jobs/new" className="btn btn-primary">Post Your First Job</Link>
          </div>
        ) : (
          <div className="recruiter-jobs-list">
            {jobs.map((job) => (
              <div key={job.id} className="recruiter-job-card">
                <div className="recruiter-job-info">
                  <h3>{job.title}</h3>
                  <p className="job-location">📍 {job.location || 'Remote'}</p>
                  <div className="skill-tags">
                    {job.skills_required.split(',').slice(0, 4).map((sk, i) => (
                      <span key={i} className="skill-tag">{sk.trim()}</span>
                    ))}
                  </div>
                </div>
                <div className="recruiter-job-actions">
                  <span className={`status-chip ${job.status}`}>{job.status}</span>
                  <Link to={`/recruiter/jobs/${job.id}/applicants`} className="btn btn-outline btn-sm">
                    👥 View Applicants
                  </Link>
                  <Link to={`/recruiter/jobs/${job.id}/edit`} className="btn btn-outline btn-sm">
                    ✏️ Edit
                  </Link>
                  {job.status !== 'published' && (
                    <button className="btn btn-success btn-sm" onClick={() => handleStatusChange(job, 'published')}>
                      Publish
                    </button>
                  )}
                  {job.status !== 'archived' && (
                    <button className="btn btn-outline btn-sm" onClick={() => handleStatusChange(job, 'archived')}>
                      Archive
                    </button>
                  )}
                  <button className="btn btn-danger btn-sm" onClick={() => handleDelete(job)}>
                    🗑 Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
