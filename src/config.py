"""
Configuration file for AI Weekly Report project.
This file loads environment variables for API keys and checks their presence.
"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../config.env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

assert OPENAI_API_KEY, "OPENAI_API_KEY is missing"
assert TAVILY_API_KEY, "TAVILY_API_KEY is missing"
assert NOTION_API_KEY, "NOTION_API_KEY is missing"
assert NOTION_DATABASE_ID, "NOTION_DATABASE_ID is missing"
