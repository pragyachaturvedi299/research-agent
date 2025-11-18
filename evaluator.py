import os
from openai import OpenAI
import numpy as np
from utils import client
# -------------------------------
# Helper: LLM-based scoring
# -------------------------------
def llm_score(query, answer, metric_name, prompt_instruction):
    prompt = f"""
You are an evaluator. Score the RESPONSE on the metric: {metric_name}.

QUERY:
{query}

RESPONSE:
{answer}

INSTRUCTION:
{prompt_instruction}

Score STRICTLY as a number between 0.0 and 1.0. Return ONLY the number.
"""
    try:
        result = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        text = result.output_text.strip()
        return float(text)
    except:
        return 0.5  # fallback


# -------------------------------
# Completeness
# -------------------------------
def evaluate_completeness(query, answer):
    instruction = "Does the response fully answer all parts of the query?"
    return llm_score(query, answer, "Completeness", instruction)


# -------------------------------
# Relevance
# -------------------------------
def evaluate_relevance(query, answer):
    instruction = "How relevant is the response to the query without going off-topic?"
    return llm_score(query, answer, "Relevance", instruction)


# -------------------------------
# Clarity & Structure
# -------------------------------
def evaluate_clarity(answer):
    instruction = "Is the response well-structured, readable, and easy to understand?"
    return llm_score("N/A", answer, "Clarity", instruction)


# -------------------------------
# Hallucination Risk
# -------------------------------
def evaluate_hallucination(query, answer):
    instruction = ("Does the response contain unverifiable claims, fabricated facts, "
                   "or information not implied by the query or known facts?")
    # Higher = more hallucination → we invert later
    score = llm_score(query, answer, "Hallucination", instruction)
    return 1 - score  # convert “hallucination” into “accuracy of facts”


# -------------------------------
# Accuracy (via embeddings similarity)
# -------------------------------
def evaluate_accuracy(query, answer):
    try:
        emb_q = client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        ).data[0].embedding

        emb_a = client.embeddings.create(
            model="text-embedding-3-small",
            input=answer
        ).data[0].embedding

        query_vec = np.array(emb_q)
        answer_vec = np.array(emb_a)

        cosine = query_vec.dot(answer_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(answer_vec)
        )
        return float((cosine + 1) / 2)  # normalize 0–1
    except:
        return 0.5


# -------------------------------
# Final evaluator wrapper
# -------------------------------
def evaluate_response(query, answer):
    return {
        "Completeness": round(evaluate_completeness(query, answer), 3),
        "Relevance": round(evaluate_relevance(query, answer), 3),
        "Accuracy": round(evaluate_accuracy(query, answer), 3),
        "Clarity": round(evaluate_clarity(answer), 3),
        "Hallucination Risk": round(evaluate_hallucination(query, answer), 3)
    }
