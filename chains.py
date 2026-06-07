from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel

load_dotenv()
OPENROUTER_API_KEY=os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL=os.environ.get("OPENROUTER_BASE_URL")

# Task - 1 : Create a mode;
model = ChatOpenAI(model="openai/gpt-3.5-turbo", temperature=0,api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL)

# Task - 2 : Create a prompt template with dynamic variables for tone and topic, and then invoke the model with the ready prompt to get a joke in the specified tone about the specified topic. The response should be structured with a setup and punchline.
# prompt_template = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful analyst."),  
#     ("human", "what is the capital of {topic}?")
# ])
# topic = input("Enter text : ")
# ready_prompt = prompt_template.invoke({"topic": topic})

# Task - 3 : Define a structured output format for the model's response, where the joke is divided into a setup and a punchline. Use this structured format to parse the model's response and print the setup and punchline separately.
output_parser = StrOutputParser()

# Chaining the prompt template, model, and output parser together not calling manually each component, instead we will call the chain and it will execute all the components in sequence.
# There are two ways to create a chain, first way is using the pipe operator and second way is using Runnable Sequence
# Usingin pipe operator
# chain = prompt_template | model | output_parser

# Using Runnable Sequence
# chain = RunnableSequence(prompt_template, model, output_parser)

# Using custom runnable
# def custom_runnable(input):
#     return {"text": input}
# runnable_chain = RunnableLambda(custom_runnable)

# prompt = PromptTemplate.from_template("Please generate a linkedin post about {text}")

# chain = prompt_template | model | output_parser | runnable_chain | prompt | model | output_parser

# response = chain.invoke({"topic": topic})

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a movie summarizer."),
    ("human", "Please summarize the movie in brief {movie_name}")
])


def custom_runnable(input):
    return {"text": input}
runnable_chain = RunnableLambda(custom_runnable)

# Linkedin chain : 
linkedin_prompt = PromptTemplate.from_template("Please generate a linkedin post about {text}")
linkedin_chain = linkedin_prompt | model | output_parser

# Insta chain : 
insta_prompt = PromptTemplate.from_template("Please generate an instagram post about {text}")
insta_chain = insta_prompt | model | output_parser

# Final chain :
final_chain = (
    prompt_template | model | output_parser | runnable_chain | RunnableParallel(branches = {"linkedin": linkedin_chain, "instagram": insta_chain})
)

def beautify_runnable(input):
    linkedin_post = input["branches"]["linkedin"]
    insta_post = input["branches"]["instagram"]
    return {"linkedin": linkedin_post, "instagram": insta_post}
beautify_chain = RunnableLambda(beautify_runnable)

final_beautify_chain = final_chain | beautify_chain
response = final_beautify_chain.invoke("KGF")
print(response)