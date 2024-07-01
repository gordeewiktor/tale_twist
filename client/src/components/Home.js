import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = ({ stories = [], currentUser }) => {
  return (
    <div>
      <h2>Available Stories</h2>
      <ul>
        {stories.map(({ story, firstSegmentId }) => (
          <li key={story.id}>
            {currentUser.isAuthenticated && currentUser.id === story.authorId ? (
              <Link to={`/manage-story/${story.id}`}>
                {story.title} - Manage
              </Link>
            ) : firstSegmentId ? (
              <Link to={`/read-story/${story.id}/${firstSegmentId}`}>
                {story.title}
              </Link>
            ) : (
              <>
                {story.title}
                <Link to={`/add-segment/${story.id}`}>(Add first segment)</Link>
              </>
            )}
          </li>
        ))}
      </ul>
      {currentUser.isAuthenticated && (
        <p>
          <Link to="/create-story">Create a New Story</Link>
        </p>
      )}
    </div>
  );
};

export default Home;
