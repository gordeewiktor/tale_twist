import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = ({ isAuthenticated }) => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/stories">Stories</Link></li>
        {isAuthenticated ? (
          <>
            <li><Link to="/profile">Profile</Link></li>
            <li><Link to="/create-story">Create Story</Link></li>
            <li><Link to="/logout">Logout</Link></li>
          </>
        ) : (
          <>
            <li><Link to="/register">Register</Link></li>
            <li><Link to="/login">Login</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default NavBar;
