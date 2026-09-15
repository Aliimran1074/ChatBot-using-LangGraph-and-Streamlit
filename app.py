import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage, AIMessage
import uuid
from backend import retrieveAllThreads


# Utility functions

def generate_thread_function():
    return str(uuid.uuid4())


def reset_chat():
    thread_id = generate_thread_function()

    st.session_state["thread_id"] = thread_id
    add_threads(thread_id)

    st.session_state["message_history"] = []


def add_threads(thread_id):
    thread_id = str(thread_id)

    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": str(thread_id)
            }
        }
    )

    return state.values.get("messages", [])


# Session State Initialization

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_function()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = [
        str(thread_id) for thread_id in retrieveAllThreads()
    ]

add_threads(st.session_state["thread_id"])


CONFIG = {
    "configurable": {
        "thread_id": st.session_state["thread_id"]
    }
}


# Sidebar

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

st.sidebar.header("My Conversations")

for thread in st.session_state["chat_threads"][::-1]:

    if st.sidebar.button(str(thread), key=f"thread_{thread}"):

        st.session_state["thread_id"] = str(thread)

        messages = load_conversation(thread)

        temp_message = []

        for message in messages:

            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                continue

            temp_message.append({
                "role": role,
                "content": message.content
            })

        st.session_state["message_history"] = temp_message

        st.rerun()


# Display Previous Messages

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# User Input

user_input = st.chat_input("Type Here")


if user_input:

    # Display User Message

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })


    # Stream AI Response

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


    # Save AI Response

    st.session_state["message_history"].append({
        "role": "assistant",
        "content": response
    })
