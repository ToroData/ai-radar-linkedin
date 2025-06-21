"""
This module processes news articles to extract insights, sentiment, named entities, and generates questions for further analysis.
"""
from transformers import pipeline
from datetime import datetime
import networkx as nx
from IPython.display import Markdown, display

ner_model = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

qa_questions = [
    "What political decision is mentioned?"
    "Which actors are involved?"
    "What impact does this news have on AI regulation?"
]

def build_entity_graph(entities_raw):
    """
    Builds a graph of named entities from the raw NER output.
    Entities with a score above 0.85 are considered significant.
    Edges are created between consecutive entities in the text.
    Args:
        entities_raw (list): List of named entities with 'word' and 'score'.
    Returns:
        nx.Graph: A graph where nodes are entities and edges connect consecutive entities.
    """
    G = nx.Graph()
    for ent in entities_raw:
        if ent['score'] > 0.85:
            G.add_node(ent['word'])
    for i in range(len(entities_raw)-1):
        e1 = entities_raw[i]
        e2 = entities_raw[i+1]
        if e1['score'] > 0.85 and e2['score'] > 0.85:
            G.add_edge(e1['word'], e2['word'])
    return G

def generate_qa_questions(llm, entries, n_questions=3):
    """
    Generates specific questions based on summarized news entries.
    Args:
        llm: Language model instance for generating questions.
        entries (list): List of news entries with 'title' and 'summary'.
        n_questions (int): Number of questions to generate.
    Returns:
        list: A list of generated questions.
    """
    full_text = "\n".join(
        f"Título: {e['title']}\nResumen: {e['summary']}" for e in entries
    )

    system_prompt = f"""
You are an analyst specializing in artificial intelligence policy and regulation.
Based on the following summarized news stories, generate {n_questions} in-depth and specific questions to be answered with NLP models.
Questions should focus on:

- specific policy decisions
- actors involved
- regulatory or strategic consequences

Do not include generic or trivial questions.
    """.strip()

    prompt = f"{system_prompt}\n\n{full_text}"
    response = llm.invoke(prompt).content

    questions = [q.strip("-• ").strip() for q in response.split("\n") if q.strip()]
    return questions[:n_questions]


def process_news_results(results):
    """
    Processes news results to extract insights, sentiment, and named entities.
    Args:
        results (list): List of news articles with 'title', 'content', and 'url'.
    Returns:
        list: Processed results with insights, sentiment, named entities, and summaries.
    """
    processed = []
    for result in results:
        title = result.get("title", "")
        content = result.get("content", "")
        url = result.get("url", "")
        full_text = f"{title}\n{content}"

        summary = content[:500] + "..." if len(content) > 500 else content

        # Named Entities
        entities_raw = ner_model(full_text)
        entities_clean = list(set([e['word'] for e in entities_raw if e['score'] > 0.85]))

        # Sentiment
        sentiment_result = sentiment_model(full_text[:512])[0]
        sentiment_label = sentiment_result['label']
        sentiment_score = sentiment_result['score']
        sentiment = f"{sentiment_label} (score={sentiment_score:.2f})"

        # QA
        qa_answers = []
        for question in qa_questions:
            answer = qa_model(question=question, context=full_text)
            if answer["score"] > 0.4 and answer["answer"].strip():
                qa_answers.append(f"- {question}: {answer['answer']}")

        # Entity Graph
        graph = build_entity_graph(entities_raw)
        centrality = nx.degree_centrality(graph)
        central_entities = sorted(centrality.items(), key=lambda x: -x[1])[:3]
        central_summary = ", ".join([f"{e[0]} (centralidad={e[1]:.2f})" for e in central_entities])

        processed.append({
            "title": title,
            "summary": summary,
            "entities": ", ".join(entities_clean),
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "insights": "\n".join(qa_answers),
            "central_entities": central_summary,
            "summary_len": len(summary),
            "url": url
        })

    return processed