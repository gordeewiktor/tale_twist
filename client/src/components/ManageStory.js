import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './ManageStory.css';

const ManageStory = ({ story, segments, currentUser, csrfToken }) => {
  const navigate = useNavigate();

  const handleDeleteSegment = (segmentId) => {
    if (window.confirm('Are you sure you want to delete this segment?')) {
      // Perform deletion logic here
      console.log(`Delete segment with ID: ${segmentId}`);
      // Example: You might send a DELETE request to your backend API
      // fetch(`/api/stories/${story.id}/segments/${segmentId}`, { method: 'DELETE', headers: { 'X-CSRFToken': csrfToken } });
    }
  };

  const handleDeleteStory = () => {
    if (window.confirm('Are you sure you want to delete this story? All segments will be deleted.')) {
      // Perform deletion logic here
      console.log('Delete story with ID:', story.id);
      // Example: You might send a DELETE request to your backend API
      // fetch(`/api/stories/${story.id}`, { method: 'DELETE', headers: { 'X-CSRFToken': csrfToken } });
      navigate('/stories');
    }
  };

  if (!currentUser.is_authenticated || currentUser.id !== story.author_id) {
    return <p>You do not have permission to edit this story.</p>;
  }

  return (
    <div>
      <h2>Manage Story: {story.title}</h2>
      <div className="segments">
        {segments.map((segment) => (
          <div id={`segment-${segment.id}`} key={segment.id} className="segment">
            <h3>{segment.title}</h3>
            <p>{segment.content.slice(0, 150)}</p>
            <div className="choices">
              <p>Choices:</p>
              {segment.choices.length > 0 ? (
                <ul>
                  {segment.choices.map((choice) => (
                    <li key={choice.id}>
                      {choice.next_segment_id ? (
                        <a href={`#segment-${choice.next_segment_id}`} className="choice-link">
                          {choice.text}
                        </a>
                      ) : (
                        choice.text
                      )}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>The segment has no choices.</p>
              )}
            </div>
            <Link to={`/stories/${story.id}/segments/${segment.id}/edit`} className="btn btn-info">
              Edit Segment
            </Link>
            <button
              onClick={() => handleDeleteSegment(segment.id)}
              className="btn btn-danger"
            >
              Delete Segment
            </button>
          </div>
        ))}
        <Link to={`/stories/${story.id}/segments/add`} className="btn btn-success">
          Add New Segment
        </Link>
      </div>
      <button onClick={handleDeleteStory} className="btn btn-danger">
        Delete Story
      </button>
      <Link to="/stories" className="btn btn-secondary">
        Back to Stories
      </Link>
    </div>
  );
};

export default ManageStory;
