### function that cleans the data and adds columns for user's inputs
def data_clean_func(data, pantry, UI, common_pantry, recommendation_type, low_calorie_threshold = 200, num_recipes_recommended=10):
    '''
    Cleans the data to include only user input preferences

    Args:
        data (pandas dataframe): cleaned dataset of all recipes
        pantry (pandas dataframe): dataframe featuring pantry items and ingredients matches
        user_input (dictionary): user's input from UI
        common_pantry (list of strings): list of items to be excluded from search when finding matches
        low_calorie_threshold (num): defaulted at 200 but able to be changed
        num_recipes_recommended (num): defaulted at 10 but able to be changed

    Returns:
        pandas dataframe: cleaned dataframe that contains only recipes that the user would potentially like
    '''
    #adapt the price per serving column to move the decimal point to the appropriate location, and then cutting off anything below "cents"
    data['pricePerServing'] = round(data['pricePerServing']/100 , 2)
    
    # TODO: do we need to do anything about the common_pantry input?
    # is it more important that that's displayed on the UI than being filtered behind the scenes?
    #print("data cleanfunc",data['Protein'])
    # create columns based on user's indicated nutrition
    # TODO: are we still doing "Low Calorie" and "Low Fat"?
    data['Calories from Protein'] = data['Protein']*4
    data['Calories from Fat'] = data['Fat']*9
    data['low-calorie'] = data['Calories'].apply(lambda x: x <= low_calorie_threshold)
    data['high-protein'] = data['Calories from Protein'] > (data['Calories']*.2)
    data['low-fat'] = data['Calories from Fat'] < (data['Calories']*.3)
    data['low-carb'] = data['Calories from Protein'] < (data['Calories']*.2)

    # filter based on user's dietary restrictions
    # renaming columns for dietary restrictions to match what is in the User Output from the UI
    data = data.rename(columns={'glutenFree': 'gluten-free', 'dairyFree': 'dairy-free'})
    #print("datapt2",data)
    restriction_list = 'Dietary Restrictions'
    if restriction_list in UI.keys() or restriction_list != {}:
        restrictions = list(UI[restriction_list].keys())
        for restriction in restrictions:
            data = data[data[restriction] == True]

    ### filter on user's nutritional needs
    nutrition_needs = 'Nutrition'
    if nutrition_needs in UI.keys() or nutrition_needs != {}:
        nutrition = list(UI[nutrition_needs].keys())
        for i in nutrition:
            data = data[data[i] == True]

    ### filter on user's selected cuisine
    selected_cuisine = 'Cuisine'
    if selected_cuisine in UI.keys():
        cuisine = list(UI[selected_cuisine].keys())
        for i in cuisine:
            data = data[data[i] == True]

    if recommendation_type == "I want to only use ingredients I have":
        ### reduce the pantry list down to just the ingredients that the user selected
        updated_pantry = pantry[pantry['Item'].isin(UI['Ingredients'])]
        #print(updated_pantry)
        # create list of all pantry items
        pantry_items = updated_pantry['Ingredient'].to_list()
        # Filter the DataFrame to just recipes that contain at least one ingredient
        matching_rows = []
        num_matches_list = []
        #print(data.iterrows())
        for index, row in data.iterrows():
            # number of matches
            num_matches = 0
            # Get the 'Ingredients' column (a string) for the current row
            ingredients = row['Ingredients']

            # Split the ingredients into a list of ingredients (split by ", ")
            ingredient_list = ingredients.split(", ")
            #print(ingredient_list)
            # Flag to check if there's any match
            match_found = False

            # Loop through each ingredient in the current row
            for ingredient in ingredient_list:
                # clean up around ingredients
                ingredient = ingredient.strip("'").strip("[").strip("]").strip("['").strip("']")
                #print("ingredient",ingredient)
                if ingredient in pantry_items:
                    num_matches += 1
                    match_found = True
                    # break  # No need to check further, we found a match

            # If a match was found, add the index to the list of matching rows
            if match_found:
                matching_rows.append(index)
                num_matches_list.append(num_matches)
        # Filter the DataFrame by the indices of the matching rows
        filtered_df = data.loc[matching_rows]
        filtered_df['num_matches'] = num_matches_list # no need to worry about matching up index because we've 
        # already removed rows that don't have a match and num_matches were added in sequential order to list

        # want to prioritize recipes that have more ingredients that match
        # then want to do a tie breaker with spoonacularScore
        filtered_df = filtered_df.sort_values(by=['num_matches', 'spoonacularScore'], ascending=[False, False])

        # filter out repeat recipes
        filtered_df = filtered_df.drop_duplicates(subset='title', keep='first', inplace=False)

    else:
        filtered_df = data.sort_values(by=['spoonacularScore'], ascending=[False])
        filtered_df = filtered_df.drop_duplicates(subset='title', keep='first', inplace=False).head(100)
    
    filtered_df = filtered_df.drop(['sustainable', 'lowFodmap', 
    'weightWatcherSmartPoints', 'gaps', 'preparationMinutes', 'cookingMinutes', 'healthScore', 'creditsText', 'license',
    'sourceName', 'readyInMinutes', 'summary', 'dishTypes', 'diets', 'occasions',
    'author'], axis=1)
    return filtered_df
