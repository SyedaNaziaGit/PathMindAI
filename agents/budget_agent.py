import asyncio
from graph_state import  TravelState
from mcp_clients import current_weather,forecast
from langchain_core.messages import AIMessage
from agents.helper import _llm_text,_json_from_llm

def budget_agent(state: TravelState):
    user_query = state['user_query']
    trip_constraints = state.get("trip_constraints")
    flight_results = state.get("flight_results")
    hotel_results = state.get("hotel_results")
    weather_results = state.get("weather_results")
    
    print("\n******************* BUDGET AGENT INPUT*******************")
    print("Trip Constraints:")
    print(state.get("trip_constraints"))
    print("\nFlight Results:")
    print(state.get("flight_results"))
    print("\nHotel Results:")
    print(state.get("hotel_results"))
    print("\nWeather Results:")
    print(state.get("weather_results"))
    print("============================================================\n")

    prompt = f"""
    You are an expert travel financial analyst. Analyze whether the proposed trip plan is realistic for the user's budget based on the provided data context.

### INPUT DATA CONTEXT
* User Query: {user_query}
* Trip Constraints: {trip_constraints}
* Flight Results: {flight_results}
* Hotel Results: {hotel_results}
* Weather Impacts: {weather_results}

### INSTRUCTIONS
1. Use exact math to calculate the total cost of fixed expenses (flights + hotels) against the user's maximum budget.
2. Apply a strict 60/40 rule: If fixed costs exceed 60% of the total budget, flag the plan as "High Risk" due to insufficient funds for daily food, transit, and activities.
3. Factor in the weather results (e.g., if raining/extreme heat, note the need for higher indoor activity/taxi budgets).

### OUTPUT FORMAT
Provide a concise, highly scannable assessment using this exact structure:

### 1. Feasibility Verdict
* **Status:** [Feasible / Borderline / Unfeasible]
* **Budget Buffer:** [Remaining amount or deficit in local currency]

### 2. Estimated Cost Breakdown
* **Flights:** [Total cost]
* **Lodging:** [Total cost for entire stay]
* **Daily Allowance:** [Remaining balance divided by number of days] per day for food, local transport, and activities.

### 3. Risk Areas
* [List specific data-backed risks, e.g., missing resort taxes, high local transit costs, or weather-driven indoor expenses]

### 4. Money-Saving Suggestions
* [Provide 2-3 highly actionable, specific alternatives based on the results, e.g., cheaper hotel alternative from the results, shifting dates, or changing transport modes]"""


    result = _llm_text(
        "You are a practical travel financial analyst. Your role is to evaluate trip plans using hard math, not generic advice. You translate raw flight, hotel, and weather data into realistic local daily allowances and flag hidden expenses (taxes, transit, surge pricing) with total transparency.",
        prompt
    )

    print("\n*******************BUDGET AGENT OUTPUT *******************\n")
    print(result)
    print("===========================================================\n")

    return {
        "budget_results": result,
        "messages": [AIMessage(content="Budget agent  process completed.")],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
