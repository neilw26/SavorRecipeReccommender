# Getting Started with Savor

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
## Prerequisites
In order to run this app you will need to install python, flask, npm and node.js. You may use any IDE but visual studio code is reccommended.

Install node.js from here

https://nodejs.org/en

Install npm from here:

https://docs.npmjs.com/cli/v9/commands/npm-install

Install python from here:

https://www.python.org/downloads/

### After completing the above steps you can now download flask

Flask installation:

- Go to project directory after cloning this repo
- run this command: pip install flask flask-cors



## Running Savor

#### `npm i`

Run this command to download all the dependencies for the project

 Then n the project directory, you can run:

#### `npm start`

Runs the app.

Open [http://localhost:3000](http://localhost:3000) after running this command to view it in your browser.

This will also start the flask backend which will show up under the link [http://127.0.0.1:5000](http://127.0.0.1:5000).

## How to use Savor

Click on the upper left "Diet & Nutrition" section to select any Nutrition Preferences, Dietary Restrictions, Cost per Serving, and Zip Code. 

Click on the upper right "My Pantry" section to select items that are in the user's pantry and would not need to be purchased before cooking. The user can select an entire category (ex. Herbs & Spices) or use the drop down arrow to select specific items per category (ex. Garlic Powder, Mint, etc.). 

The central "what are we feeling..." search bar allows the user to select a specific type of cuisine, or leave it blank. 

Below the search bar, the user should select either "Use What I Have" or "Purchase Items" to signal if they're willing to purchase ingredients not in their pantry.

After confirming selections, the user should press the magnifying glass icon next to the search bar.

Once the model has finished running, it will output recipes that fit the criteria ranked from highest to lowest Spoonacular score. This score takes into account quality of ingredients, popularity of the recipe, and nutritional value. 

## Modeling workflow

There are 6 different scripts that are run in to produce the desired output of recommended recipes. Below is an explanation of each script and how they are interact:

* app.py: this script is the main interaction point between the front-end (user interface) and back-end (modeling scripts). The process_data() function is run each time the user submit their input to the website. This function contains the code to pull the output from the user interface (the dietary restrictions, nutrition information, ingredients in their pantry, among other things), it then sends that output through the modeling pipeline, and finally it returns the output from the modeling pipeline (a JSON structured object of the 5 recipes that were recommended).

* step_05_run_all.py: this script organizes code from each functional part of the pipeline into one coherant function to then be run in the app.py script. 

* step_01_data_clean.py: this is the first step of the modeling pipeline. This step filters down the original 100MB+ recipes file to only include recipes that adhere to the individual's dietary, nutritional, and budgetary needs as well as includes recipes that have at least one ingredient that corresponds to the input pantry list that they included. 

* step_02a_build_lancedb.py: this script would be run if the user selected that they would like to "use what I have". This means that they are not open to buying other ingredients if possible. This strict sort of filtered dataset is then vectorized and loaded into a lancedb vector database. This database makes it possible for an LLM to query for the recipes.



## How the RAG Model Works

There are 6 different scripts that are run in to produce the desired output

When running programs in the "modeling" folder in order, some additional data filtering occurs (to determine if a recipe is high protein, low calorie, etc.) after loading in data and establishing a connection to Neo4j. 

A lancedb database and Neo4j database are created with the top 10 recommended recipes to be passed into the LLM.

The original query from the UI is added so that GPT-Neo knows what it is being asked. This includes if the user has any dietary restrictions and/or nutritional preferences.

GPT output is then generated. 

Output from the LLM is added to a dictionary.


## FAQ

#### Where does the data come from?

Recipes were pulled from the Spoonacular API into a json file (Raw.py). 
This file was manipulated to add nutrition and ingredient columns in a Python script (Clean.py) and exported to the "Clean.csv" excel file that is the starting file for the RAG model. 
