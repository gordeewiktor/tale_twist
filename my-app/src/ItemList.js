import React from 'react';
import Item from './Item'; // Import the new component

function ItemList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <Item key={index} item={item} /> // Use the new component
      ))}
    </ul>
  );
}

export default ItemList;
