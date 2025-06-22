"""
Lambda function to generate AI weekly reports based on Tavily search results and OpenAI LLM.
# This function processes news results, generates questions, formats articles, and uploads the final report to Notion.
# This script is designed to be run as an AWS Lambda function.
# It uses the Tavily API for news search and OpenAI's LLM for text generation.
# It supports two topics: 'general' for AI policy and investment, and 'research' for AI research trends.
# It processes the search results, generates questions, formats the articles, and uploads the final report to Notion.
# It requires the following environment variables:
# - OPENAI_API_KEY: API key for OpenAI.
# - TAVILY_API_KEY: API key for Tavily.
# It also requires the following Python packages:
#   - langchain_openai
#   - tavily
#   - jinja2
# This script is intended to be run in an AWS Lambda environment, but can also be tested locally with a simulated payload.
# It uses the Tavily API to search for news articles based on predefined queries, processes the results using NLP techniques, 
# and generates a formatted report that is uploaded to Notion.
"""
from src.upload_to_notion import upload_to_notion
from src.config import OPENAI_API_KEY, TAVILY_API_KEY
from src.query_definitions import get_ai_general_queries, get_ai_research_queries
from src.nlp_pipeline import process_news_results, generate_qa_questions
from src.formatter import format_articles_for_prompt, build_references_section
from src.generator import load_prompt, generate_article, load_static_text
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from datetime import datetime
import argparse
import os


def run(payload: dict):
    topic = payload.get("topic", "general")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tavily = TavilyClient(api_key=TAVILY_API_KEY)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if topic == "general":
        queries = get_ai_general_queries()
        prompt_path = os.path.join(BASE_DIR, "prompts", "ai_general_prompt.md")
        title = "International AI Policy and Investment Overview"
    elif topic == "research":
        queries = get_ai_research_queries()
        prompt_path = os.path.join(BASE_DIR, "prompts", "ai_research_prompt.md")
        title = "Emerging Trends in AI Research and Algorithms"
    else:
        raise ValueError(f"Unsupported topic '{topic}'.")

    all_articles = []

    for section_title, query in queries.items():
        print(f"[{topic.upper()}] → {section_title}")
        results = tavily.search(query=query, max_results=3)
        entries_preview = [{"title": r["title"], "summary": r["content"][:300]} for r in results["results"]]
        qa_questions = generate_qa_questions(llm, entries_preview, n_questions=4)
        entries = process_news_results(results["results"])
        for entry, qa in zip(entries, qa_questions):
            entry["qa_questions"] = qa

        all_articles.append({"section_title": section_title, "entries": entries})

    material, ref_list, updated_sections = format_articles_for_prompt(all_articles)
    template = load_prompt(prompt_path)
    footer = load_static_text("prompts/footer.md")
    article = generate_article(llm, template, material, title, datetime.now().strftime("%Y-%m-%d"))

    references = build_references_section(ref_list)
    final_markdown = f"{article}\n\n{footer}\n\n{references}"
    upload_to_notion(final_markdown, title_prefix=title)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", choices=["general", "research"], default="general")
    args = parser.parse_args()

    run({"topic": args.topic})
