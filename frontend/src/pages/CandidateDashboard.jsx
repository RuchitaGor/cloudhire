import { useState, useEffect, useRef } from 'react';
import { useAuth } from '../context/AuthContext';
import { jobsAPI, resumeAPI, applicationsAPI } from '../api/axios';

export default function CandidateDashboard() {
  const { user } = useAuth();
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState('');
  const [resume, setResume] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [applying, setApplying] = useState(null);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const fileRef = useRef(null);

  const fetchJobs = async (q = '') => {
    try {
      const res = await jobsAPI.listPublished(q);
      setJobs(res.data);
    } catch {
      setJobs([]);
    }
  };

  const fetchResume = async () => {
    try {
      const res = await resumeAPI.getMy();
      setResume(res.data);
    } catch {
      setResume(null);
    }
  };

  useEffect(() => {
    fetchJobs();
    fetchResume();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchJobs(search);
  };

  const handleResumeUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    setError('');
    setMessage('');
    try {
      const formData = new FormData();
      formData.append('file', file);
      const res = await resumeAPI.upload(formData);
      setResume(res.data);
      setMessage('✓ Resume uploaded successfully!');
    } catch (err) {
      setError(err.response?.data?.file?.[0] || 'Upload failed. Ensure PDF/DOCX/TXT under 5 MB.');
    } finally {
      setUploading(false);
    }
  };

  const handleApply = async (jobId) => {
    if (!resume) {
      setError('Please upload your resume first.');
      return;
    }
    setApplying(jobId);
    setError('');
    setMessage('');
    try {
      await applicationsAPI.apply(jobId);
      setMessage('✓ Application submitted! AI matching in progress.');
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.[0] || 'Failed to apply.');
    } finally {
      setApplying(null);
    }
  };

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
          <a href="/candidate/dashboard" className="sidebar-link active">🔍 Job Search</a>
          <a href="/candidate/applications" className="sidebar-link">📋 My Applications</a>
        </nav>
        <div className="sidebar-resume">
          <h4>My Resume</h4>
          {resume ? (
            <div className="resume-status uploaded">
              <span>✓ {resume.original_filename}</span>
              <a href={resume.cloudinary_url} target="_blank" rel="noreferrer" className="resume-view-link">View</a>
            </div>
          ) : (
            <div className="resume-status missing">No resume uploaded</div>
          )}
          <button className="btn btn-outline btn-sm" onClick={() => fileRef.current?.click()} disabled={uploading}>
            {uploading ? 'Uploading…' : 'Upload Resume (PDF/DOCX/TXT)'}
          </button>
          <input
            ref={fileRef}
            type="file"
            accept=".pdf,.docx,.txt"
            style={{ display: 'none' }}
            onChange={handleResumeUpload}
          />
        </div>
      </aside>

      {/* Main */}
      <main className="main-content">
        <div className="page-header">
          <h1>Find Your Next Job</h1>
          <p>Browse and apply for positions matched to your skills</p>
        </div>

        {message && <div className="alert alert-success">{message}</div>}
        {error && <div className="alert alert-error">{error}</div>}

        {/* Search */}
        <form onSubmit={handleSearch} className="search-bar">
          <input
            id="job-search-input"
            type="text"
            placeholder="Search by title, skills, or location…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit" className="btn btn-primary">Search</button>
        </form>

        {/* Job List */}
        <div className="job-grid">
          {jobs.length === 0 ? (
            <div className="empty-state">No jobs found. Try a different search.</div>
          ) : (
            jobs.map((job) => (
              <div key={job.id} className="job-card">
                <div className="job-card-header">
                  <div>
                    <h3 className="job-title">{job.title}</h3>
                    <p className="job-company">{job.recruiter_name}</p>
                  </div>
                  <span className="job-location">📍 {job.location || 'Remote'}</span>
                </div>
                <p className="job-description">{job.description.slice(0, 150)}…</p>
                <div className="skill-tags">
                  {job.skills_required.split(',').map((sk, i) => (
                    <span key={i} className="skill-tag">{sk.trim()}</span>
                  ))}
                </div>
                <div className="job-card-footer">
                  <span className="job-date">{new Date(job.created_at).toLocaleDateString()}</span>
                  <button
                    id={`apply-btn-${job.id}`}
                    className="btn btn-primary btn-sm"
                    onClick={() => handleApply(job.id)}
                    disabled={applying === job.id}
                  >
                    {applying === job.id ? 'Applying…' : 'Apply Now'}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}
