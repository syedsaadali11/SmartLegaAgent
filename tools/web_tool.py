from langchain.agents import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from config.settings import TAVILY_API_KEY

tavily_tool_instance = TavilySearchResults(api_key=TAVILY_API_KEY)

web_tool = Tool(
    name="TavilySearch",
    func=tavily_tool_instance.run,
    description="Provides the latest information from the web."
)
