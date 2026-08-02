import asyncio
from graph_state import  TravelState
from mcp_clients import current_weather,forecast
from langchain_core.messages import AIMessage

def weather_agent(state: TravelState):
    constraints = state["trip_constraints"]
    city = constraints["destination"]
    print("\n******************* WEATHER AGENT INPUT *******************\n")
    print("City:", city)
    print("=============================================================\n")
    weather_data = asyncio.run(current_weather(city))
    forecast_data = asyncio.run(forecast(city))
    print("\n******************* CURRENT WEATHER *********************\n")
    print(weather_data)
    print("============================================================\n")
    print("\n******************* WEATHER FORECAST *******************")
    print(forecast_data)
    print("===========================================================\n")
    result = f"[WEATHER UPDATE] Current: {weather_data} // Forecast: {forecast_data}"
    print("\n*******************WEATHER AGENT OUTPUT *******************\n")
    print(result)
    print("============================================================\n")

    return {
        "weather_results": result,
        "messages": [AIMessage(content="Weather agent process completed.")],
    }

