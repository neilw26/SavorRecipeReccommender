import React, { useState } from 'react';
import './RecipeFinder.css';
import Pantry from './pantry';
import Narrow from './narrow';
import SavorLogo from './images/savorlogo.png';
import pantryButton from './images/PantryButton.png';
import narrowButton from './images/NutritionButton.png';
import searchButton from './images/Magnifier.png';
import loading from './images/loading-gif.gif'
import axios from 'axios';

const RecipeFinder = () => {
  
  const [isPantryOpen, setIsPantryOpen] = useState(false);
  const [isNarrowOpen, setIsNarrowOpen] = useState(false);
  const [filteredFoodTypes, setFilteredFoodTypes] = useState([]);
  const [recommendedRecipes, setRecommendedRecipes] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [searchOption, setSearchOption] = useState('useWhatIveGot');
  const [expandedIndex, setExpandedIndex] = useState(null);


  const foodTypes = [
    'Italian', 'Japanese', 'Korean', 'Spanish', 'Jewish', 'Mediterranean',
    'Barbecue', 'bbq', 'Greek', 'Vietnamese', 'Scottish', 'Central American',
    'American', 'Creole', 'Cajun', 'Caribbean', 'Nordic', 'Thai', 'Asian',
    'Indian', 'Eastern European', 'European', 'English', 'German', 'British',
    'Chinese', 'Southern', 'Latin American', 'Mexican', 'Middle Eastern',
    'French', 'Irish', 'Scandinavian', 'South American'
  ];

  const togglePantry = () => {
    setIsPantryOpen(!isPantryOpen);
  };

  const toggleNarrow = () => {
    setIsNarrowOpen(!isNarrowOpen);
  };

  const handleSearchChange = (event) => {
    const term = event.target.value;
    setSearchTerm(term);

    const filteredTypes = foodTypes.filter((type) =>
      type.toLowerCase().includes(term.toLowerCase())
    );
    setFilteredFoodTypes(filteredTypes);
  };

  const handleSelectCuisine = (cuisine) => {
    setSearchTerm(cuisine);
    setFilteredFoodTypes([]);
    setIsFocused(false);
    console.log(`Selected cuisine: ${cuisine}`);
  };

  const handleFocus = () => {
    setIsFocused(true);
    setFilteredFoodTypes(foodTypes);
  };

  const handleBlur = () => {
    setTimeout(() => setIsFocused(false), 100);
  };



  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    const recipes = [
      { name: 'Grilled Chicken Salad', ingredients: ['chicken', 'lettuce', 'tomato'] },
      { name: 'Vegetable Stir Fry', ingredients: ['tofu', 'carrot', 'broccoli'] },
      // Add more recipes
    ];
    const samplejson = [{
      title: "Turkish Chicken Salad with Home-made Cacik Yogurt Sauce",
      Ingredients: "['carrot', 'cucumber', 'garlic', 'pickled cucumbers / gherkins', 'jalapeno peppers', 'juice of lemon', 'lebanese cucumber', 'lemon juice', 'i gem lettuce', 'olive oil', 'parsley', 'cabbage', 'onion', 'roast chicken', 'salt & pepper', 'tomatoes', 'yoghurt']",
      Calories: 643,
      Protein: 67,
      Fat: 30,
      pricePerServing: 447.82,
      servings: 4,
      sourceUrl: "https://www.foodista.com/recipe/XYFWSH25/a-turkish-inspired-chicken-salad-with-tomato-cucumber-red-onion-salsa-charred-green-peppers-and-home-made-cacik-delicious-and-healthy",
      spoonacularScore: 95.7654800415039,
      match_count: 1,
      Ingredients_in_pantry: [
          "onion"
      ],
      Ingredients_not_in_pantry: [
          "carrot",
          "cucumber",
          "garlic",
          "pickled cucumbers / gherkins",
          "jalapeno peppers",
          "juice of lemon",
          "lebanese cucumber",
          "lemon juice",
          "i gem lettuce",
          "olive oil",
          "parsley",
          "cabbage",
          "roast chicken",
          "salt & pepper",
          "tomatoes",
          "yoghurt"
      ]
  }]



    ///////////////////////////////////////
    // CODE TO COME UP WITH THE LIST OF RECPIES WILL GO HERE
    ///////////////////////////////////////
    // const filteredRecipes = recipes.filter((recipe) =>
    //   recipe.name.toLowerCase().includes(searchTerm.toLowerCase())
    // );
    //setRecommendedRecipes(samplejson);
    
    sendDataToPython();

  };
  
  const sendDataToPython = async () => {
    setRecommendedRecipes(null);
    try {
      const response = await axios.post('http://127.0.0.1:5000/process_data', 
        {"Nutrition" : window.nutrition,
          "Dietary Restrictions" : window.dietaryRestrictions,
          "Cost": window.cost,
          "Ingredients": window.selectedItems,
          "Zipcode": window.zipcode,
          "recommendation_type": searchOption,
          "Calories": window.Calories

        }
      );
      console.log('Response from Python:', response.data);
      response.data = response.data.map((recipe) => {
        recipe.Ingredients = JSON.parse(recipe.Ingredients.replace(/'/g, '"'));
        return recipe;
      });
      console.log(response.data);
    
      setRecommendedRecipes(response.data);
    } catch (error) {
      console.error('Error sending data to Python:', error);
    }
    
  };

  const handleOptionChange = (event) => {
    setSearchOption(event.target.value);
  };
  

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <div className={`recipe-finder ${isPantryOpen ? 'shrink' : ''}`}>
      <div className="title-section">
        <img src={SavorLogo} alt= "Savor Logo" className="savor-logo"/>
      </div>

      <div className="pantry">
        <img src={pantryButton} alt="My Pantry" className="pantry" onClick={togglePantry}/>
      </div>

      <Pantry isOpen={isPantryOpen} onClose={togglePantry} />

      <div className="narrow">
        <img src={narrowButton} alt="Narrow" onClick={toggleNarrow} />
      </div>
      <Narrow isOpen={isNarrowOpen} onClose={toggleNarrow} />
      <div className={`background-overlay ${isNarrowOpen ? 'show' : ''}`} onClick={toggleNarrow}></div>

      <div className="search">
        <input
          type="text"
          className="search-bar"
          placeholder="What are we feeling..."
          value={searchTerm}
          onChange={handleSearchChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
        />
        <button className="search-button" onClick={handleSubmit}>
          <img src={searchButton} alt="Search" />
        </button>
      </div>
      <div className='outer-suggestions-box'>
      {isFocused && filteredFoodTypes.length > 0 && (
        <div className="suggestions-box">
          {filteredFoodTypes.map((type, index) => (
            <div
              key={index}
              className="suggestion-item"
              onMouseDown={() => handleSelectCuisine(type)}
            >
              {type}
            </div>
          ))}
        </div>
      )}
      </div>

      <div className='searchOptions'>
        <label>
          <input
            type = 'radio'
            value = "I want to only use ingredients I have"
            checked = {searchOption === "I want to only use ingredients I have"}
            onChange = {handleOptionChange}
          />
          Use What I Have
        </label>
        <label>
          <input
            type = 'radio'
            value = 'UsePurchase'
            checked = {searchOption === 'UsePurchase'}
            onChange = {handleOptionChange}
          />
          Purchase Items
        </label>
      </div>
      {recommendedRecipes === null && (
    <div className='loadingwheel'>
  <img src={loading} alt="Loading..." />
  </div>
)}
      {recommendedRecipes && recommendedRecipes.length > 0 && (
        <div className="recipe-results">
          {recommendedRecipes.map((recipe, index) => (
            <div key={index} className="recipe-card">
              <h1
                onClick={() => toggleExpand(index)}
                className="recipe-title"
              >
                {recipe.title} {expandedIndex === index ? "▲" : "▼"}
              </h1>
              {expandedIndex === index && (
                <div className="recipe-details">
                  <p><strong>Calories:</strong> {recipe?.Calories}</p>
                  <p><strong>Protein:</strong> {recipe?.Protein}g</p>
                  <p><strong>Fat:</strong> {recipe?.Fat}g</p>
                  <p><strong>Price Per Serving:</strong> ${recipe?.pricePerServing}</p>
                  <p><strong>Servings:</strong> {recipe?.servings}</p>
                  <p><strong>Spoonacular Score:</strong> {(parseFloat(recipe?.spoonacularScore) || 0).toFixed(2)}</p>
                  <p>
                    <strong>Source:</strong>{" "}
                    <a
                      href={recipe?.sourceUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      Recipe Link
                    </a>
                  </p>
                  <div className="ingredients-container">
                    <div className="ingredients-list">
                      <h2>Ingredients</h2>
                      <ul>
                        {recipe?.Ingredients?.map((ingredient, idx) => (
                          <li key={idx}>{ingredient}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="ingredients-list">
                      <h2>Ingredients in Pantry</h2>
                      <ul>
                        {recipe?.Ingredients_in_pantry?.map(
                          (ingredient, idx) => (
                            <li key={idx}>{ingredient}</li>
                          )
                        )}
                      </ul>
                    </div>
                    <div className="ingredients-list">
                      <h2>Ingredients Not in Pantry</h2>
                      <ul>
                        {recipe?.Ingredients_not_in_pantry?.map(
                          (ingredient, idx) => (
                            <li key={idx}>{ingredient}</li>
                          )
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};


export default RecipeFinder;
