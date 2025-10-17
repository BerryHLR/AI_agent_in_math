# AI Agent in Math

A lightweight Python project demonstrating an AI agent designed to help solve, explain, and reason about mathematics problems. The repo includes the agent logic, a small web UI demo, and example scripts for experimentation.

## Table of contents
- [Key features](#key-features)  
- [Who this is for](#who-this-is-for)  
- [Quick start](#quick-start)  
  - [Prerequisites](#prerequisites)  
  - [Clone & setup](#clone--setup)  
  - [Install dependencies](#install-dependencies)  
  - [Run examples](#run-examples)  
- [Project structure](#project-structure)  
- [How the agent works](#how-the-agent-works)    
- [Acknowledgements & references](#acknowledgements--references)  
- [Contact](#contact)

## Key features

- Multi‑agent architecture: a modular set of specialized agents (analyzer, thinker, questioner, derivation, computation, etc.) that collaborate to parse, reason, verify, and present solutions.  
- Role‑driven workflows: each agent has a clear role and job (e.g., computation executes Python, derivation produces rigorous math, writer crafts explanatory articles), enabling responsibility separation and easier extensibility.  
- Enhanced mathematical reasoning: combines LLM prompting with symbolic/math-aware components to produce step‑by‑step, logically consistent solutions.  
- Python execution sandbox: an isolated computation agent that runs Python code to verify calculations, generate examples, and compute symbolic results.  
- Neuro‑symbolic inspiration: design informed by recent advances (e.g., AlphaGeometry), enabling hybrid neural + symbolic strategies for harder mathematical tasks.  
- Symbolic validation and derivation: integrates or can integrate tools like SymPy to derive, check, and symbolically validate intermediate and final results.  
- Human‑readable article output: a writer/designer/editor pipeline that generates well‑structured, pedagogical articles and HTML layouts suitable for publishing or classroom use.  
- Model‑agnostic adapters: abstraction layers for plugging different model backends (local Transformers, Hugging Face, OpenAI, etc.) without invasive code changes.  
- Input validation & judgement: agents that verify input validity and decide when rigorous symbolic transformation or deeper proof strategies are required.  
- Iterative critique & refinement: reflection and questioner agents provide critique, ask clarifying questions, and drive iterative improvement of solutions and prompts.  
- Small demo web UI: lightweight HTML/CSS/JS frontend to demo agent outputs and share interactive examples.  
- Research & evaluation ready: intended for reproducible experimentation — easy to extend with datasets, notebooks, and evaluation scripts to benchmark reasoning performance and compare against competitors.


## Who this is for
- Developers: extend the code, swap models, add interfaces.  
- Researchers: experiment with reasoning workflows, prompting strategies, and evaluation.  
- Educators: adapt demos and notebooks for teaching math problem solving.

## Quick start

### Prerequisites
- Python 3.8+  
- Git  
- Optional: virtualenv or conda for isolated environments

### Clone & setup
```bash
git clone https://github.com/BerryHLR/AI_agent_in_math.git
cd AI_agent_in_math
```

### Create & activate virtual environment
macOS / Linux:
```bash
python -m venv .venv
source .venv/bin/activate
```
Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run examples / demos
- backend demo:
```bash
python backend/test.py
```

- frontend demo:
```bash
python app.py
```


## Project structure
```
AI_agent_in_math
├─ app.py
├─ backend
│  ├─ agents
│  │  ├─ analyzer.py
│  │  ├─ computation.py
│  │  ├─ computationv1.py
│  │  ├─ computationv2.py
│  │  ├─ derivation.py
│  │  ├─ derivationv2.py
│  │  ├─ designer.py
│  │  ├─ editor.py
│  │  ├─ explainer.py
│  │  ├─ input_checker.py
│  │  ├─ judger.py
│  │  ├─ publisher.py
│  │  ├─ questioner.py
│  │  ├─ reflection.py
│  │  ├─ thinker.py
│  │  ├─ writer.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  │     ├─ analyzer.cpython-310.pyc
│  │     ├─ analyzer.cpython-311.pyc
│  │     ├─ computation.cpython-310.pyc
│  │     ├─ computation.cpython-311.pyc
│  │     ├─ derivation.cpython-310.pyc
│  │     ├─ derivation.cpython-311.pyc
│  │     ├─ designer.cpython-310.pyc
│  │     ├─ designer.cpython-311.pyc
│  │     ├─ editor.cpython-310.pyc
│  │     ├─ editor.cpython-311.pyc
│  │     ├─ explainer.cpython-310.pyc
│  │     ├─ explainer.cpython-311.pyc
│  │     ├─ input_checker.cpython-310.pyc
│  │     ├─ input_checker.cpython-311.pyc
│  │     ├─ judger.cpython-310.pyc
│  │     ├─ judger.cpython-311.pyc
│  │     ├─ publisher.cpython-310.pyc
│  │     ├─ publisher.cpython-311.pyc
│  │     ├─ questioner.cpython-310.pyc
│  │     ├─ questioner.cpython-311.pyc
│  │     ├─ reflection.cpython-310.pyc
│  │     ├─ reflection.cpython-311.pyc
│  │     ├─ thinker.cpython-310.pyc
│  │     ├─ thinker.cpython-311.pyc
│  │     ├─ writer.cpython-310.pyc
│  │     ├─ writer.cpython-311.pyc
│  │     ├─ __init__.cpython-310.pyc
│  │     └─ __init__.cpython-311.pyc
│  ├─ langgraph_agent.py
│  ├─ outputs
│  │  ├─ run_1711273436
│  │  ├─ run_1711273574
│  │  └─ run_1711273689
│  ├─ server.py
│  ├─ tempCodeRunnerFile.py
│  ├─ templates
│  │  ├─ article
│  │  │  ├─ index.html
│  │  │  └─ styles.css
│  │  └─ newspaper
│  │     └─ layouts
│  │        └─ layout_3.html
│  ├─ test.py
│  ├─ __init__.py
│  └─ __pycache__
│     ├─ langgraph_agent.cpython-310.pyc
│     └─ __init__.cpython-310.pyc
└─ frontend
   ├─ index.html
   └─ static
      ├─ favicon.ico
      ├─ icon.jpg
      ├─ layout_icons
      │  ├─ layout_1.png
      │  ├─ layout_2.png
      │  └─ layout_3.png
      ├─ scripts.js
      └─ styles.css
```


## How the agent works
In the context of our project, we have developed a multi-agent system consisting of various agents that collectively work towards achieving our objectives--solve math problems. These agents play distinct roles and collaborate to enhance the capabilities of ChatGPT, enabling it to fulfill specific tasks with greater effectiveness and relevance. 

The following table outlines the different roles and corresponding jobs of the agents:
| Agents | Role | Job |
|---|---|---|
| analyzer | Math expert | Analyze the problem step by step |
| computation | Python expert | Use to execute python code to solve math problems |
| derivation | Math expert | Do mathematical derivations based on the given thought using rigor mathematical expressions |
| designer | N/A | Get the format of the article |
| editor | N/A | Get the html layout of the article |
| explainer | Math teacher expert in explaining in simple yet accurate terms | Explain how to solve a math problem |
| input_checker | System/user | Check whether the input is a valid math problem |
| judger | System/user | Judge whether a problem needs rigor mathematical transformation |
| pulisher | N/A | Save newspaper html |
| questioner | Math expert | Question the thoughts and analysis process on a certain problem |
| reflection | Math expert | Criticize the usefulness of thought |
| thinker | Math expert | Think about what to do next for solving the question you are given based on current progress and feedback. |
| writer | Excellent explanatory blog writer | Write a well-written and engaging article about how to solve a math problem. |
<img width="752" height="1064" alt="image" src="https://github.com/user-attachments/assets/8b6472aa-36de-450d-9334-f9afc5c08cf7" />

## Acknowledgements & references
- Built as an exploration of combining symbolic math tools and LLMs for math reasoning.  
- Thank open-source projects and model providers used in experiments (SymPy, Hugging Face, OpenAI, etc.).

## Contact
Repository owner: @BerryHLR
