import json
from typing import List, Literal, Optional
from config import get_gemini_llm
from pydantic import BaseModel,Field
from langchain_core.prompts import ChatPromptTemplate
from graph_state import  TravelState
from agents.helper import _llm_text,_json_from_llm
from langchain_core.messages import AIMessage

#allowed agents strictly
AgentType = Literal["flight_agent", "hotel_agent", "weather_agent", "budget_agent", "itinerary_agent"]

#Pydantic models for structured output

#Strcutured output for TripConstraints
class TripConstraints(BaseModel):
    destination: Optional[str] = Field(default="", description="The destination city/country. Empty if unknown.")
    origin: Optional[str] = Field(default="", description="The departure location. Empty if unknown.")
    duration: Optional[str] = Field(default="", description="Length of the trip (e.g., '5 days'). Empty if unknown.")
    budget: Optional[str] = Field(default="",description="Financial limits or price constraints. Empty if unknown.",)
    travel_style: Optional[str] = Field(default="",description="Vibe of the trip (e.g., luxury, solo). Empty if unknown.",)
    special_preferences: List[str] = Field(default_factory=list,description="List of specific needs like 'vegan food' or 'wheelchair accessible'.",)

#Structured output for the Supervisor output
class SupervisorOutput(BaseModel):
    selected_agents: List[AgentType] = Field(description="The subset of specialist agents required to handle this specific user request.")
    trip_constraints: TripConstraints = Field(description="Extracted parameters and constraints from the user request.")
    reasoning: str = Field(description="A brief explanation justifying why these specific agents were chosen based on the user's text.")


# supervisor agent with gaurdrail
def supervisor_agent(state:TravelState):
    
    user_query = state['user_query']
    #-------------------------------- INPUT GUARDRAIL------------------------------
    
    guardrail_prompt = f"""
You are a strict validation assistant. Analyze the user request below and determine if it is a valid travel planning request.

A request is VALID if it asks about:
- Booking or researching flights, hotels, trains, or car rentals.
- Creating itineraries, finding activities, or recommending places to visit.
- Travel logistics, packing tips, visa requirements, or local customs.

A request is INVALID if it is:
- Completely unrelated to travel (e.g., coding, math, general chatting).
- Explicitly malicious, unsafe, or violating standard safety guidelines.

Output MUST be strictly valid JSON. Do not include markdown formatting (like ```json), code blocks, or any conversational text before or after the JSON.

JSON Format:
{{
    "allowed": true or false,
    "reason": "A concise explanation of why the request is allowed or denied"
}}

User request:
{user_query}
"""

    guardrail_raw = _llm_text(
        "You are a strict input validation guardrail. Analyze the user request. Return strict JSON only",
        guardrail_prompt
    )

    print("\n******************* GUARDRAIL RAW RESPONSE *******************\n")
    print(guardrail_raw)
    print("=================================================================\n")

    guardrail_result = _json_from_llm(guardrail_raw)

    print("\n******************* GUARDRAIL PARSED RESPONSE *******************\n")
    print(json.dumps(guardrail_result, indent=2))
    print("==================================================================\n")

    if not guardrail_result.get("allowed", False):
        reason = guardrail_result.get(
            "reason",
            "Request rejected by input guardrail."
        )

        return {
            "selected_agents": [],
            "trip_constraints": {},
            "supervisor_reasoning": reason,
            "final_response": reason,
            "messages": [
                AIMessage(content=f"Guardrail blocked the request: {reason}")
            ],
            "llm_calls": state.get("llm_calls", 0) + 1,
        }
    #------------------------Supervisor agent logic ----------------------------------
    #initializing llm model
    llm = get_gemini_llm()
    #to get the desired structured output using
    structured_llm = llm.with_structured_output(SupervisorOutput)
    
    #prompt using chat prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system",(
            "You are the expert supervisor of a real-world multi-agent travel planning system.\n"
            "Analyze the user's request, extract constraints, and pick only necessary specialist agents.\n\n"
            "Agent Selection Guide:\n"
            "- flight_agent: Use when flights, airports, airlines, or airfare are needed.\n"
            "- hotel_agent: Use when hotels, stays, neighborhoods, or accommodation are needed.\n"
            "- weather_agent: Use when weather, climate, packing lists, or forecasts are useful.\n"
            "- budget_agent: Use when budget limits, affordability, or costs are mentioned.\n"
            "- itinerary_agent: Use for producing the structured, daily travel schedule.\n\n"
            "Rules:\n"
            "1. Only select agents strictly required by the context of the user request.\n"
            "2. Extract constraints accurately. Map missing ones to empty strings or empty lists."
        
            )),
        ("user","{user_query}")
    ])
    #chaining it for execution
    supervisor_chain = prompt | structured_llm
    parsed: SupervisorOutput = supervisor_chain.invoke({"user_query": user_query})
    # Returning updated state format natively
    return {
        "selected_agents": parsed.selected_agents,
        "trip_constraints": parsed.trip_constraints.model_dump(),  # serializing to dictionary
        "supervisor_reasoning": parsed.reasoning,
        "messages": [AIMessage(content="Supervisor agent process completed.")],
        # Tracking LLM iteration increments
        "llm_calls": state.get("llm_calls", 0) + 1,
    }