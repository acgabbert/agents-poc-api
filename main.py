from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

import os
from dotenv import load_dotenv

from agents import Agent, RunResult, RunResultStreaming, Runner, Usage
from agents.extensions.models.litellm_model import LitellmModel
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

app = FastAPI(title="Local Agent Demo")

default_model = os.getenv("OPENROUTER_MODEL", "openrouter/anthropic/claude-3.7-sonnet")
key = os.getenv("OPENROUTER_API_KEY")

assistant = Agent(
    name="Assistant",
    instructions="You are a concise, helpful assistant.",
    model=LitellmModel(model=default_model, api_key=key)
)

class ChatRequest(BaseModel):
    input: str

class ChatResponse(BaseModel):
    output: str
    usage: List[Usage]

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    try:
        result: RunResult = await Runner.run(assistant, input=req.input)
        return {"output": result.final_output, "usage": [response.usage for response in result.raw_responses]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    run: RunResultStreaming = Runner.run_streamed(assistant, input=req.input)
    async def event_source():
        async for evt in run.stream_events():
            if evt.type == "raw_response_event" and isinstance(evt.data, ResponseTextDeltaEvent):
                yield evt.data.delta
    return StreamingResponse(event_source(), media_type="text/event-stream")