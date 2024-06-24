# imports from langchain package
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
llm = OpenAI(openai_api_key=OPENAI_API_KEY) # Language Model
chat_model = ChatOpenAI(openai_api_key=OPENAI_API_KEY) # Another LLM interface
# use llm.predict to get the answer
question = "What is this?"
answer = llm.predict(question).strip()
print(question)
print(answer)
# use chat_model.predict to get the answer
answer = chat_model.predict(question).strip()
print(question)
print(answer)