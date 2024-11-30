import React, { useState, useEffect, useRef } from 'react';
import './pantry.css';

const Pantry = ({ isOpen, onClose }) => {

  const [data, setData] = useState({});
  const [selectedItems, setSelectedItems] = useState({});
  const [openCategories, setOpenCategories] = useState({});
  const [searchTerm, setSearchTerm] = useState('');

  const pantryRef = useRef(null);

  useEffect(() => {
    fetch('/Pantry.csv')
      .then((response) => response.text())
      .then((csvText) => {
        //console.log(csvText);
        
        const rows = csvText.split('\n');
        //console.log(rows);
        rows.shift();
        const cleanedrows = rows.map(item => item.replace(/\r/g, ''));
        //console.log(cleanedrows);

        let datadict = {};
        for(let i of cleanedrows){
          const [category, item] = i.trim().split(',');
          //console.log(category, item) 
          if (!datadict[category]) {
            datadict[category] = {}; 
          }
          if (!datadict[category][item]) {
            datadict[category][item] = [];  
          }
        }
        setData(datadict);
      })
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (pantryRef.current && !pantryRef.current.contains(event.target)) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

 // Toggle category visibility
const toggleCategory = (category) => {
  setOpenCategories((prevState) => {
    const updatedCategories = {};
    for (let key in prevState) {
      updatedCategories[key] = prevState[key];
    }
    updatedCategories[category] = !prevState[category];
    return updatedCategories;
  });
};

// Handle item checkbox change
const handleItemChange = (category, item) => {
  setSelectedItems((prevState) => {
    const updatedItems = {};
    for (let cat in prevState) {
      updatedItems[cat] = { ...prevState[cat] };
    }
    if (!updatedItems[category]) {
      updatedItems[category] = {};
    }
    updatedItems[category][item] = !prevState[category]?.[item];
    return updatedItems;
  });
};

// Handle category checkbox change
const handleCategoryChange = (category) => {
  const categoryItems = data[category] || {};
  const allChecked = Object.keys(categoryItems).every((item) => selectedItems[category]?.[item]);

  setSelectedItems((prevState) => {
    const newState = {};
    for (let cat in prevState) {
      newState[cat] = { ...prevState[cat] };
    }

    for (let item in categoryItems) {
      if (!newState[category]) {
        newState[category] = {};
      }
      newState[category][item] = !allChecked;
    }
    return newState;
  });
};

// Handle search change and update open categories based on search term
const handleSearchChange = (e) => {
  const term = e.target.value.toLowerCase();
  setSearchTerm(term);
  if (!term) {
    setOpenCategories({});
    return;
  }
  const newOpenCategories = {};
  for (let category in data) {
    const categoryMatches = category.toLowerCase().includes(term);
    const itemMatches = Object.keys(data[category]).some((item) =>
      item.toLowerCase().includes(term)
    );
    if (categoryMatches || itemMatches) {
      newOpenCategories[category] = true;
    }
  }
  setOpenCategories(newOpenCategories);
};

  //console.log(selectedItems);
  //global variable and preparation
  const getIngredientsArray = () => {
    const ingredientsArray = Object.keys(selectedItems).flatMap(category => 
      Object.keys(selectedItems[category]).filter(item => selectedItems[category][item])
    );
    
    return ingredientsArray;
  };
  console.log(window.selectedItems);
  
  window.selectedItems = getIngredientsArray();

  return (
    <div ref={pantryRef} id="main_pantry" className={`pantry-menu ${isOpen ? 'open' : ''}`}>
      <h3 className='PantryTitle'>My Pantry</h3>
      <input
        className="PantrySearch"
        type="text"
        placeholder="Search for Categories or Items"
        value={searchTerm}
        onChange={handleSearchChange}
      />
      
      {Object.keys(data).map((category) => {
        const filteredItems = Object.keys(data[category]).filter(item => {
          return (
            category.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.toLowerCase().includes(searchTerm.toLowerCase())
          );
        });
       if (filteredItems.length === 0) return null;

        return (
        <div
          key={category}
          className={`category-container ${openCategories[category] ? 'active' : ''}`}
        >
          <div className="category-header">
            <h2>
              <input
                type="checkbox"
                className='category-checkbox'
                checked={Object.keys(data[category]).every((item) => selectedItems[category]?.[item])}
                onChange={() => handleCategoryChange(category)}
              />
              {category}
            </h2>
            <button
              onClick={() => toggleCategory(category)}
            >
              {openCategories[category] ? '▲' : '▼'}
            </button>
          </div>
          <div className={`items-container ${openCategories[category] ? 'open' : 'closed'}`}>
            {filteredItems.map((item) => (
                <div key={item}>
                  <h3>
                    <input
                      type="checkbox"
                      className='ingredient-checkbox'
                      checked={selectedItems[category]?.[item] || false}
                      onChange={() => handleItemChange(category, item)}
                    />
                    {item}
                    </h3>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default Pantry;
