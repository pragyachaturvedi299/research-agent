from utils import client, load_config

config = load_config()
model = config["llm"]["model"]
N = config["planning"]["num_subquestions"]

def generate_plan(query):
    prompt = f"""
Break this query into {N} research sub-questions.

Query: {query}

Return only bullet points.
"""

    response = client.responses.create(
        model=model,
        input=prompt
    )

    lines = [l.strip("-• ").strip() for l in response.output_text.split("\n") if l.strip()]
    return lines[:N]
