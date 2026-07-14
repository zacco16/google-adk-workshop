from google.adk.sessions import InMemorySessionService
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.genai import types  # For creating message Content/Parts
import asyncio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / "my_travel_planner" / ".env")  # Load environment variables from the .env file
from my_travel_planner.agent import get_root_agent

APP_NAME = "travel-planner_app"
USER_ID = "user_1"
SESSION_ID = "session_001"


async def setup_session_and_runner(root_agent: Agent | None = None, session_id: str = SESSION_ID):
    """Set up the InMemorySessionService and Runner instances for one conversation."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    return session, runner


async def call_agent_async(query: str, root_agent: Agent | None = None, session_id: str = SESSION_ID) -> str:
    """Workshop TODO: send the user's query to the runner and capture the final response."""
    raise NotImplementedError(
        "Create a google.genai.types.Content payload, feed it through Runner.run_async, and parse the final "
        "response text to return to the caller."
    )


async def run_agent_pipeline(query: str) -> str:
    """Workshop TODO: orchestrate the call by wiring up the root agent and async runner helper."""
    raise NotImplementedError(
        "Call get_root_agent(), pass it into call_agent_async(), and return the text you receive back."
    )


if __name__ == "__main__":
    user_query = ("I'm planning a trip to Paris in the spring. What are some must-see attractions and local events "
                  "during that time?")
    asyncio.run(run_agent_pipeline(query=user_query))
