import os
import sqlite3
from typing import TypedDict, List, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

load_dotenv(override=True)

# sqlite connection
sqlite= sqlite3.connect("chat_checkpoint.sqlite", check_same_thread=False)
memory= SqliteSaver(sqlite)


# LLM
def get_groq_llm():
    return ChatOpenAI(
        model= "openai/gpt-oss-120b",
        base_url= "https://api.groq.com/openai/v1",
        api_key= os.getenv("GROQ_API_KEY"),
        model_kwargs= {"temperature": 0.7},
        max_tokens= 1000,
        )
    
llm= get_groq_llm()


# Chat State
class ChatState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Agent
def agent(state: ChatState):
    messages= state['messages']
    response= llm.invoke(messages)
    return {'messages': [response]}

# Langgraph workflow
graph= StateGraph(ChatState)

graph.add_node('agent', agent)
graph.set_entry_point('agent')
graph.add_edge('agent', END)
app= graph.compile(checkpointer=memory)

config = {"configurable": {"thread_id": 2}}


# Inference

while True:
    user_input= input("User: ")
    if user_input.lower() in ['exit', 'end', 'quit']:
        break
    else:
        result=app.invoke({'messages': [HumanMessage(content= user_input)]}, 
                            config=config)
        print('AI:' +(result['messages'][-1].content))
