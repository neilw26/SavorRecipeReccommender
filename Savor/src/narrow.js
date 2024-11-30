import React, { useState, useEffect, useRef } from 'react';
import './narrow.css';
import Select from 'react-select';

const Narrow = ({ isOpen, onClose }) => {

  const narrowRef = useRef(null);
  const [nutrition, setNutrition] = useState([]);
  const [dietaryRestrictions, setDietaryRestrictions] = useState([]);
  const [cost, setCost] = useState("5.00");
  const [displayCost, setDisplayCost] = useState("5.00");
  const [zipcode, setzipcode] = useState('');
  const [ingredients, setIngredients] = useState([]);
  const [cuisine, setCuisine] = useState([]);
  const [recommendedRecipes, setRecommendedRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [calories, setCalories] = useState("1300");
  const [displayCalories, setDisplayCalories] = useState("1300");

  //DEFAULT DROPDOWN
  const nutritionOptions = [
    { value: 'low-carb', label: 'Low Carb' },
    { value: 'high-protein', label: 'High Protein' },
    { value: 'low-fat', label: 'Low Fat' },
    // Add more options as needed
  ];

  const dietaryOptions = [
    { value: 'vegan', label: 'Vegan' },
    { value: 'vegetarian', label: 'Vegetarian' },
    { value: 'gluten-free', label: 'Gluten Free' },
    { value: 'dairy-free', label: 'Dairy Free' },
    // Add more options as needed
  ];


  const handleSubmit = () => {
    const recipes = [
      { name: 'Grilled Chicken Salad', ingredients: ['chicken', 'lettuce', 'tomato'] },
      { name: 'Vegetable Stir Fry', ingredients: ['tofu', 'carrot', 'broccoli'] },
      // Add more recipes
    ];
    ///////////////////////////////////////
    // CODE TO COME UP WITH THE LIST OF RECPIES WILL GO HERE
    ///////////////////////////////////////
    setRecommendedRecipes(recipes);
  };

  const handleRecipeClick = (recipe) => {
    setSelectedRecipe(recipe);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (narrowRef.current && !narrowRef.current.contains(event.target)) {
        onClose();
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown',handleClickOutside);
    };
  }, [isOpen,onClose]);

  // Handle slider change
  const handleCostChange = (e) => {
    const newCost = parseFloat(e.target.value).toFixed(2);
    setCost(newCost);
    setDisplayCost(e.target.value);
  };

  const handleCalChange = (e) => {
    const newCalories = parseInt(e.target.value);
    setCalories(newCalories);
    setDisplayCalories(e.target.value);
  }

  // Handle text input change as string to FLOAT
  const handleFloatChange = (e) => {
    e.target.value = e.target.value.replace(/[^0-9.]/g, '');
    const inputValue = e.target.value
    setDisplayCost(inputValue);
    const numericValue = parseFloat(inputValue);
    if (/^\d*\.?\d*$/.test(inputValue)) {
      setCost(inputValue);
    }
    if (inputValue === ''){
      setCost("5.00");
      return
    }
    if(parseFloat(e.target.value) > 13.00){
      setCost("13.00");
    }
    else if(parseFloat(e.target.value) < 0){
      setCost("0");

    }
  };
  // Handle text input change as string to INTEGER
  const handleIntChange = (e) => {
    e.target.value = e.target.value.replace(/[^0-9]/g, '');
    const inputValue = e.target.value
    setDisplayCalories(inputValue);
    const numericValue = parseInt(inputValue);
    if (/^\d*\.?\d*$/.test(inputValue)) {
      setCost(inputValue);
    }
    if (inputValue === ''){
      setCost("1300");
      return
    }
    if(parseFloat(e.target.value) > 13.00){
      setCost("1300");
    }
    else if(parseFloat(e.target.value) < 0){
      setCost("13");

    }
  };  
  // Handle zip code input
  const handlezipcodechange = (e) => {
    const inputvalue = e.target.value;
    if (/^\d{0,5}$/.test(inputvalue)) {
      setzipcode(inputvalue);
    }
  };
  //global variable setting
  //console.log(cost,nutrition,dietaryRestrictions);
  window.cost = cost;
  window.calories = calories;
  const nutritionformatted = {};
  nutrition.forEach(item => {
    nutritionformatted[item.value] = true;
  });
  window.nutrition = nutritionformatted;
  const dietrest = {};
  dietaryRestrictions.forEach(item => {
    dietrest[item.value] = true;
  });
  window.dietaryRestrictions = dietrest;
  window.zipcode = zipcode;


  return (
    <div ref={narrowRef} className={`narrow-menu ${isOpen ? 'open' : ''}`}>
      
      <h3>What are we looking for in this meal?</h3>
      
      <div className="dropdown-section">
        <label>Nutrition</label>
        <Select
        isMulti
          options={nutritionOptions}
          value={nutrition}
          onChange={setNutrition}
          placeholder="Select nutrition preferences"
        />

        <label>Dietary Restrictions</label>
        <Select
          isMulti
          options={dietaryOptions}
          value={dietaryRestrictions}
          onChange={setDietaryRestrictions}
          placeholder="Select dietary restrictions"
        />
        <label>Calories: {parseFloat(calories).toFixed(0)}</label>
        <div className='slider-input-container'>
          <input
            type="range"
            min="13"
            max="1300"
            step="1"
            value={calories}
            onChange={handleCalChange}
            className='cal-slider'
          />
          <input
            type="text"
            value={displayCalories}
            onChange={handleIntChange}
            className='cal-input'
          />
        </div>
        
        <label>Cost: ${parseFloat(cost).toFixed(2)}</label>
        <div className="slider-input-container">
          <input
            type="range"
            min="0.00"
            max="13.00"
            step="0.01"
            value={cost}
            onChange={handleCostChange}
            className="cost-slider"
          />
          <input
            type="text"
            value={displayCost}
            onChange={handleFloatChange}
            className="cost-input"
          />
        </div>

        <label>Zip Code</label>
        <input
          type="text"
          value={zipcode}
          onChange={handlezipcodechange}
          placeholder="What's your Zip?"
          className='zip-code-input'
          maxLength={5}
          />
      </div>
    </div>
  );
};

export default Narrow;