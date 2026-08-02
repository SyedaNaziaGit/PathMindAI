import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import TAVILY_API_KEY,AVIATION_STACK_API_KEY

#-------------------------------MCP CLIENT-------------------------------

client = MultiServerMCPClient(
    {
        "tavily": {
            "transport":"streamable_http",
            "url":f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
        },
        "aviationstack":{
                "transport":"stdio",
                "command": r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\aviationstack-mcp\.venv\Scripts\python.exe",
                "args": [
                        "-m",
                        "aviationstack_mcp",
                        "mcp",
                        "run"
                    ],
                    "env": {
                        "AVIATION_STACK_API_KEY": AVIATION_STACK_API_KEY
                    }
        },
        "weather":{
                    "transport":"stdio",
                    "command": r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\myenv\Scripts\python.exe",
                    "args": [ r"C:\Users\Lenovo\OneDrive\Desktop\MCP\itenari_langgraph_mcp\custom_weather_mcp_server3.py"
                            ],
        }
    }
)

#--------------------Helper Functions------------------------

#Caching tools to avoid repeated loading
_tools_cache = None

async def get_tools():
    global _tools_cache
    if _tools_cache is  None:
        try:
            pass
        except Exception as e:
            print(type(e))
            print(repr(e))
            if hasattr(e, "exceptions"):
                print("\nSUB EXCEPTIONS:")
                for i, sub in enumerate(e.exceptions):
                    print(f"\n--- Exception {i+1} ---")
                    print(type(sub))
                    print(repr(sub))

            raise
    return _tools_cache

async def call_tool(tool_name:str,args : dict = None):
    #tools = await get_tools()
    tools = asyncio.run(get_tools())
    tool = next((tool for tool in tools if tool.name == tool_name), None)
    if tool is None:
        raise ValueError(f"Tool '{tool_name}' not found")
    return await tool.ainvoke(args or {})

#--------------------------TOOLS---------------------------------

#------------------------1. Flight Tools -------------------
async def list_airports(search: str = "", limit: int = 10):
    return await call_tool("list_airports", {"search": search, "limit": limit, "offset": 0})


async def list_airlines(search: str = "", limit: int = 10):
    return await call_tool("list_airlines", {"search": search, "limit": limit, "offset": 0})

#-----------------------2. Tavily Search Tool ---------------------

async def tavily_search(query: str):
    return await call_tool("tavily_search", {"query": query})

#-----------------------3.Weather Tools------------------------

async def current_weather(city: str):
    return await call_tool("get_current_weather", {"city": city})


async def forecast(city: str):
    return await call_tool("get_forecast", {"city": city})