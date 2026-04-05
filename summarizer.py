from utils import client, generator, load_config


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

    if client:
        resp = client.responses.create(
            model=model,
            input=prompt
        )
        return resp.output_text
    else:
        # Use local model
        if generator:
            # Phi-2 is a conversational model, so format as instruction
            formatted_prompt = f"Instruct: {prompt}\nOutput:"
            outputs = generator(formatted_prompt, max_new_tokens=1024, do_sample=True, temperature=0.2, pad_token_id=generator.tokenizer.eos_token_id)
            generated_text = outputs[0]['generated_text']
            # Extract the response after the prompt
            response = generated_text[len(formatted_prompt):].strip()
            return response
        else:
            return "No model available for summarization."
