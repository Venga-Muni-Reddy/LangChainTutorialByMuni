from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY=os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL=os.environ.get("OPENROUTER_BASE_URL")

model = ChatOpenAI(model="openai/gpt-3.5-turbo", temperature=0, max_tokens=1000, api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL, timeout=30)

@tool
def custom_tool(query: str) -> str:
    # Implement your custom tool logic here
    """This is a tool to send emails"""
    return "Email Sent"

agent = create_agent(
    model,
    tools=[DuckDuckGoSearchRun(), custom_tool]
)

example_query = "Please send an email to muni@gmail.com about india"

events = agent.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()
