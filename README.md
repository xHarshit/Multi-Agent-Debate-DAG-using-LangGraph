# Multi-Agent Debate DAG (LangGraph-style) — CLI Demo (OpenAI backend)

**What it is**
A CLI program implementing the ATG Technical Assignment: two agents (Scientist vs Philosopher) debate a user-provided topic for 8 rounds total (4 turns each) with memory, turn control, coherence validation, and a Judge node that summarizes and declares a winner.

**Features**
- CLI interface
- OpenAI API backend for agent/judge LLM calls
- MemoryNode storing per-agent relevant summary + full transcript file
- State validation: turn enforcement, duplicate prevention, logical coherence
- All node messages & state transitions logged
- DAG diagram generation using Graphviz

**Files**
- `main.py` — entrypoint; CLI loop
- `nodes.py` — node class definitions (UserInputNode, AgentNode, MemoryNode, JudgeNode)
- `langgraph_dag.py` — DAG builder + simple runtime orchestration
- `utils.py` — logging, env, validation helpers
- `generate_diagram.py` — create DAG PNG via graphviz
- `requirements.txt` — Python deps
- `.env.example` — env variable example

**Requirements**
- Python 3.10+
- OpenAI API key

**Setup**
1. Create virtualenv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` and optionally `OPENAI_MODEL` and `LOG_FILE`.

3. Generate DAG diagram (optional):
   ```bash
   python generate_diagram.py
   # will write dag_diagram.png
   ```

4. Run the debate:
   ```bash
   python main.py
   ```

**Output**
- Interactive CLI prompts
- `logs/debate_log.txt` contains full logs: user input, each agent message, memory updates, turn validation events, judge summary & verdict.

**Notes**
- This repo uses the OpenAI Chat completions; you can switch `OPENAI_MODEL` to your preferred model in `.env`.
- The project intentionally keeps agent prompts persona-specific (Scientist vs Philosopher). Change in `main.py` if you want different personas.

**Walkthrough / Demo**
Record a 2–4 minute demo showing:
- Repo structure
- How to set `OPENAI_API_KEY`
- Running `python main.py` and the debate flow
- Inspecting `logs/debate_log.txt`
- Showing the generated DAG image (`dag_diagram.png`)
