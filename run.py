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

# Created once and reused across requests so conversation history is retained
# for the life of the process (InMemory: resets on restart).
_session_service = InMemorySessionService()


async def setup_session_and_runner(root_agent: Agent | None = None, session_id: str = SESSION_ID):
    """Set up the Runner against the shared session service, reusing the session."""
    session = await _session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )
    if session is None:
        session = await _session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=_session_service,
    )
    return session, runner


async def call_agent_async(query: str, root_agent: Agent | None = None, session_id: str = SESSION_ID) -> str:
    """Send the user's query to the runner and capture the final response text."""
    _, runner = await setup_session_and_runner(root_agent=root_agent, session_id=session_id)

    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response = ""
    async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text

    return final_response


async def run_agent_pipeline(query: str) -> str:
    """Orchestrate the call: build the root agent and run the query through it."""
    root_agent = get_root_agent()
    return await call_agent_async(query, root_agent=root_agent)


if __name__ == "__main__":
    user_query = ("I'm planning a trip to Paris in the spring. What are some must-see attractions and local events "
                  "during that time?")
    response = asyncio.run(run_agent_pipeline(query=user_query))
    print(response)
