import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ManageSegment.css';

const ManageSegment = ({ story, segment, csrfToken }) => {
  const [title, setTitle] = useState(segment ? segment.title : '');
  const [content, setContent] = useState(segment ? segment.content : '');
  const [choiceText1, setChoiceText1] = useState(segment && segment.choices[0] ? segment.choices[0].text : '');
  const [nextSegmentId1, setNextSegmentId1] = useState(segment && segment.choices[0] ? segment.choices[0].next_segment_id : '');
  const [choiceText2, setChoiceText2] = useState(segment && segment.choices[1] ? segment.choices[1].text : '');
  const [nextSegmentId2, setNextSegmentId2] = useState(segment && segment.choices[1] ? segment.choices[1].next_segment_id : '');
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!title) newErrors.title = 'Title is required';
    if (!content) newErrors.content = 'Content is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      console.log({ title, content, choiceText1, nextSegmentId1, choiceText2, nextSegmentId2 });
      navigate(`/stories/${story.id}/manage`);
    }
  };

  const handleDelete = (e) => {
    e.preventDefault();
    if (window.confirm('Are you sure you want to delete this segment?')) {
      console.log('Delete segment with ID:', segment.id);
      navigate(`/stories/${story.id}/manage`);
    }
  };

  return (
    <div>
      <h2>{segment && segment.id ? 'Edit' : 'Add'} Segment for "{story.title}"</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label" htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            className="form-control"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          {errors.title && <div className="alert alert-danger">{errors.title}</div>}
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="content">Content</label>
          <textarea
            id="content"
            className="form-control"
            value={content}
            onChange={(e) => setContent(e.target.value)}
          />
          {errors.content && <div className="alert alert-danger">{errors.content}</div>}
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="choice_text_1">Choice Text 1</label>
          <input
            type="text"
            id="choice_text_1"
            className="form-control"
            value={choiceText1}
            onChange={(e) => setChoiceText1(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="next_segment_id_1">Next Segment ID 1</label>
          <input
            type="text"
            id="next_segment_id_1"
            className="form-control"
            value={nextSegmentId1}
            onChange={(e) => setNextSegmentId1(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="choice_text_2">Choice Text 2</label>
          <input
            type="text"
            id="choice_text_2"
            className="form-control"
            value={choiceText2}
            onChange={(e) => setChoiceText2(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="next_segment_id_2">Next Segment ID 2</label>
          <input
            type="text"
            id="next_segment_id_2"
            className="form-control"
            value={nextSegmentId2}
            onChange={(e) => setNextSegmentId2(e.target.value)}
          />
        </div>
        <button type="submit" className="btn btn-primary">{segment && segment.id ? 'Update' : 'Create'} Segment</button>
        {segment && segment.id && (
          <button onClick={handleDelete} className="btn btn-danger">Delete Segment</button>
        )}
      </form>
    </div>
  );
};

export default ManageSegment;
