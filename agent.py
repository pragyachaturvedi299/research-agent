from utils import load_config
from planner import generate_plan
from search import run_search
from summarizer import summarize
from pdf_generator import save_pdf
from evaluator import evaluate_response
config = load_config()

def deep_research(query):

    subqs = generate_plan(query)
    results = [run_search(sq) for sq in subqs]
    final_answer = summarize(query, subqs, results)

    evaluation = evaluate_response(query, final_answer)
    print(evaluation)
    save_pdf(
        query=query,
        sub_questions=subqs,
        search_results=results,
        final_answer=final_answer,
        eval_metrics=evaluation,
        file_name="research_report.pdf",
        config=config
    )

    return final_answer