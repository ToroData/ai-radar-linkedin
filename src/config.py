"""
Configuration file for AI Weekly Report project.
This file loads environment variables for API keys and checks their presence.
"""
import os
from dotenv import load_dotenv

load_dotenv('config.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

assert OPENAI_API_KEY, "Falta OPENAI_API_KEY"
assert TAVILY_API_KEY, "Falta TAVILY_API_KEY"
