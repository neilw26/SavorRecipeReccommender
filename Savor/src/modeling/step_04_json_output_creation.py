# helper functions
def count_words_in_ingredients(ingredients, words):
    count = 0
    # Convert the ingredients text to lowercase to make the count case-insensitive
    ingredients = ingredients.lower()
    for word in words:
        count += ingredients.count(word.lower())  # Count each word's occurrences
    return count

# Function to split ingredients into two lists: found and not found in target
def split_ingredients(ingredients_str, target_ingredients):
    # Split the ingredients string into a list
    if isinstance(ingredients_str, str):
        # Remove square brackets, quotes, and any other unwanted characters
        ingredients_str = ingredients_str.replace("'", "").replace("[", "").replace("]", "")
        ingredients = [ingredient.strip() for ingredient in ingredients_str.split(",")]
    else:
        # If it's already a list, just strip any extra spaces from each ingredient
        ingredients = [ingredient.strip() for ingredient in ingredients_str]
    
    # Find ingredients in the target list
    in_target = [ingredient for ingredient in ingredients if ingredient in target_ingredients]
    
    # Find ingredients not in the target list
    not_in_target = [ingredient for ingredient in ingredients if ingredient not in target_ingredients]
    
    return (in_target, not_in_target)

def json_creation_func(recipes_output, UI):
    '''
    Take output from LLM and the calculated cost of each meal based on the multiplier and add to a dictionary.
    '''
    import pandas as pd
    from modeling.step_01_data_clean import data_clean_func
    import json
    
    data = pd.read_csv("modeling/data/recipes_sample_old.csv")

    # import pantry data
    with open("modeling/data/Full_Ingredients.csv", encoding='utf-8', errors='replace') as f:
        pantry = pd.read_csv(f)

    # read in UI inputs from JSON file
    with open ('modeling/data/output.json', 'r') as file:
        UI = json.load(file)

    common_pantry = ['salt', 'pepper', 'oil', 'olive oil', 'vegetable oil', 'butter']

    clean_data = data_clean_func(data, pantry, UI, common_pantry, UI['recommendation_type'])

    if UI['recommendation_type'] == "I want to only use ingredients I have":
        recipe_names = recipes_output['Recipe Name'].tolist()

        # filter down original data to just the recipes that were output from model
        filtered_df = clean_data[clean_data['title'].isin(recipe_names)].drop('num_matches', axis=1)

    else:
        recipe_names = [recipe.split(",")[0].replace("Recipe: ", "").strip() for recipe in recipes_output]
    
        # filter down original data to just the recipes that were output from model
        filtered_df = clean_data[clean_data['title'].isin(recipe_names)]

    filtered_df['match_count'] = filtered_df['Ingredients'].apply(lambda x: count_words_in_ingredients(x, UI['Ingredients']))

    # "ingredients they have" and "ingredients they need" columns creation
    filtered_df[['Ingredients_in_pantry', 'Ingredients_not_in_pantry']] = filtered_df['Ingredients'].apply(lambda x: pd.Series(split_ingredients(x, UI['Ingredients'])))

    # columns to display
    columns = ['title', 'Ingredients', 'Calories', 'Protein', 'Fat', 'pricePerServing', 'servings', 'sourceUrl', 'spoonacularScore', 'match_count', 'Ingredients_in_pantry', 'Ingredients_not_in_pantry']

    filtered_df = filtered_df[columns]

    return filtered_df.to_dict(orient='records')