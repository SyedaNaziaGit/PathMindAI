import asyncio
import json
from typing import Any

from langchain_core.messages import SystemMessage , AIMessage, HumanMessage
#for HITL - using  interrupt from types
from langgraph.types import interrupt
from graph_state import  TravelState
from config import get_groq_llm, get_gemini_llm

#LLM models
groq_llm = get_groq_llm()
#gemini_llm = get_gemini_llm()
#llm
#llm = get_gemini_llm() 
llm = get_groq_llm()
#to check the llm text
def _llm_text(system:str,prompt : str) -> str:
    response = llm.invoke([
            SystemMessage(content = system),
            HumanMessage(content = prompt)
        ])
    return response.content

#converting the text  in readable form
def  _json_from_llm(text:str) -> dict:
    print("\n========== RAW LLM RESPONSE ==========")
    print(text)
    start = text.index("{")
    end = text.rindex("}") + 1
    json_text = text[start:end]
    print("\n========== JSON Response from LLM ==========")
    print(json_text)
    return json.loads(json_text)



