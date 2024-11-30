def generate_prompt_neo4j(recipes):
    """
    Generate a query prompt for the LLM to pick 5 recipes from the returned ones.
    """
    from neo4j import GraphDatabase
    # Start building the prompt string
    prompt = "I have the following recipes with their match count, total ingredients, and likes. Please pick the top 5 recipes based on these factors:\n"

    # Add each recipe's details into the prompt
    for recipe in recipes:
        prompt += f"Recipe: {recipe['recipe']}, Match Count: {recipe['matchCount']}, Total Ingredients: {recipe['totalIngredients']}, Likes: {recipe['likes']}\n"

    # Add the instruction for the LLM to pick the top 5
    prompt += "\nPlease list the names of the 5 recipes you would recommend, with one recipe per line (no additional information)."

    return prompt

def query_llm_for_recipes_neo4j(formatted_prompt):
    """
    Use the GPT-Neo model to process the prompt and pick the top 5 recipes.
    """
    from neo4j import GraphDatabase
    model_name = "EleutherAI/gpt-neo-125M"
    from transformers import AutoModelForCausalLM, AutoTokenizer
    gpt_model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # Tokenize the input prompt
    inputs = tokenizer(formatted_prompt, return_tensors="pt")

    # Generate output from the model
    output = gpt_model.generate(
        inputs['input_ids'], 
        max_length=1000,       # Adjust max_length based on your prompt size
        num_return_sequences=1,
        temperature=0.7,  # Increase temperature for more diversity in the response
        do_sample=True   # Ensures randomness
    )

    # Decode the output to get the response text
    result = tokenizer.decode(output[0], skip_special_tokens=True)

    # Post-processing: Split by lines and filter duplicates if needed
    # Post-processing: Split by lines, remove unwanted parts (e.g., extra prompt or empty lines)
    recommended_recipes = result.split("\n")
    recommended_recipes = [line.strip() for line in recommended_recipes if line.strip() and "Recipe:" in line]

    # Limit to 5 unique recipes
    recommended_recipes = list(set(recommended_recipes))  # Remove duplicates
    recommended_recipes = recommended_recipes[:5]  # Limit to top 5 recipe

    return recommended_recipes
