from graph_state import  TravelState
from agents.helper import _llm_text,_json_from_llm
from langchain_core.messages import  AIMessage


def final_agent(state: TravelState):

    print("\n******************* FINAL AGENT INPUT *******************\n")
    print("Approved:", state.get("approved"))
    print("Feedback:", state.get("human_feedback"))
    print("==========================================================\n")

    if state["approved"]:
        prompt = f"""
The human approved this draft itinerary.
Produce the final polished travel plan.
Draft itinerary:
{state['itinerary']}
Budget notes:
{state['budget_results']}
"""
    else:
        prompt = f"""
The human did not approve the draft.
Original user request:
{state['user_query']}
Draft itinerary:
{state['itinerary']}
Human feedback:
{state['human_feedback']}
Budget notes:
{state['budget_results']}
"""

    result = _llm_text(
    "You are an elite travel designer who revises draft itineraries by precisely applying human feedback and resolving logistical constraints to output a definitive, publication-grade, user-ready travel plan.",
    prompt
    )

    print("\n******************* FINAL RESPONSE *******************\n")
    print(result)
    print("========================================================\n")

    return {
        "final_response": result,
        "messages": [AIMessage(content=result)],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }