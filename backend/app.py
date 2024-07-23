from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from openai import OpenAI
from config import app, db
from models import MenuItem
import os
from dotenv import load_dotenv

load_dotenv()
# Load .env file

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key) # create an OpenAI client with the API key from the .env file




@app.route('/menu', methods=['GET'])
def get_menu():
    menu = MenuItem.query.all()
    return jsonify([{'name': item.name, 'description': item.description} for item in menu])

@app.route('/ask', methods=['GET','POST'])
def ask_question(): # this function will be called when a POST request is made to /ask
    data = request.json # get the JSON data from the request
    question = data.get('question') # get the 'question' key from the JSON data

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    print(question,'\n')
    menu_items = MenuItem.query.all() # get all menu items from the database
    menu_context = "\n".join([f"{item.name}: {item.description}" for item in menu_items])

    prompt = f"Here is the menu for a restaurant with items followed by their descriptions:\n{menu_context}\n\nQuestion: {question}"
    print(prompt)
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a knowledgable and careful restaurant waiter."},
        {"role": "user", "content": prompt}
    ])
    
    answer = response.choices[0].message.content 
    print(answer)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)