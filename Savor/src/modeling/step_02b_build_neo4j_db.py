# Function to insert data into vectordb
def delete_existing_data():
    from neo4j import GraphDatabase

    uri = "neo4j+s://7facb574.databases.neo4j.io"  # Replace with your actual URI
    username = "neo4j"  # Replace with your actual username
    password = "vio9r1hK66PJZjXEfPtM1Y5KZE0fhj7d6C2SCxvsq40"  # Replace with your actual password
    driver = GraphDatabase.driver(uri, auth=(username, password))

    with driver.session() as session:
        # delete existing data
        session.run("MATCH (n) DETACH DELETE n")

def insert_data(row):
    from neo4j import GraphDatabase
    uri = "neo4j+s://7facb574.databases.neo4j.io"  # Replace with your actual URI
    username = "neo4j"  # Replace with your actual username
    password = "vio9r1hK66PJZjXEfPtM1Y5KZE0fhj7d6C2SCxvsq40"  # Replace with your actual password
    driver = GraphDatabase.driver(uri, auth=(username, password))

    ingredients = row["Ingredients"][1:-1].split(", ")  # Split ingredients into a list
    query = """
    MERGE (r:Recipe {name: $title})  // Use recipe name as the unique identifier (ensures that the recipe is unique by its name)
    ON CREATE SET r.likes = $spoonacularScore // Set the likes property only if new recipe is created (?)
    WITH r // Pass the `r` (recipe) variable to the next part of the query
    UNWIND $Ingredients AS ingredientName // Unwinds the list of ingredients so we can process each ingredient individually
    MERGE (i:Ingredient {name: ingredientName}) // Ensures that each ingredient is unique
    MERGE (r)-[:CONTAINS]->(i) // Creates a relationship between the recipe and the ingredient
    """

    # Correct parameter names to match the query
    parameters = {
        "title": row["title"],  # Corrected to match the query parameter name
        "spoonacularScore": int(row["spoonacularScore"]),  # Corrected to match the query parameter name
        "Ingredients": ingredients  # Corrected to match the query parameter name
    }

    with driver.session() as session:
        session.run(query, parameters)


# Function to recommend recipes
def recommend_recipes(ingredients, limit=20):
    from neo4j import GraphDatabase

    uri = "neo4j+s://7facb574.databases.neo4j.io"  # Replace with your actual URI
    username = "neo4j"  # Replace with your actual username
    password = "vio9r1hK66PJZjXEfPtM1Y5KZE0fhj7d6C2SCxvsq40"  # Replace with your actual password
    driver = GraphDatabase.driver(uri, auth=(username, password))

    query = """
    MATCH (r:Recipe)-[:CONTAINS]->(i:Ingredient)
    WITH r, COUNT(i) AS matchCount, COUNT(DISTINCT i) AS totalIngredients, r.likes AS likes
    RETURN r.name AS recipe, matchCount, totalIngredients, likes
    ORDER BY matchCount DESC, likes
    LIMIT 10;
    """

    parameters = {"ingredients": ingredients, "limit": limit}

    with driver.session() as session:
        result = session.run(query, parameters)

        # Convert the result into a list immediately to avoid consuming it prematurely
        records = [record for record in result]  # Fully consume the result and store it in `records`

    recipes = [{"recipe": record["recipe"], "matchCount": record["matchCount"], "totalIngredients": record["totalIngredients"], "likes": record["likes"]} for record in records]
    return recipes

def create_neo4j_db(df, ingredients, limit=10):

    delete_existing_data()
    df.apply(insert_data, axis=1)
    print("Data successfully inserted in Neo4j.")

    recommended_recipes = recommend_recipes(ingredients, limit=10)

    return recommended_recipes
