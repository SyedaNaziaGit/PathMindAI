import asyncio
from graph_state import  TravelState
from mcp_clients import list_airports,list_airlines
from agents.helper import _llm_text,_json_from_llm
from langchain_core.messages import  AIMessage

def flight_agent(state: TravelState):
    user_query = state["user_query"]
    constraints = state["trip_constraints"]
    destination = constraints["destination"]

    print("\n******************* FLIGHT AGENT INPUT *******************\n")
    print("Query:", user_query)
    print("Constraints:", constraints)
    print("==========================================================\n")

    airports = asyncio.run(list_airports(destination, limit=10))
    airlines = asyncio.run(list_airlines("", limit=10))

    print("\n*******************AIRPORT MCP DATA *******************\n")
    print(airports)
    print("===========================================================\n")

    print("\n******************* AIRLINE MCP DATA *******************\n")
    print(airlines)
    print("===========================================================\n")
    
    prompt = f"""
            You are an expert travel assistant specializing in flight logistics and route optimization. Your task is to generate a comprehensive, highly scannable flight guidance report based on the user's request and the provided dataset.

### INPUT DATA
<user_query>
{user_query}
</user_query>

<trip_constraints>
{constraints}
</trip_constraints>

<airport_data>
{airports}
</airport_data>

<airline_data>
{airlines}
</airline_data>

### OUTPUT REQUIREMENTS
Structure your response exactly as follows. Use short, punchy sentences (under 10 words where possible) and functional emojis as visual anchors.

# ✈️ Flight Guidance Report

## 🛫 Recommended Airports
* **Departure Options**: [List 1-2 most likely departure airports with codes based on data]
* **Arrival Options**: [List 1-2 most likely arrival airports with codes based on data]
* **Selection Logic**: [1-sentence explanation of why these airports fit the constraints]

## 🛩️ Flight Logistics & Airlines
* **Key Carriers**: [List relevant airlines from the dataset serving this route]
* **Estimated Duration**: [Provide expected flight duration, noting if direct or connecting]
* **Route Dynamics**: [1 sentence on frequency or typical layover hubs if applicable]

## 💰 Budget & Timing
* **Estimated Fare Range**: [Provide a realistic price range based on constraints/season]
* **Seasonality Alert**: [State peak season months and potential price surges for this route]

## 📅 Strategic Booking Advice
* **Booking Window**: [When to buy tickets, e.g., 2-3 months out]
* **Best Days**: [Cheapest days to fly or book for this specific route]
* **Constraint Alignment**: [How this itinerary specifically satisfies the user's unique constraints]
            
        """
        
    result = _llm_text("You are a flight planning specialist.",prompt)
    print("\n******************* FLIGHT AGENT OUTPUT *******************\n")
    print(result)
    print("=============================================================\n")
    return {
        "flight_results": result,
        "messages": [AIMessage(content="Flight agent process completed.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }