import React, { useState } from 'react';
import List from './List';
import './App.css';

function App() {
  const [newItem, setNewItem] = useState('');
  const [items, setItems] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(null);

  const handleInputChange = (e) => {
    setNewItem(e.target.value);
  };

  const handleAddItem = () => {
    if (newItem.trim() !== '') {
      if (isEditing) {
        const updatedItems = items.map((item, index) =>
          index === currentIndex ? newItem : item
        );
        setItems(updatedItems);
        setIsEditing(false);
        setCurrentIndex(null);
      } else {
        setItems([...items, newItem]);
      }
      setNewItem('');
    }
  };

  const handleDeleteItem = (index) => {
    const newItems = items.filter((_, i) => i !== index);
    setItems(newItems);
  };

  const handleEditItem = (index) => {
    setNewItem(items[index]);
    setIsEditing(true);
    setCurrentIndex(index);
  };

  return (
    <div className="App">
      <h1>Hello World</h1>
      <input
        type="text"
        value={newItem}
        onChange={handleInputChange}
        placeholder="Add a new item"
      />
      <button onClick={handleAddItem}>
        {isEditing ? 'Update' : 'Add'}
      </button>
      <List items={items} onDeleteItem={handleDeleteItem} onEditItem={handleEditItem} />
    </div>
  );
}

export default App;
