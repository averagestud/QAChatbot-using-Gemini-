from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY="Your API key goes here."

# In this chatbot I am using Gemini Pro API to create a simple conversational chatbot
import streamlit as st
import os 
import google.generativeai as genai
genai.configure(api_key=os.getenv(GOOGLE_API_KEY))

# function to load gemini
model=genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response= chat.send_message(question, stream=True)
    return response

# Initialising the streamlit app to run the model
st.set_page_config(page_title="Q&A Chatbot")
st.header("Chatbot using Gemini Pro")

# Initialize the session to store history of the chat performed with the chatbot
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]
    
# Generate greeting so as to greet the user.
greet = model.generate_content("Hi!")
st.write("Bot:", greet.text)


# Take the input for the query from the user
input=st.text_input("Input: ", key="input")
submit=st.button("Ask the question to be answered")

# As soon as the user submits the input we will generate a response for the user
if submit and input:
    response = get_gemini_response(input)
    
    # Add user query and the bot response to the chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The response is:")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The chat history is:")

for role,text in st.session_state['chat_history']:
    st.write(f"{role} : {text}")

 
