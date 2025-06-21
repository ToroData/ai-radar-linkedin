"""
This module provides functionality to generate articles using a language model and a Jinja2 template."""
from jinja2 import Template

def load_prompt(path="prompts/ai_general_prompt.md"):
    """
    Loads a Jinja2 template from a file.
    Args:
        path (str): Path to the prompt template file.
    Returns:
        Template: Jinja2 template object.
    """
    with open(path, "r") as f:
        return Template(f.read())
    
def load_static_text(path):
    """
    Loads static text from a file.
    Args:
        path (str): Path to the static text file.
    Returns:
        str: Content of the static text file.
    """
    with open(path, "r") as f:
        return f.read()


def generate_article(llm, prompt_template, material, category_title, date):
    """
    Generates an article based on the provided material and category title.
    Args:
        llm: Language model instance for generating text.
        prompt_template (Template): Jinja2 template for the prompt.
        material (str): The content to be included in the article.
        category_title (str): Title of the article category.
        date (str): Date of the report.
    Returns:
        str: Generated article content.
    """
    rendered_prompt = prompt_template.render(
        category_title=category_title,
        date=date,
        material=material
    )
    return llm.invoke(rendered_prompt).content.strip()
