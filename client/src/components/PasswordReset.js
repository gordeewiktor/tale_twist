import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './PasswordReset.css';

const PasswordReset = ({ csrfToken }) => {
  const { token } = useParams();
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!password) newErrors.password = 'Password is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      console.log({ password, token });
      navigate('/login');
    }
  };

  return (
    <div>
      <h2>Reset Password</h2>
      <p>Please enter your new password.</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="password">New Password</label>
          <input
            type="password"
            id="password"
            name="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {errors.password && <div className="alert alert-danger">{errors.password}</div>}
        </div>
        <input type="submit" value="Reset Password" className="btn btn-primary" />
      </form>
    </div>
  );
};

export default PasswordReset;
