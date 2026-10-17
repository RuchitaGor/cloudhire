import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { jobsAPI } from '../api/axios';

const BLANK = {
  title: '',
  description: '',
  requirements: '',
  skills_required: '',
  location: '',
  status: 'draft',
};

export default function JobForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [form, setForm] = useState(BLANK);
  const [loading, setLoading] = useState(false);
  const [fetchLoading, setFetchLoading] = useState(isEdit);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!isEdit) return;
    jobsAPI.getPublished(id)
      .catch(() => jobsAPI.listMy().then((r) => ({ data: r.data.find((j) => j.id === Number(id)) })))
      .then((res) => {
        if (res.data) setForm(res.data);
      })
      .catch(() => setError('Failed to load job.'))
      .finally(() => setFetchLoading(false));
  }, [id, isEdit]);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (isEdit) {
        await jobsAPI.update(id, form);
      } else {
        await jobsAPI.create(form);
      }
      navigate('/recruiter/dashboard');
    } catch (err) {
      const data = err.response?.data;
      setError(data ? Object.values(data).flat().join(' ') : 'Failed to save job.');
    } finally {
      setLoading(false);
    }
  };

  if (fetchLoading) return <div className="loading-screen"><div className="spinner"></div></div>;

  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <div className="sidebar-profile">
          <div className="avatar">R</div>
          <span className="role-badge recruiter">Recruiter</span>
        </div>
        <nav className="sidebar-nav">
          <a href="/recruiter/dashboard" className="sidebar-link">💼 My Jobs</a>
          <a href="/recruiter/jobs/new" className="sidebar-link active">➕ Post a Job</a>
        </nav>
      </aside>

      <main className="main-content">
        <div className="page-header">
          <h1>{isEdit ? 'Edit Job Posting' : 'Post a New Job'}</h1>
          <p>{isEdit ? 'Update job details' : 'Fill in the details to create a job posting'}</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="form-card">
          <form onSubmit={handleSubmit} className="job-form">
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="job-title">Job Title *</label>
                <input id="job-title" name="title" type="text" value={form.title} onChange={handleChange} placeholder="e.g. Senior Python Developer" required />
              </div>
              <div className="form-group">
                <label htmlFor="job-location">Location</label>
                <input id="job-location" name="location" type="text" value={form.location} onChange={handleChange} placeholder="e.g. New York, NY or Remote" />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="job-description">Job Description *</label>
              <textarea id="job-description" name="description" value={form.description} onChange={handleChange} rows={5} placeholder="Describe the role, responsibilities, and team…" required />
            </div>

            <div className="form-group">
              <label htmlFor="job-requirements">Requirements *</label>
              <textarea id="job-requirements" name="requirements" value={form.requirements} onChange={handleChange} rows={4} placeholder="List qualifications, education, experience…" required />
            </div>

            <div className="form-group">
              <label htmlFor="job-skills">Required Skills * <span className="hint">(comma-separated, e.g. Python,Django,REST)</span></label>
              <input
                id="job-skills"
                name="skills_required"
                type="text"
                value={form.skills_required}
                onChange={handleChange}
                placeholder="Python, Django, MySQL, REST API"
                required
              />
              {form.skills_required && (
                <div className="skill-preview">
                  {form.skills_required.split(',').map((sk, i) => sk.trim() && <span key={i} className="skill-tag">{sk.trim()}</span>)}
                </div>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="job-status">Status</label>
              <select id="job-status" name="status" value={form.status} onChange={handleChange}>
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="archived">Archived</option>
              </select>
            </div>

            <div className="form-actions">
              <button type="button" className="btn btn-outline" onClick={() => navigate('/recruiter/dashboard')}>Cancel</button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Saving…' : isEdit ? 'Update Job' : 'Post Job'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
