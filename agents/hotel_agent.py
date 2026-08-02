import asyncio
from graph_state import  TravelState
from mcp_clients import tavily_search
from langchain_core.messages import AIMessage

def hotel_agent(state: TravelState):
    user_query = f"Provide a detailed travel guide on the best neighborhoods to stay in {state['user_query']}, including pros and cons for each area, followed by top-rated hotel recommendations for different budgets."
    print("\n******************* HOTEL AGENT INPUT*******************\n ")
    print(user_query)
    print("===========================================================\n")

    result = asyncio.run(tavily_search(user_query))

    print("\n******************* HOTEL SEARCH RESULT*******************\n")
    print(result)
    print("=============================================================\n")
    return {
        "hotel_results": str(result),
        "messages": [AIMessage(content="Hotel agent process completed.")],
    }