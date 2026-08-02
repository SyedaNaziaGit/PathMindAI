import psycopg
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from config import DATABASE_URL
from langchain_core.messages import SystemMessage , AIMessage, HumanMessage
from graph_state import TravelState
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.budget_agent import budget_agent
from agents.human_approval_agent import human_approval_agent
from agents.itinerary_agent import itinerary_agent
from agents.weather_agent import weather_agent
from agents.final_agent import final_agent
from agents.supervisor_agent import supervisor_agent

#the order in which agent should be called
AGENT_ORDER = [
    "flight_agent",
    "hotel_agent",
    "weather_agent",
    "budget_agent",
    "itinerary_agent",
]

#route map for the  order of execution
ROUTE_MAP = {
    "flight_agent": "flight_agent",
    "hotel_agent": "hotel_agent",
    "weather_agent": "weather_agent",
    "budget_agent": "budget_agent",
    "itinerary_agent": "itinerary_agent",
}

#------------------------HELPER--------------------
#returns the list of all the selected agents by llm 
def _selected_agents(state: TravelState) -> list[str]:
    selected = state.get("selected_agents")
    return [agent  for agent in AGENT_ORDER if agent in selected]

#after supervisor agent the next agent is first agent in the selected list else it will generate the itinerary agent
def route_after_supervisor(state: TravelState) -> str:
    selected = _selected_agents(state)
    return selected[0] if selected else 'itinerary_agent'

#choosing the next agent in the choice of agents either following order as in  wrapper route func 
def route_after_agent(present_agent:str):
    def route(state: TravelState):
        selected = _selected_agents(state)
        present_index = AGENT_ORDER.index(present_agent)
        
        for next_agent in AGENT_ORDER[present_index + 1]:
            if next_agent in selected:
                return next_agent
        return 'itinerary_agent'
    return route

#-------------------------GRAPH-------------------------
#Building graph function
def build_graph():
    #defining graph
    graph = StateGraph(TravelState)
    
    #adding nodes
    graph.add_node('supervisor',supervisor_agent)
    graph.add_node('flight_agent',flight_agent)
    graph.add_node('hotel_agent',hotel_agent)
    graph.add_node('weather_agent',weather_agent)
    graph.add_node('budget_agent',budget_agent)
    graph.add_node('itinerary_agent',itinerary_agent)
    graph.add_node('human_approval',human_approval_agent)
    graph.add_node('final_response',final_agent)
    
    #adding edges
    graph.add_edge(START,'supervisor')
    graph.add_conditional_edges('supervisor',route_after_supervisor,ROUTE_MAP)
    graph.add_conditional_edges('flight_agent',route_after_agent('flight_agent'),ROUTE_MAP)
    graph.add_conditional_edges('hotel_agent',route_after_agent('hotel_agent'),ROUTE_MAP)
    graph.add_conditional_edges('weather_agent',route_after_agent('weather_agent'),ROUTE_MAP)
    graph.add_conditional_edges('budget_agent',route_after_agent('budget_agent'),ROUTE_MAP)
    graph.add_edge('itinerary_agent','human_approval')
    graph.add_edge('human_approval','final_response')
    graph.add_edge('final_response',END)
    
    #adding a checkpoint- persistant - using postgres db for the checkpoint to save the state
    if DATABASE_URL:
        conn = psycopg.connect(DATABASE_URL)
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()
        return graph.compile(checkpointer=checkpointer)
        
    #compiling graph
    return graph.compile()

#building app
app =  build_graph()
'''
TESTING
user_query = "Japan 7 day trip with 1L budget"
result = app.invoke({
    "messages": [HumanMessage(content=user_query)],
    "user_query":user_query
    })
    
print(result)
'''