import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './PasswordResetRequest.css';

const PasswordResetRequest = ({ csrfToken }) => {
  const [email, setEmail] = useState('');
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!email) newErrors.email = 'Email is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      console.log({ email });
      navigate('/login');
    }
  };

  return (
    <div>
      <h2>Password Reset Request</h2>
      <p>Enter your email address to request a password reset link.</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          {errors.email && <div className="alert alert-danger">{errors.email}</div>}
        </div>
        <input type="submit" value="Request Password Reset" className="btn btn-primary" />
      </form>
    </div>
  );
};

export default PasswordResetRequest;
