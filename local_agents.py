import os

from dotenv import load_dotenv
from fastapi import HTTPException
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel


load_dotenv()

# Get environment variables
default_model = os.getenv("OPENROUTER_MODEL", "openrouter/anthropic/claude-3.7-sonnet")
key = os.getenv("OPENROUTER_API_KEY")

concise_assistant = Agent(
    name="Concise Assistant",
    instructions="You are a concise, helpful assistant. Keep answers short and to the point.",
    model=LitellmModel(model=default_model, api_key=key)
)

agent_registry = {
    "concise_assistant": concise_assistant
}

DEFAULT_AGENT_NAME = "concise_assistant"

def get_agent_by_name(agent_name: str) -> Agent:
    """Dependency to retrieve an agent by name."""
    agent = agent_registry.get(agent_name)
    if not agent:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{agent_name}' not found. Available agents: {list(agent_registry.keys())}"
        )
    return agent