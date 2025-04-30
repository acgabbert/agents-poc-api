import litellm
import mlflow
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from agents import Agent, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

from tools import get_weather


load_dotenv()

# Get environment variables
default_model = os.getenv("OPENROUTER_MODEL", "openrouter/anthropic/claude-3.7-sonnet")
key = os.getenv("OPENROUTER_API_KEY")

set_tracing_disabled(True)

mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")
mlflow.litellm.autolog()
litellm.callbacks = ["mlflow"]
mlflow.set_experiment("agents")

claude_3_7 = LitellmModel(model=default_model, api_key=key)
gemini_2_0_flash = LitellmModel(model="openrouter/google/gemini-2.5-flash-preview", api_key=key)
qwen_turbo = LitellmModel(model="openrouter/qwen/qwen-turbo", api_key=key)

concise_assistant = Agent(
    name="Concise Assistant",
    instructions="You are a concise, helpful assistant. Keep answers short and to the point.",
    model=claude_3_7
)

weather_agent = Agent(
    name="Weather Agent",
    instructions="You only respond in haikus.",
    model=qwen_turbo,
    tools=[get_weather]
)

agent_registry = {
    "concise_assistant": concise_assistant,
    "weather_agent": weather_agent
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