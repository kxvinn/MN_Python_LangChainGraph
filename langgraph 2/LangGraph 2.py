import os
import re
import json

from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph

# hide API key
from dotenv import load_dotenv

load_dotenv("api_key.env")

key = os.getenv("GROQ_API_KEY")

# configure the AI model
model = "mixtral-8x7b-32768"
chat = ChatGroq(model_name=model)

# function to check if the question is mathematical
def check_question(question):
    pattern = r'[\d+\-*/=]'
    return bool(re.search(pattern, question))

# receptor node to receive, validate, and forward the question to the Virtual Teacher
def receptor(state):
    question = state["question"]
    if not check_question(question):
        return {"error": "The question does not seem to be mathematical."}
    
    return {"question": question, "category": "mathematics"}

# virtual Teacher node to generate the response
def virtual_teacher(state):
    question = state["question"]
    messages = [ 
        SystemMessage(content="You are a math teacher specializing in calculus, algebra, and geometry. Explain each solution clearly, step by step, focusing on every detail."),
        HumanMessage(content=question)
    ]
    response = chat.invoke(messages)
    return {"question": question, "category": "mathematics", "response": response.content}

# final node to return the graph's final state
def end_node(state):
    return state

# create the LangGraph graph
graph = StateGraph(dict)

# add nodes to the graph
graph.add_node("receptor", receptor)
graph.add_node("virtual_teacher", virtual_teacher)
graph.add_node("end", end_node)  # Adding the final node

# define the entry point
graph.set_entry_point("receptor")

# create connections between the nodes
graph.add_edge("receptor", "virtual_teacher")
graph.add_edge("virtual_teacher", "end")

# compile and execute the graph
teacher = graph.compile()
question = input("Enter your math question: ")

response = teacher.invoke({"question": question})

# ask the user if they want the JSON format output
choice = input("Do you want the response in JSON format? (yes/no): ").strip().lower()

if choice == "yes":
    print(json.dumps(response, indent=2, ensure_ascii=False))
else:
    print("Response:", response.get("response", "No response generated."))
