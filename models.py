from typing import List
from agents import Usage
from pydantic import BaseModel

from local_agents import DEFAULT_AGENT_NAME


class ChatRequest(BaseModel):
    input: str
    agent_name: str = DEFAULT_AGENT_NAME

class ChatResponse(BaseModel):
    output: str
    usage: List[Usage]
    agent_used: str