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

Test an agent with tools:
```
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"input": "What is the weather in New York City?", "agent_name": "weather_agent"}'
```

Test the `/agents/` endpoint:
```
curl http://127.0.0.1:8000/agents
```

## Tracing with [MLflow](https://docs.litellm.ai/docs/observability/mlflow)
If you have a MLflow server running locally, the agents LiteLLM integration enables tracing with just a few lines of code.