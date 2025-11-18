from utils import client, load_config


config = load_config()
model = config["llm"]["model"]

def summarize(query, subqs, search_results):
    prompt = f"""
Write a well-structured research report.

Main Query: {query}

Sub-questions:
{subqs}

Search Results:
{search_results}

Produce a clear, concise expert-level answer.
"""

    resp = client.responses.create(
        model=model,
        input=prompt
    )

    return resp.output_text
