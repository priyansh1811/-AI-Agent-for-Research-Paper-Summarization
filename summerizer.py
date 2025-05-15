from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import ArxivAPIWrapper
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-latest",
    verbose=True,
    temperature=0.0,
    google_api_key=google_api_key
)

# Initialize Arxiv wrapper
arxiv_tool = ArxivAPIWrapper()

# Define tools list
tools = [
    Tool(
        name="Research Paper Summarizer",
        func=arxiv_tool.run,
        description="Useful for when you need to summarize the paper."
    )
]

# Load prompt from LangChain hub
prompt = hub.pull("hwchase17/react")

# Define the agent builder function
def getAgent():
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor