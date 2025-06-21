"""
Module for formatting articles and generating a report structure.
"""
def format_articles_for_prompt(sections):
    """
    Formate the articles for the prompt and generate a reference list.
    Args:
        sections (list): List of sections, each containing a title and entries.
    Returns:
        tuple: Formatted string for the prompt, reference list, and updated sections.
    """
    formatted = ""
    ref_list = []
    ref_counter = 1

    for section in sections:
        formatted += f"\n### Tema: {section['section_title']}\n"
        for entry in section["entries"]:
            entry["ref_id"] = ref_counter
            ref_list.append(entry["url"])

            formatted += f"""
[{ref_counter}] Title: {entry['title']}
Summary: {entry['summary']}
Entity keys: {entry['entities']}
Central entity: {entry['central_entities']}
Length summary: {entry['summary_len']} caracteres
Sentiment: {entry['sentiment']}
Insights:
{entry['insights']}"""

            if "qa_questions" in entry and entry["qa_questions"]:
                formatted += "\nQ&A Highlights:"
                for qa in entry["qa_questions"]:
                    formatted += f"\n- {qa}"

            formatted += "\n"
            ref_counter += 1

    return formatted.strip(), ref_list, sections



def build_references_section(ref_list):
    """
    Build a Markdown section for references based on the provided list.
    Args:
        ref_list (list): List of URLs to be included as references.
    Returns:
        str: Markdown formatted references section.
    """
    if not ref_list:
        return "## No references available.\n\n"
    
    ref_text = f"## References\n\n"
    for i, url in enumerate(ref_list, start=1):
        ref_text += f"[{i}] {url}\n"
    return ref_text.strip()
