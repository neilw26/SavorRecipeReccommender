def vectorize_data(data):
    from sentence_transformers import SentenceTransformer
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    combined_text = data['title'] + " " + data['Ingredients']

    vectors = model.encode(combined_text.tolist())

    return vectors

def create_lancedb_db(data, num_recipes_recommended=10):
    '''
    Creates lancedb database of top 10 recommended recipes to be passed into LLM.

    Args:
        data (pandas dataframe): output from data_clean_func() in 01_data_clean.py

    Returns:
        lancedb (database object): name of lancedb database that contains top 10 recipes
    '''
    import lancedb

    # filter to only top N
    data = data.head(num_recipes_recommended)

    db = lancedb.connect('recipes_lancedb')

    # delete old table
    #db.drop_table("recipes_table")

    # vectorize data
    vectors = vectorize_data(data)

    data = [{'id': i, 
             'vector': vector.tolist(), 
             'recipe_name': row.title, 
             'ingredients': row.Ingredients} 
             for i, (row, vector) in enumerate(zip(data.itertuples(), vectors))]

    # overwrite table each time
    db.create_table("recipes_table", data)

    return db
