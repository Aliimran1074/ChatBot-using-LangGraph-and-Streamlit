import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage


CONFIG = {
    "configurable": {
        "thread_id": "1"
    }
}


if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


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