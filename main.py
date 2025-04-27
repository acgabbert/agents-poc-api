import json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

import os
from dotenv import load_dotenv

from agents import RunResult, RunResultStreaming, Runner
from openai.types.responses import ResponseTextDeltaEvent

from local_agents import agent_registry, get_agent_by_name

from models import ChatRequest, ChatResponse

load_dotenv()

app = FastAPI(title="Local Agent Demo")

default_model = os.getenv("OPENROUTER_MODEL", "openrouter/anthropic/claude-3.7-sonnet")
key = os.getenv("OPENROUTER_API_KEY")

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """
    Chat with an agent.
    """
    try:
        agent = get_agent_by_name(req.agent_name)
        result: RunResult = await Runner.run(agent, input=req.input)
        for resp in result.raw_responses:
            print(resp.output)
        return {
            "output": result.final_output,
            "usage": [response.usage for response in result.raw_responses],
            "agent_used": req.agent_name
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    """
    Stream a chat response.
    """
    try:
        agent = get_agent_by_name(req.agent_name)
        # don't await here because we'll be streaming back to the client
        run: RunResultStreaming = Runner.run_streamed(agent, input=req.input)
        async def event_source():
            try:
                async for evt in run.stream_events():
                    if evt.type == "raw_response_event" and isinstance(evt.data, ResponseTextDeltaEvent):
                        yield evt.data.delta
            except Exception as stream_e:
                print(f"Error during stream: {stream_e}")
        return StreamingResponse(event_source(), media_type="text/event-stream")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents() -> List[str]:
    return list(agent_registry.keys())