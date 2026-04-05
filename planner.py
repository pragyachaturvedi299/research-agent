from openai import OpenAI
import os
from langchain_openai import ChatOpenAI
from utils import client, generator, load_config



config = load_config()
model = config["llm"]["model"]
N = config["planning"]["num_subquestions"]

def generate_plan(query):
    prompt = f"""
Break this query into {N} research sub-questions.

Query: {query}

Return only bullet points.
"""

    if client:
        response = client.responses.create(
            model=model,
            input=prompt
        )
        output_text = response.output_text
    else:
        # Use local model
        if generator:
            formatted_prompt = f"Instruct: {prompt}\nOutput:"
            outputs = generator(formatted_prompt, max_new_tokens=512, do_sample=True, temperature=0.2, pad_token_id=generator.tokenizer.eos_token_id)
            generated_text = outputs[0]['generated_text']
            output_text = generated_text[len(formatted_prompt):].strip()
        else:
            output_text = f"- Sub-question 1 for {query}\n- Sub-question 2 for {query}"

    lines = [l.strip("-• ").strip() for l in output_text.split("\n") if l.strip()]
    return lines[:N]
