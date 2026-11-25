import asyncio
import os
import traceroot
from traceroot import Integration
from agents import Agent, Runner, function_tool

BREAK = os.getenv("BREAK") == "1"

@function_tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    if BREAK:
        # Silent bug: a stale cache entry ignores the requested city.
        return "It is -2C and snowing in Oslo."
    return f"It is 24C and sunny in {city}."

@function_tool
def search_flights(origin: str, dest: str) -> str:
    """Find the cheapest flight between two cities."""
    return f"Cheapest flight {origin} to {dest}: $320, 1 stop."

weather_agent = Agent(
    name="Weather agent",
    instructions="Answer weather questions using get_weather.",
    tools=[get_weather],
)
flight_agent = Agent(
    name="Flight agent",
    instructions="Find flights using search_flights.",
    tools=[search_flights],
)
planner = Agent(
    name="Trip planner",
    instructions="Use both specialist tools, then give one short answer.",
    tools=[
        weather_agent.as_tool("weather_specialist", "Weather for a city"),
        flight_agent.as_tool("flight_specialist", "Flights between two cities"),
    ],
)

async def main():
    result = await Runner.run(
        planner, "I'm flying SFO to Lisbon. Will it be warm, and what's the flight cost?"
    )
    print(result.final_output)

if __name__ == "__main__":
    traceroot.initialize(integrations=[Integration.OPENAI_AGENTS])
    tag = "broken" if BREAK else "healthy"
    with traceroot.using_attributes(tags=[tag], metadata={"demo": "multi-agent"}):
        asyncio.run(main())
    traceroot.flush()