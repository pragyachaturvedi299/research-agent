#  Research Agent — Automated Deep Research Pipeline

A modular, configurable research agent that performs **planning → web search → summarization → synthesis → evaluation → PDF report generation**, powered by **OpenAI models** and **LangChain**.


Runs locally with **no GPU required** and supports OpenAI’s latest research / reasoning models.

---

##  What the Agent Does

### 1. **Planning**
Breaks the input query into structured sub-questions.  
→ `planner.py`

### 2. **Web Search**
Uses OpenAI’s web search tool to gather real-time information.  
→ `search.py`

### 3. **Summarization**
Summarizes search results into clean, usable chunks.  
→ `summarizer.py`

### 4. **Synthesis**
Combines summaries into a coherent research report.  
→ `synthesis.py`

### 5. **Evaluation**
Evaluates the final answer on relevance, completeness, depth, and coherence.  
→ `evaluation.py`

### 6. **PDF Generation**
Creates a neat report containing:
- Original query  
- Sub-questions  
- Search results  
- Summaries  
- Final research  
- Evaluation metrics  

→ `pdf_generator.py`

---
# Quick Start

## 1. Clone repo
```bash
git clone <your-repo-url>
cd research-agent
## 2. Create virtual environment
python3 -m venv research-agent
source research-agent/bin/activate
## 3. Install Dependencies
pip install -r requirements.txt
## 4. Add your .env
OPENAI_API_KEY=your_openai_api_key_here
## 5. Make script executable
chmod +x run.sh
## Run the agent
bash run.sh
