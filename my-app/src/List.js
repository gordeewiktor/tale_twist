import React from 'react';

function List({ items, onDeleteItem, onEditItem }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>
          {item}
          <button onClick={() => onEditItem(index)}>Edit</button>
          <button onClick={() => onDeleteItem(index)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}

export default List;
