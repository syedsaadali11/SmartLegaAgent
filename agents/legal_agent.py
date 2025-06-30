from langchain.agents import initialize_agent
from langchain_openai import ChatOpenAI
from config.settings import LLM_MODEL, OPENROUTER_API_KEY
from tools.vector_tool import vector_tool
from tools.web_tool import web_tool

llm = ChatOpenAI(
    model=LLM_MODEL,
    openai_api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.3,
)

agent = initialize_agent(
    tools=[vector_tool, web_tool],
    llm=llm,
    agent_type="zero-shot-react-description",
    verbose=False,
)
