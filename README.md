This is a basic proof of concept repo for using the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) with FastAPI. 

To run the project in development mode, run the following:
```
uvicorn main:app --reload
```

Test the `/chat` endpoint:
```
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"input": "Construct a basic curl POST request to test a local FastAPI app", "agent_name": "concise_assistant"}'
```

Test the streaming `/chat/stream/` endpoint with the default agent:
```
curl -X POST http://127.0.0.1:8000/chat/stream \
-H "Content-Type: application/json" \
-d '{"input": "Construct a basic curl POST request to test a local FastAPI app"}'
```

Test the streaming `/agents/` endpoint:
```
curl http://127.0.0.1:8000/agents
```