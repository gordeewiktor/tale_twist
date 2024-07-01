import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './CreateStory.css';

const CreateStory = ({ currentUser }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [genre, setGenre] = useState('');
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission logic, including validation
    const newErrors = {};

    if (!title) newErrors.title = 'Title is required';
    if (!description) newErrors.description = 'Description is required';
    if (!genre) newErrors.genre = 'Genre is required';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
    } else {
      // Submit form data (example logic)
      console.log({ title, description, genre });
      // Redirect or update state after submission
      navigate('/stories');
    }
  };

  if (!currentUser.isAuthenticated) {
    return (
      <div>
        <p>
          You must be logged in to create stories. Please <a href="/login">login</a> or <a href="/register">register</a> if you don't have an account.
        </p>
      </div>
    );
  }

  return (
    <div>
      <h2>Create a New Story</h2>
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
          <label className="form-label" htmlFor="description">Description</label>
          <textarea
            id="description"
            className="form-control"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          {errors.description && <div className="alert alert-danger">{errors.description}</div>}
        </div>
        <div className="form-group">
          <label className="form-label" htmlFor="genre">Genre</label>
          <input
            type="text"
            id="genre"
            className="form-control"
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
          />
          {errors.genre && <div className="alert alert-danger">{errors.genre}</div>}
        </div>
        <input type="submit" value="Create Story" className="btn btn-primary" />
      </form>
    </div>
  );
};

export default CreateStory;
