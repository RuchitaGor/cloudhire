import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getDashboardLink = () => {
    if (!user) return '/login';
    if (user.role === 'candidate') return '/candidate/dashboard';
    if (user.role === 'recruiter') return '/recruiter/dashboard';
    if (user.role === 'admin') return '/admin/dashboard';
    return '/';
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to={getDashboardLink()} className="brand-link">
          <span className="brand-icon">☁</span>
          <span className="brand-name">CloudHire</span>
        </Link>
      </div>

      <div className="navbar-links">
        {user ? (
          <>
            <span className="navbar-role-badge">{user.role}</span>
            <span className="navbar-user">{user.full_name}</span>
            <button onClick={handleLogout} className="btn btn-outline-sm">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="btn btn-primary-sm">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}
