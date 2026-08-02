import asyncio
from graph_state import  TravelState
from mcp_clients import current_weather,forecast
from langchain_core.messages import AIMessage
from agents.helper import _llm_text,_json_from_llm


def itinerary_agent(state: TravelState):

    print("\n******************* ITINERARY AGENT INPUT *******************\n")
    print("Trip Constraints:")
    print(state.get("trip_constraints"))

    print("\nFlight Results:")
    print(state.get("flight_results"))

    print("\nHotel Results:")
    print(state.get("hotel_results"))

    print("\nWeather Results:")
    print(state.get("weather_results"))

    print("\nBudget Results:")
    print(state.get("budget_results"))
    print("==============================================================\n")

    prompt =  f"""
You are a practical travel designer. Your task is to synthesize the provided flight, hotel, weather, and budget constraints into a highly realistic, logical, day-by-day travel itinerary.

### INPUT DATA CONTEXT
* **User Query:** {state['user_query']}
* **Trip Constraints:** {state.get('trip_constraints', {})}
* **Flight Selection:** {state.get('flight_results', 'None selected')}
* **Hotel Selection:** {state.get('hotel_results', 'None selected')}
* **Weather Context:** {state.get('weather_results', 'No weather restrictions')}
* **Budget Limits/Allowances:** {state.get('budget_results', 'No budget restrictions')}

### CRITICAL LOGICAL RULES
1. **Pacing Rules:** Do not overpack days. Account for travel exhaustion on Day 1 and transit logistics on the final day.
2. **Weather Adaptive:** Align activities with the weather forecast. If heavy rain or extreme heat is predicted, shift to indoor museums, galleries, or indoor markets. 
3. **Budget Guardrails:** Ensure recommended attractions, dining styles, and transit options stay strictly within the daily allowance defined in the budget results.
4. **Geographic Flow:** Group activities by neighborhood or proximity to the hotel to minimize unnecessary cross-town travel time.

### OUTPUT FORMAT
Provide a clean, scannable draft using this exact markdown structure:

### 🗺️ Trip Overview
* **Destination & Duration:** [City, Country | X Days, Y Nights]
* **Base Camp:** [Hotel Name, with brief note on its location/vibe]
* **Theme/Pace:** [e.g., Relaxed, Action-Packed, Weather-Adjusted Cultured]

### ✈️ Transit Logistics
* **Arrival:** [Flight details, arrival time, and practical airport transfer recommendation]
* **Departure:** [Flight details, departure time, and when to head to the airport]

### 📅 Day-by-Day Schedule

#### Day 1: Arrival & Orientation
* **Morning/Afternoon:** [Flight arrival, hotel check-in, low-key exploration near hotel]
* **Evening:** [Welcome dinner matching budget tier; light neighborhood walk]

[Repeat for middle days using the format below]
#### Day X: [Thematic Title, e.g., Historic District Exploration]
* **Morning:** [Specific landmark or area; clear transport method from hotel]
* **Afternoon:** [Lunch neighborhood + secondary nearby activity; weather-safe option if needed]
* **Evening:** [Dinner recommendation style + night activity or relaxation]

#### Day N: Departure Day
* **Morning:** [Souvenir shopping or final café visit near hotel; checkout logistics]
* **Afternoon:** [Head to airport based on departure timing]

### 💡 Practical Review Notes
* **Weather Note:** [Why you scheduled specific days indoors/outdoors based on the forecast]
* **Budget Compliance:** [Confirmation of how this layout honors the calculated daily allowance]
"""
    result = _llm_text(
        "You are an expert itinerary planner and structural travel designer. Your role is to transform raw travel data into a flawless, immersive day-by-day narrative. You build plans around geographic logic, balancing optimal pacing with weather alerts, budget boundaries, and intuitive local transit strategies.",
        prompt
    )
    print("\n******************* ITINERARY OUTPUT *******************\n")
    print(result)
    print("===========================================================\n")
    
    #To get the approval request:
    approval_request = f"""
Please review this draft travel plan.
{result}
Reply with approval or feedback.
"""

    return {
        "itinerary": result,
        "approval_request": approval_request,
        "messages": [AIMessage(content= f"✨ **Draft Itinerary Prepared for Your Review**\n\nI have synthesized your flights, hotel choice, real-time weather data, and budget limits into a logistically optimized day-by-day experience layout below.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
