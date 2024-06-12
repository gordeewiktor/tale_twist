// frontend/src/App.js
import React from 'react';
import './App.css';
import Stories from './components/Stories';
import Register from './components/Register';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Tale Twist</h1>
      </header>
      <main>
        <Register />
        <Stories />
      </main>
    </div>
  );
}

export default App;
