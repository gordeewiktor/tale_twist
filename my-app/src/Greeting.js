// src/Greeting.js
import React, { useState } from 'react';
import './Greeting.css';

function Greeting() {
  const [message, setMessage] = useState('Hello, World!');

  const changeMessage = () => {
    setMessage('You clicked the button!');
  };

  return (
    <div className="greeting-container">
      <h1 className="greeting">{message}</h1>
      <button onClick={changeMessage}>Click Me</button>
    </div>
  );
}

export default Greeting;
