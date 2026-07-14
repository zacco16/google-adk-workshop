import os

from google.adk.agents import Agent


def get_root_agent() -> Agent:
    """Construct and return the root travel planner Agent."""
    return Agent(
        name="travel_planner",
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        description="An AI travel planner that recommends attractions and local events.",
        instruction=(
            "You are an expert travel planner. Given a destination and time of year, "
            "recommend must-see attractions, seasonal highlights, and local events. "
            "Be specific and practical, and organize your answer clearly with short "
            "sections or bullet points."
        ),
    )
