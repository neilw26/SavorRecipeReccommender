import json
import pandas as pd
import numpy as np

file_path = "/Users/melody_pogo/Desktop/OMSA/CSE 6242/Project/data/data/Spoonacular_Raw.json"

with open(file_path, 'r') as file:
    data = json.load(file)

    df = pd.DataFrame(data["recipes"])

df['Ingredients'] = np.nan
df["Protein"] = np.nan
df["Calories"] = np.nan
df["Fat"] = np.nan
df["Carbs"] = np.nan

cal = []
pro = []
fat = []
carb = []
big_ing_list = []
for index, row in df.iterrows():
    ingredients = []
    column = row["nutrition"]
    nutri = column['nutrients']
    ing = column['ingredients']
    for i in nutri:
        if i['name'] == 'Calories':
            cal.append(i['amount'])
        elif i['name'] == 'Protein':
            pro.append(i['amount'])
        elif i['name'] == 'Fat':
            fat.append(i['amount'])
        elif i['name'] == 'Carbohydrates':
            carb.append(i['amount'])
    for i in ing:
        ingredients.append(i['name'])
    big_ing_list.append(ingredients)

df['Ingredients'] = big_ing_list
df["Protein"] = pro
df["Calories"] = cal
df["Fat"] = fat
df["Carbs"] = carb

df.insert(0, 'title', df.pop('title'))
df.insert(1, 'Ingredients', df.pop('Ingredients'))
df.insert(2, 'Calories', df.pop('Calories'))
df.insert(3, 'Protein', df.pop('Protein'))
df.insert(4, 'Fat', df.pop('Fat'))
df.insert(5, 'Carbs', df.pop('Carbs'))


file_path2 = "/Users/melody_pogo/Desktop/OMSA/CSE 6242/Project/data/data/Dataset.csv"

df.to_csv(file_path2, index=False)
print("done")
