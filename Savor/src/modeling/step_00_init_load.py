def init_load():
    '''
    Function to initialize all the variables for pipeline run
    '''
    print("Initializing load...")
    from neo4j import GraphDatabase
    from sentence_transformers import SentenceTransformer
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import pandas as pd
    import json
    global common_pantry, low_calorie_threshold, driver, gpt_model, tokenizer, data, pantry, UI, model

    ### define global variables
    common_pantry = ['salt', 'pepper', 'oil', 'olive oil', 'vegetable oil', 'butter']
    low_calorie_threshold = 200

    # Neo4j connection setup
    uri = "neo4j+s://7facb574.databases.neo4j.io"  # Replace with your actual URI
    username = "neo4j"  # Replace with your actual username
    password = "vio9r1hK66PJZjXEfPtM1Y5KZE0fhj7d6C2SCxvsq40"  # Replace with your actual password
    driver = GraphDatabase.driver(uri, auth=(username, password))

    # Initialize the LLM connection
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model_name = "EleutherAI/gpt-neo-125M"
    gpt_model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    ### import data
    # import clean Spoonacular data
    data = pd.read_csv("src/modeling/data/Clean.csv")

    # import pantry data
    with open("src/modeling/data/Full_Ingredients.csv", encoding='utf-8', errors='replace') as f:
        pantry = pd.read_csv(f)

    # read in UI inputs from JSON file
    with open ('src/modeling/data/output.json', 'r') as file:
        UI = json.load(file)

    return data, pantry, UI, common_pantry