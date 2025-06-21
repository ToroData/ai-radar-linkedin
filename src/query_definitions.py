"""
This module defines search queries for AI policy, investment, and research news."""
from datetime import datetime, timedelta

def get_ai_general_queries():
    """
    Returns a dictionary of search queries for AI policy and investment news.
    Each key is a section title and the value is the search query string.
    The queries are designed to fetch recent news articles and reports related to AI policy, regulation, and investment.
    """
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    start_str = start_of_week.strftime("%Y-%m-%d")

    queries_ai_general = {
        "AI News": f'artificial intelligence policy OR AI regulation OR AI investment OR national AI strategy OR AI governance from the last few weeks',
        "USA Policy": 'site:whitehouse.gov OR site:nist.gov "AI policy" OR "executive order" OR "national strategy for AI"',
        "European Union": 'site:ec.europa.eu "AI Act" OR "artificial intelligence regulation"',
        "France Policy": 'site:economie.gouv.fr "intelligence artificielle" OR "stratégie nationale IA"',
        "Spain Policy": 'site:lamoncloa.gob.es OR site.mineco.gob.es "inteligencia artificial"',
        "AI Investment Global": 'site:reuters.com OR site:techcrunch.com OR site:forbes.com "AI investment" OR "AI venture funding"',
        "China Policy": 'site:gov.cn OR site:scmp.com "AI policy" OR "AI development plan"',
        "UN/UNESCO Reports": 'site:unesco.org OR site:un.org "AI ethics" OR "artificial intelligence" report',
    }
    return queries_ai_general

def get_ai_research_queries():
    """
    Returns a dictionary of search queries for AI research and algorithm news.
    Each key is a section title and the value is the search query string.
    The queries are designed to fetch recent academic papers, conference highlights, and breakthroughs in AI research.
    """
    today = datetime.now()
    start_str = today.strftime("%Y-%m-%d")

    queries_ai_research = {
        "New AI Papers": 'site:arxiv.org OR site:nature.com OR site:paperswithcode.com "new algorithm" OR "deep learning" OR "transformer" OR "quantum AI"',
        "ML Research Trends": 'site:deepmind.com OR site.openai.com "research" OR "technical blog" OR "whitepaper"',
        "NeurIPS/ICML Highlights": 'site:neurips.cc OR site:icml.cc "accepted papers" OR "conference highlights"',
        "Breakthroughs in Generative Models": 'site:huggingface.co OR site:openai.com OR site:meta.ai "generative models" OR "LLM architecture"',
        "New Algorithms and Papers": 'site:arxiv.org OR site:openreview.net "artificial intelligence" OR "deep learning" OR "neural network" sorted by date',
        "Academic Conferences": 'site:nips.cc OR site:icml.cc OR site:aaai.org OR site:cvpr.thecvf.com OR site:sigir.org "2024 program" OR "accepted papers"',
        "Benchmarking Trends": 'site:paperswithcode.com OR site:mlcommons.org "state-of-the-art" OR "new benchmark"',
        "Transformer Models": 'site:arxiv.org "transformer architecture" OR "attention mechanism" OR "scaling laws"',
        "Reinforcement Learning": 'site:arxiv.org OR site:deepmind.com "reinforcement learning" OR "RLHF" OR "offline RL"',
        "ML Ethics & Safety Research": 'site:arxiv.org OR site:openai.com OR site:alignmentforum.org "AI alignment" OR "AI safety research"',
        "Neurosymbolic AI": 'site:arxiv.org OR site:mit.edu OR site:stanford.edu "neurosymbolic AI" OR "hybrid learning"',
        "Computational Efficiency": 'site:arxiv.org OR site:meta.com "efficient inference" OR "model compression" OR "quantization"',
        "LLM Architectures": 'site:arxiv.org OR site:huggingface.co "Mixture of Experts" OR "LLM architecture" OR "model parallelism"',
        "General Academic Trends": 'artificial intelligence AND ("research trend" OR "latest paper" OR "new method") from the last month',
    }

    return queries_ai_research