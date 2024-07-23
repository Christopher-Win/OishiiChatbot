from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from openai import OpenAI
from config import app, db
from models import MenuItem
import os
from dotenv import load_dotenv
from menu_Embedder import get_relevant_menu_items

load_dotenv()
# Load .env file

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key) # create an OpenAI client with the API key from the .env file

migrate = Migrate(app, db) # create a migration object for the Flask app and the database connection so that we can run migrations from the command line

@app.route('/menu', methods=['GET'])
def get_menu():
    menu = MenuItem.query.all()
    return jsonify([{'name': item.name, 'description': item.description, 'price': item.price, 'category': item.category} for item in menu])

@app.route('/ask', methods=['GET','POST'])
def ask_question(): # this function will be called when a POST request is made to /ask
    data = request.json # get the JSON data from the request
    question = data.get('question') # get the 'question' key from the JSON data

    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    # Retrieve relevant menu items based on the question. RAG model will be used to generate the answer.
    print(question,'\n')
    relevant_items = get_relevant_menu_items(question)
    menu_context = "\n".join([f"{item.name}: {item.description}, Category: {item.category}, Price: ${item.price}" for item in relevant_items])
    
    prompt = f"Here is the menu for a restaurant with items followed by various information about each item:\n{menu_context}\n\nNow, can you please tell me: {question}"
    print(prompt)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a very knowledgable and experienced restaurant server."},
            {"role": "user", "content": prompt}
    ])
    
    answer = response.choices[0].message.content 
    print(answer)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)