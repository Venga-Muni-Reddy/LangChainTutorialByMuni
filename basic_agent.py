# LLM Call --> First way
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY=os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL=os.environ.get("OPENROUTER_BASE_URL")

model = init_chat_model("openai:gpt-3.5-turbo", api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL,temperature=0)
# response = model.invoke("Hello, how are you?")
# print(response.content)

# LLM Call --> Second way

# model = ChatOpenAI(model="openai/gpt-3.5-turbo", api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)
# response = model.invoke("Hello, I love you❤️")
# print(response.content)

# Messages format

# messages = [
#     SystemMessage(content="You are a Cricket expert."),
#     HumanMessage(content="Who won the last cricket world cup?")
# ]

# response = model.invoke(messages)
# print(response.content)

# Prompts format - Currently we have two ways.
# First way using PromptTemplate, here we cannot set tone.

# user_input = input("Enter a topic for the poem: ")
# dynamic_prompt = PromptTemplate.from_template("Write a poem about {topic}.")

# ready_prompt = dynamic_prompt.invoke({"topic": user_input})

# Second way using ChatPromptTemplate, here we can set tone.

# dynamic_prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a poet who writes in a romantic tone."),
#     HumanMessage(content="Write a poem about {topic}.")
# ])  

# Structured output for llm response
class llm_response(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")

dynamic_prompt = ChatPromptTemplate.from_messages([
    (SystemMessage, "You are a {tone} analyst."),
    (HumanMessage, "Tell me a joke about {topic}.")
])
tone = input("Enter the tone for the joke (e.g. humorous, sarcastic, etc.): ")
topic = input("Enter the topic for the joke: ")

model_structured_output = model.with_structured_output(llm_response)
ready_prompt = dynamic_prompt.invoke({"tone": tone, "topic": topic})
response = model_structured_output.invoke(ready_prompt)

print(response)