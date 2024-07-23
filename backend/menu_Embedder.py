from openai import OpenAI
from models import MenuItem
from config import db, app
import os
import numpy as np
from dotenv import load_dotenv
from scipy.spatial.distance import cosine

load_dotenv()
# Load .env file

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def generate_and_store_embeddings(): # 
    menu_items = MenuItem.query.all()
    for item in menu_items:
        item_text = f"{item.name}: {item.description}, Category: {item.category}, Price: ${item.price}"
        
        response = client.embeddings.create(
            input=item_text,
            model="text-embedding-3-small"
        )
        item.embedding = response.data[0].embedding
        db.session.commit()
        print("Embeddings generated and stored successfully.")

def get_relevant_menu_items(question, top_n=5):
    response = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    )
    question_embedding = response.data[0].embedding

    menu_items = MenuItem.query.all()
    similarities = []
    for item in menu_items:
        similarity = 1 - cosine(question_embedding, item.embedding)
        similarities.append((similarity, item))

    similarities.sort(reverse=True, key=lambda x: x[0])
    relevant_items = [item for _, item in similarities[:top_n]]
    return relevant_items

if __name__ == '__main__':
    with app.app_context():
        generate_and_store_embeddings()
    