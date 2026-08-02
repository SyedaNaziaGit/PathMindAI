import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

#loading env vars
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATION_STACK_API_KEY = os.getenv("AVIATION_STACK_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

#defining groq llm 
def get_groq_llm():
    model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    return ChatGroq(model=model_name)

#defining gemini llm
def get_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )