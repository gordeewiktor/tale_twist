import React from 'react';
import { Link } from 'react-router-dom';
import './ReadStory.css';

const ReadStory = ({ story, segment, choices, currentUser }) => {
  return (
    <div>
      {segment.is_first ? (
        <h2>{story.title}</h2>
      ) : (
        <h2>{segment.title}</h2>
      )}
      <p>{segment.content}</p>

      <h3>{choices && choices.length > 0 ? 'Make a Choice' : 'The End'}</h3>

      {choices && choices.length > 0 && (
        <ul>
          {choices.map((choice, index) => (
            <li key={index}>
              {choice.next_segment_id ? (
                <Link to={`/read-story/${story.id}/${choice.next_segment_id}`}>{choice.text}</Link>
              ) : (
                choice.text
              )}
            </li>
          ))}
        </ul>
      )}

      {currentUser.is_authenticated && currentUser.id === story.author_id && (
        <div>
          <p><Link to={`/add-segment/${story.id}`}>Add a new segment</Link></p>
          <p><Link to={`/edit-segment/${segment.id}/${story.id}`}>Edit This Segment</Link></p>
          <p><Link to={`/manage-story/${story.id}`}>Edit Story</Link></p>
        </div>
      )}
    </div>
  );
};

export default ReadStory;
