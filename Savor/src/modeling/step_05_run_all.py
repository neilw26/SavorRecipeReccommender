def run_all(data, pantry, UI, common_pantry):
    '''
    Run each file's function(s) and save output to JSON script
    '''
    # load in all necessary libraries
    from neo4j import GraphDatabase
    import pandas as pd
    from modeling.step_00_init_load import init_load
    from modeling.step_01_data_clean import data_clean_func
    from modeling.step_02a_build_lancedb import create_lancedb_db
    from modeling.step_02b_build_neo4j_db import create_neo4j_db
    from modeling.step_03a_llm_call_lancedb import user_input_flags, generate_query_lancedb, data_setup_lancedb, generate_recipe_recommendations, format_results_to_json_lance_db, get_recipe_recommendations, format_recommendations_lancedb
    from modeling.step_03b_llm_call_neo4j import generate_prompt_neo4j, query_llm_for_recipes_neo4j
    from modeling.step_04_json_output_creation import count_words_in_ingredients, split_ingredients, json_creation_func

    # initialize all variables
    # data = pd.DataFrame()
    # pantry = pd.DataFrame()
    # UI = {}
    # UI['recommendation_type'] = "dummy variable"
    # common_pantry = []
    # environment = init_load()
    # UI = environment[2]

    # clean data
    clean_data = None
    # if UI['recommendation_type'] != "dummy variable":
    clean_data = data_clean_func(data, pantry, UI, common_pantry, UI['recommendation_type'])
    # else:
        # print("Bypassing data cleaning because of dummy variable")

    # conditional logic to bypass parts of the function you don't need yet
    recommended_recipes = None
    if clean_data is not None:
        # choose which function to run dependent on what the user selects in the UI
        if UI['recommendation_type'] == "I want to only use ingredients I have":
            db = create_lancedb_db(clean_data)
            recommended_recipes = format_recommendations_lancedb(get_recipe_recommendations(UI, db))
        elif UI['recommendation_type'] == "dummy variable":
            print("Data did not load in correctly. Using dummy data.")
        else:
            recipes = create_neo4j_db(clean_data, UI['Ingredients'], limit=50)
            recommended_recipes = query_llm_for_recipes_neo4j(generate_prompt_neo4j(recipes))

    # Format output ready for UI (only if recipes were successfully created)
    if recommended_recipes is not None:
        return json_creation_func(recommended_recipes, UI)

# run_all()
