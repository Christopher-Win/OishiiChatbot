import streamlit as st
import requests

st.title('Menu Chatbot')

# Input for the user question
question = st.text_input('Ask about ingredients or get suggestions:')

if st.button('Ask'):
    if question:
        try:
            headers = {'Content-Type': 'application/json'}  # Add necessary headers here
            # Send the question to the backend API
            response = requests.get('http://127.0.0.1:5000/ask', json={'question': question}, headers=headers) 
            print(response)
            if response.status_code == 200:
                answer = response.json().get('answer', 'No answer available')
            else:
                answer = 'Sorry, something went wrong with the request.'
        except Exception as e:
            answer = f'An error occurred: {e}'
        
        # Display the response from the API
        st.write('Response:')
        st.write(answer)
    else:
        st.write('Please enter a question.')

# Display the menu items
if st.button('Show Menu'):
    try:
        menu_response = requests.get('http://127.0.0.1:5000/menu')
        if menu_response.status_code == 200:
            menu_items = menu_response.json()
            st.write('Menu Items:')
            st.json(menu_items)  # Write the JSON response to the screen
        else:
            st.write('Sorry, something went wrong with the request.')
    except Exception as e:
        st.write(f'An error occurred: {e}')
