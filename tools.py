from agents import function_tool

# basic example from the SDK repository
@function_tool
def get_weather(city: str):
    """Get the current weather for a city."""
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny today."