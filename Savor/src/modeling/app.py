# library imports for modeling code
import pandas as pd
import json
import re
from sentence_transformers import SentenceTransformer
import lancedb
from neo4j import GraphDatabase
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.modeling.step_00_init_load import init_load
from src.modeling.step_01_data_clean import data_clean_func
from src.modeling.step_02a_build_lancedb import create_lancedb_db
from src.modeling.step_02b_build_neo4j_db import create_neo4j_db
from src.modeling.step_03a_llm_call_lancedb import user_input_flags, generate_query_lancedb, data_setup_lancedb, generate_recipe_recommendations, format_results_to_json_lance_db, get_recipe_recommendations, format_recommendations_lancedb
from src.modeling.step_03b_llm_call_neo4j import generate_prompt_neo4j, query_llm_for_recipes_neo4j
from src.modeling.step_04_json_output_creation import count_words_in_ingredients, split_ingredients, json_creation_func

from flask import Flask, request, jsonify
from flask_cors import CORS
from src.modeling.step_05_run_all import run_all

data = pd.read_csv("src/modeling/data/Dataset.csv")

# import pantry data
with open("src/modeling/data/Full_Ingredients.csv", encoding='utf-8', errors='replace') as f:
    pantry = pd.read_csv(f)

common_pantry = ['salt', 'pepper', 'oil', 'olive oil', 'vegetable oil', 'butter']

with open ('src/modeling/data/output.json', 'r') as file:
    UI = json.load(file)

run_all(data, pantry, UI, common_pantry)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/process_data', methods=['POST'])
def process_data():
    ui_data = request.json #ui input
    result = run_all(data, pantry, ui_data, common_pantry) #do operation on the json object

    #returning the recipes 
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)