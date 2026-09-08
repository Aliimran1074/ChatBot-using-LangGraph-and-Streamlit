from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from typing import TypedDict,Literal,Annotated
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage
from dotenv import load_dotenv
load_dotenv()
model  =ChatOpenAI()
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph.message import add_messages
class chatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
    


def chatFunction (state=chatState):
    messages=state['messages']
    response =model.invoke(messages)
    return {'messages':[response]}



checkPointer = MemorySaver()
graph = StateGraph(chatState)

#  
graph.add_node('chatNode',chatFunction)
graph.add_edge(START,'chatNode')
graph.add_edge('chatNode',END)
chatbot=graph.compile(checkpointer=checkPointer)

for message_chunk, metadata in chatbot.stream(
    {
        "messages": [
            HumanMessage(content="Cricket World Cup 2011 Team Pakistan")
        ]
    },
    config={
        "configurable": {
            "thread_id": "1"
        }
    },
    stream_mode="messages"
):
    print(message_chunk.content)

    if message_chunk.content:
        print(message_chunk.content, end=" ", flush=True)

    
# print(type(stream))