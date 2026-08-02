from typing import Annotated, Any,TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

#Defining State
class TravelState(TypedDict,total = False):
    #user related
    messages : Annotated[list[AnyMessage],add_messages]
    user_id : str
    user_query : str

    #gaurdrails for super agent related
    trip_constraints : dict[str,Any]
    selected_agents : list[str]
    supervisor_reasoning : str
    
    #hotel, flight, budget, iternary, weather agents related
    flight_results : str
    hotel_results : str
    weather_results : str
    budget_results : str
    itinerary : str
    
    #HITL related
    approval_request : str
    human_feedback : str
    approved : bool
    
    #final agent related
    final_response : str
    
    llm_calls : int