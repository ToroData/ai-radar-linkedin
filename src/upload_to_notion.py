"""
This module provides functionality to upload Markdown content to a Notion database as a new page.
It converts Markdown text into Notion blocks and creates a new page with the specified title."""
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from notion_client import Client

load_dotenv("config.env") 

notion = Client(auth=os.getenv("NOTION_API_KEY"))
NOTION_DATABASE_ID =os.getenv("NOTION_DATABASE_ID")

def markdown_to_blocks(markdown_text, chunk_limit=1800):
    """
    Convert Markdown text to Notion blocks.
    This function processes Markdown text and converts it into a list of Notion blocks.
    It handles headings, paragraphs, bulleted lists, and numbered references.
    Args:
        markdown_text (str): The Markdown text to convert.
        chunk_limit (int): The maximum number of characters per block.
    Returns:
        list: A list of Notion blocks.
    """
    lines = markdown_text.split("\n")
    blocks = []

    def add_paragraph(text):
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    def add_heading(text, level):
        return {
            "object": "block",
            f"heading_{level}": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            },
            "type": f"heading_{level}"
        }

    def add_bulleted_item(text):
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [{"type": "text", "text": {"content": text}}]
            }
        }

    paragraph_buffer = []

    def flush_buffer():
        if paragraph_buffer:
            blocks.append(add_paragraph(" ".join(paragraph_buffer)))
            paragraph_buffer.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            flush_buffer()
            blocks.append(add_heading(stripped[3:], level=2))
        elif stripped.startswith("# "):
            flush_buffer()
            blocks.append(add_heading(stripped[2:], level=1))
        elif stripped.startswith("- "):
            flush_buffer()
            blocks.append(add_bulleted_item(stripped[2:]))
        elif re.match(r"\[\d+\]", stripped):
            flush_buffer()
            blocks.append(add_paragraph(stripped))
        elif stripped == "":
            flush_buffer()
        else:
            paragraph_buffer.append(stripped)

    flush_buffer()
    return blocks


def upload_to_notion(markdown_text, title_prefix="AI Governance Report"):
    """
    Uploads a Markdown text to Notion as a new page in the specified database.
    Args:
        markdown_text (str): The Markdown text to upload.
        title_prefix (str): The prefix for the page title.
    Returns:
        dict: The response from the Notion API containing the page URL.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = f"{title_prefix} - {date_str}"
    blocks = markdown_to_blocks(markdown_text)

    response = notion.pages.create(
        parent={"database_id": NOTION_DATABASE_ID},
        properties={
            "Doc name": {
                "title": [{"text": {"content": title}}]
            }
        },
        children=blocks
    )
    print(f"Notion URL: {response['url']}")
    return response