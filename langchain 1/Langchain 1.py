import os
import re
import json

from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage

#hide API Key
from dotenv import load_dotenv

load_dotenv("api_key.env")

key = os.getenv("GROQ_API_KEY")



#   model name
mixtral = "mixtral-8x7b-32768"

#   generating virtual teacher
chat = ChatGroq(model_name=mixtral)

#   check if question is about math
def check_question(question):


#   expression to detect math operators
    pattern = r'[\d+\-*/=]'
    return bool (re.search(pattern,question))
    




#   set teacher's rules function
system_message = SystemMessage (
  content=(
  "You're a math teacher who specializes in helping studients with calculus, algebra and geometry problems."
    "explain every solution clearly and step by step, focusing on the minimum details. "
    )
)





#  teacher function
def ask_teacher(question):

#   sends the question to the teacher and returns the response

    messages = [system_message, HumanMessage(content=question)]
    response = chat.invoke(messages)
    return response.content

# question test
question = "How do I solve the equation: 2x + 3 = 7?"


# verify if the question hits the pattern for a mathematical solution.
if check_question(question):
    print(ask_teacher(question))

else:

    print("The question does not seem to be mathematical.")


# now, creating the communication with JSON

def process_question(question):

# processes the question, verifies if it's mathematical and return a JSON response.

    if not check_question(question):
        return json.dumps({"error":"The question does not seem to be mathematical. "})
    
    response = ask_teacher(question)
    return json.dumps({
        "question": question,
        "category": "mathematics",
        "response": response


    }, indent=2
)



show_output = input("Should I show the JSON output? (yes/no): ").strip().lower() 


if show_output in ["yes","y"]:
    
    
    
    print(process_question(question))

else:

    print("JSON output will not be shown.")
    


    



