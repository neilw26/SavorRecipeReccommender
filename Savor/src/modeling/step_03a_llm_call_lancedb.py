# helper function(s)
def user_input_flags(UI):
    '''
    Creates flags based on user's inputs to feed into prompt for LLM.
    '''
    # test nutrition
    restriction_list = 'Dietary Restrictions'
    if restriction_list in UI.keys():
        restrictions = list(UI[restriction_list].keys())
        gluten_free_flag = 'does' if 'gluten-free' in restrictions else 'does not'
        vegan_flag = 'does' if 'vegan' in restrictions else 'does not'
        vegetarian_flag = 'does' if 'vegetarian' in restrictions else 'does not'
    
    nutrition_needs = 'Nutrition'
    if nutrition_needs in UI.keys():
        nutrition = list(UI[nutrition_needs].keys())
        high_protein_flag = 'is' if 'high-protein' in nutrition else 'is not'
        low_carb_flag = 'is' if 'low-carb' in nutrition else 'is not'
        low_fat_flag = 'is' if 'low-fat' in nutrition else 'is not'

    return gluten_free_flag, vegan_flag, vegetarian_flag, high_protein_flag, low_carb_flag, low_fat_flag
            

def generate_query_lancedb(ingredients, UI):

    user_restrictions_flags = user_input_flags(UI)

    # Add the original query to ensure GPT-Neo knows what it's being asked
    full_prompt = f"""
    Given that the individual {user_restrictions_flags[1]} follow a vegan diet, {user_restrictions_flags[2]} follow a vegetarian diet, {user_restrictions_flags[0]} follow a gluten-free diet,
    {user_restrictions_flags[3]} looking for a high-protein diet, {user_restrictions_flags[5]} looking for a low-fat diet, 
    {user_restrictions_flags[4]} looking for a low-carb diet,
    what are the top 5 recipes that should be recommended to the consumer based on the ingredients {ingredients} that they already have?
    """
    
    return full_prompt

def data_setup_lancedb(db):
    '''
    Fetch recipes from LanceDB based on the ingredients and dietary restrictions.
    '''
    # Assuming the db has a 'recipes_table' with columns 'ingredients' and 'recipe_name'
    recipes_table = db['recipes_table']

    # Example of how to fetch all recipes (with ingredients and recipe_name)
    # Use the select() method to get all rows or filter the query if needed
    df = recipes_table.to_pandas()
    
    # Now df is a DataFrame containing all rows and columns from the recipes table
    # Filter out the columns you need, like 'recipe_name' and 'ingredients'
    recipe_data = df[['recipe_name', 'ingredients']].to_dict(orient='records')

    # Now pass the retrieved data to the LLM for processing
    return recipe_data


def generate_recipe_recommendations(recipes, ingredients, UI):
    '''
    Use GPT to generate recommendations based on the recipes retrieved from LanceDB.
    '''
    user_restrictions_flags = user_input_flags(UI)

    # Extract recipe names and ingredients
    recipe_details = "\n".join([f"Recipe: {recipe['recipe_name']}\nIngredients: {recipe['ingredients']}" for recipe in recipes])

    # Construct the prompt with the retrieved recipes and query ingredients
    full_prompt = f"""
    The individual has the following ingredients: {ingredients}.
    Dietary restrictions:
    - Vegan: {user_restrictions_flags[1]}
    - Vegetarian: {user_restrictions_flags[2]}
    - Gluten-Free: {user_restrictions_flags[0]}
    - High-Protein: {user_restrictions_flags[3]}
    - Low-Carb: {user_restrictions_flags[4]}
    - Low-Fat: {user_restrictions_flags[5]}
    
    Here are some recipes with ingredients: {recipe_details}. Based on the user's dietary restrictions and available ingredients, **rank the following recipes** in order of suitability (from the best match to the worst match). For each recipe, provide:
    1. The recipe name.
    2. A list of the ingredients.
    3. An explanation of why this recipe is a good match for the user (considering the ingredients and dietary preferences).

    Format the response like this:

    **1. Recipe Name: [Recipe Name]**
    Ingredients: [Ingredients]
    Why it’s a good match: [Explain why this recipe fits the user’s preferences]

    Do not include anything else. Only return the rankings and explanations.
    """
    model_name = "EleutherAI/gpt-neo-125M"
    from transformers import AutoModelForCausalLM, AutoTokenizer
    gpt_model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Tokenize the input prompt and generate the GPT output
    inputs = tokenizer(full_prompt, return_tensors="pt")
    output = gpt_model.generate(inputs['input_ids'], max_new_tokens=300, num_return_sequences=1)

    # Decode and return the result
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

def format_results_to_json_lance_db(results):
    '''
    Format the results into a JSON-friendly format.
    '''
    formatted_results = []
    
    for recipe in results:
        formatted_recipe = {
            "recipe_name": recipe.get('recipe_name', 'N/A'),
            "ingredients": recipe.get('ingredients', 'N/A'),
            "match_score": recipe.get('match_score', 'N/A'),
            "id": recipe.get('id', 'N/A')
        }
        formatted_results.append(formatted_recipe)

    return formatted_results


def get_recipe_recommendations(UI, db):
    '''
    Fetch recipes from LanceDB, generate a query and pass it to the LLM for recommendations.
    '''
    # Step 1: Generate the query for the language model
    ingredients = UI.get('Ingredients', [])
    query = generate_query_lancedb(ingredients, UI)

    # Step 2: Execute the query and get recipes from LanceDB
    recipes = data_setup_lancedb(db)

    # Step 3: Generate recipe recommendations using GPT
    recommendations = generate_recipe_recommendations(recipes, ingredients, UI)

    return recommendations

def format_recommendations_lancedb(input_recipes):
    import re
    import pandas as pd
    # Regular expression to capture the recipe names, ingredients and other details
    recipe_pattern = re.compile(r"Recipe: (.*?)\nIngredients: \[(.*?)\]", re.DOTALL)

    # Find all matches
    matches = recipe_pattern.findall(input_recipes)

    # Initialize an empty list to hold the structured data
    recipes = []

    # Iterate over the matches and structure the data
    for match in matches:
        recipe_name = match[0].strip()
        ingredients = match[1].strip().replace("'", "").replace("[", "").replace("]", "").split(", ")
        
        # Append the structured data to the recipes list
        recipes.append({"Recipe Name": recipe_name, "Ingredients": ingredients})

    # Create a pandas DataFrame from the structured data
    df = pd.DataFrame(recipes)

    # Display the DataFrame
    return df.head(5)