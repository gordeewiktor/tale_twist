import React from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './components/Home';
import Stories from './components/Stories';
import Profile from './components/Profile';
import ReadStory from './components/ReadStory';
import CreateStory from './components/CreateStory';
import ManageStory from './components/ManageStory';
import ManageSegment from './components/ManageSegment';
import Login from './components/Login';
import Register from './components/Register';
import EditProfile from './components/EditProfile';
import PasswordResetRequest from './components/PasswordResetRequest';
import PasswordReset from './components/PasswordReset';
import './App.css';
import './style.css';

const sampleStories = [
  // Add sample stories here to test
];

const sampleSegments = [
  {
    id: 1,
    title: 'Sample Segment Title',
    content: 'This is the content of the segment.',
    choices: [
      { text: 'Choice 1', next_segment_id: 2 },
      { text: 'Choice 2', next_segment_id: null }
    ]
  },
  // Add more segments as needed
];

const sampleSegment = {
  id: 1,
  title: 'Sample Segment Title',
  content: 'This is the content of the segment.',
  choices: [
    { text: 'Choice 1', next_segment_id: 2 },
    { text: 'Choice 2', next_segment_id: null }
  ]
};

const currentUser = {
  is_authenticated: true, // or false
  id: 1, // Sample user ID
  username: 'johndoe', // Sample username
  email: 'johndoe@example.com' // Sample email
};

const csrfToken = 'sample-csrf-token';

const Logout = () => {
  // Logic to handle logout
  // For example, clear user session and redirect to login
  console.log('User logged out');
  return <Navigate to="/login" />;
};

function App() {
  return (
    <BrowserRouter>
      <Layout isAuthenticated={currentUser.is_authenticated}>
        <Routes>
          <Route path="/" element={<Home stories={sampleStories} currentUser={currentUser} />} />
          <Route path="/stories" element={<Stories stories={sampleStories} currentUser={currentUser} />} />
          <Route path="/profile" element={<Profile currentUser={currentUser} />} />
          <Route path="/stories/:storyId/segments/:segmentId" element={<ReadStory story={sampleStories[0]} segment={sampleSegments[0]} choices={sampleSegments[0].choices} currentUser={currentUser} />} />
          <Route path="/create-story" element={<CreateStory currentUser={currentUser} />} />
          <Route path="/stories/:storyId/manage" element={<ManageStory story={sampleStories[0]} segments={sampleSegments} currentUser={currentUser} csrfToken={csrfToken} />} />
          <Route path="/stories/:storyId/segments/:segmentId/edit" element={<ManageSegment story={sampleStories[0]} segment={sampleSegment} csrfToken={csrfToken} />} />
          <Route path="/stories/:storyId/segments/add" element={<ManageSegment story={sampleStories[0]} csrfToken={csrfToken} />} />
          <Route path="/login" element={<Login csrfToken={csrfToken} />} />
          <Route path="/register" element={<Register csrfToken={csrfToken} />} />
          <Route path="/edit-profile" element={<EditProfile currentUser={currentUser} csrfToken={csrfToken} />} />
          <Route path="/password-reset-request" element={<PasswordResetRequest csrfToken={csrfToken} />} />
          <Route path="/reset-password/:token" element={<PasswordReset csrfToken={csrfToken} />} />
          <Route path="/logout" element={<Logout />} />
          {/* Add more routes as needed */}
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
