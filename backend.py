from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from typing import TypedDict,Literal,Annotated
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage
from dotenv import load_dotenv
load_dotenv()
model  =ChatOpenAI()
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3


conn = sqlite3.connect('chatbot.db',check_same_thread=False)
checkPointer = SqliteSaver(conn=conn)

class chatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
    


def chatFunction (state=chatState):
    messages=state['messages']
    response =model.invoke(messages)
    return {'messages':[response]}



graph = StateGraph(chatState)

#  
graph.add_node('chatNode',chatFunction)
graph.add_edge(START,'chatNode')
graph.add_edge('chatNode',END)
chatbot=graph.compile(checkpointer=checkPointer)

def retrieveAllThreads():
    all_threads = set()
    for checkpoint in checkPointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return (list(all_threads))
# for message_chunk, metadata in chatbot.stream(
#     {
#         "messages": [
#             HumanMessage(content="Cricket World Cup 2011 Team Pakistan")
#         ]
#     },
#     config={
#         "configurable": {
#             "thread_id": "1"
#         }
#     },
#     stream_mode="messages"
# ):
    # print(message_chunk.content)

    # if message_chunk.content:
    #     print(message_chunk.content, end=" ", flush=True)

# CONFIG = {
#     "configurable": {
#         "thread_id": "thread_1"
#     }
# }

# response= chatbot.invoke(
# {"messages": [HumanMessage(content="What is my Name")]},
#     config=CONFIG,
#     stream_mode="messages")

# print (response)

# print(chatbot.get_state(config=CONFIG).values['messages']) 
# print(type(stream))