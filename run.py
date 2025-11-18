import sys
from agent import deep_research

if __name__ == "__main__":
    # If query is passed by run.sh
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"[INFO] Query = {query}")
    else:
        # fallback for manual usage
        query = input("Enter a research topic: ").strip()

    print("[INFO] Running research agent...\n")
    output = deep_research(query)

    print("\n=== FINAL REPORT ===\n")
    print(output)
