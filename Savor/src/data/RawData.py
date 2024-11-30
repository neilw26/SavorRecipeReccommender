import json
import pandas as pd
import numpy as np
import requests


api_key = '55293aab311f449d851ab9345505eebf'

url = 'https://api.spoonacular.com/recipes/complexSearch'


def get_recipes(count, offset):

    # Set parameters
    params = {
    'apiKey': api_key,
    'number': count,  # Number of random recipes to retrieve
    'addRecipeNutrition': 'true',
    'addRecipeInformation': 'true',
    'offset': offset
    }

    response = requests.get(url, params=params)
    return response.json()


def main():
    off = 0
    recipe_list = []
    k = 0
    while off<1000:
        try:
            # get 100 recipes
            recipes = get_recipes(100,off)
            #print(recipes)
            #add to list of previous requests
            recipe_list.extend(recipes['results'])
            off+=100
            k+=1
            print(off)
            
        except KeyError as e:
            print('daily limit reached')
            break

    file_path = "/Users/melody_pogo/Desktop/OMSA/CSE 6242/Project/data/data/Spoonacular_Raw.json"
     
    
    with open(file_path, "w") as file:
        json.dump({"recipes": recipe_list}, file, indent = 4)
    print("success")
    

if __name__ == "__main__":
    main()
