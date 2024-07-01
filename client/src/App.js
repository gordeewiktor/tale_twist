import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './components/Home';
import Stories from './components/Stories';
import Profile from './components/Profile';
import './App.css';
import './style.css';

const sampleStories = [
  // Add sample stories here to test
];

const currentUser = {
  isAuthenticated: true, // or false
  id: 1 // Sample user ID
};

function App() {
  return (
    <BrowserRouter>
      <Layout isAuthenticated={currentUser.isAuthenticated}>
        <Routes>
          <Route path="/" element={<Home stories={sampleStories} currentUser={currentUser} />} />
          <Route path="/stories" element={<Stories stories={sampleStories} currentUser={currentUser} />} />
          <Route path="/profile" element={<Profile />} />
          {/* Add more routes as needed */}
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
