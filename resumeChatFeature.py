import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid


# utility functions
def generate_thread_function():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_function()
    st.session_state['thread_id']=thread_id
    add_threads(thread_id=thread_id)
    st.session_state['message_history']=[]

def add_threads (thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return (chatbot.get_state(config={"configurable": {"thread_id": st.session_state["thread_id"]}}).values['messages'])

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
if "thread_id" not in st.session_state:
    st.session_state["thread_id"]=generate_thread_function()
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_threads(st.session_state['thread_id'])

CONFIG = {
    "configurable": {
        "thread_id": st.session_state["thread_id"]
    }
}



# add side bar
st.sidebar.title('LangGraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My Conversation') 

for threads in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(f"{threads}\n"):
        st.session_state['thread_id']=threads
        messages=load_conversation(thread_id=threads)

        temp_message=[]
        
        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_message.append({'role':role,'content':message.content})
        
        st.session_state['message_history']= temp_message

# Display previous messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# User input
user_input = st.chat_input("Type Here")


if user_input:

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    # Stream AI response
    with st.chat_message("assistant"):

        response = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input)
                    ]
                },
                config=CONFIG,
                stream_mode="messages"
            )
            if message_chunk.content
        )

    # Save AI response
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": response
    })
    
    
    
# is me aik feature add karna hai short chat answer ka usay uuid ki jagah my converstation me show karwana hai