import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Stories.css';  // Assuming you have a CSS file for styling

const Stories = () => {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('/api/stories')
      .then(response => {
        setStories(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching stories:', error);
        setError('Error fetching stories');
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1>Stories</h1>
      <ul>
        {stories.map(story => (
          <li key={story.id}>
            <h2>{story.title}</h2>
            <p>{story.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Stories;
