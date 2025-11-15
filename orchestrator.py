import os
import json
from datetime import datetime
from tools.tool_wrappers import LLM, save_json
from agents.knowledge_agent import KnowledgeAgent
from agents.debug_agent import DebugAgent
from agents.report_agent import ReportAgent
from tools.memory import add_memory, search_memory

# Ensure outputs exist
os.makedirs('outputs', exist_ok=True)

# Initialize LLM wrapper (uses environment variables if available)
llm = LLM()
K = KnowledgeAgent(llm)
D = DebugAgent(llm)
R = ReportAgent(llm)

LOG = []

def orchestrate(user_prompt: str, notebook_path: str):
    run_id = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log_entry = {'run_id': run_id, 'prompt': user_prompt, 'notebook': notebook_path, 'steps': []}
    LOG.append({'run_start': log_entry})

    # 1) Research
    r = K.research(user_prompt)
    log_entry['steps'].append({'name': 'knowledge', 'out': r})
    print("[Orchestrator] KnowledgeAgent done.")

    # 2) Debug / run notebook
    dbg = D.inspect_and_fix_notebook(notebook_path)
    log_entry['steps'].append({'name': 'debug', 'out': dbg})
    print("[Orchestrator] DebugAgent done.")

    # 3) Report
    rep = R.make_report(r.get('notes', ''), {'debug': dbg}, out_dir='outputs')
    log_entry['steps'].append({'name': 'report', 'out': rep})
    print("[Orchestrator] ReportAgent done.")

    # Save artifacts
    save_json(f'outputs/orchestrator_log_{run_id}.json', log_entry)
    add_memory('last_project', {'prompt': user_prompt, 'run_id': run_id})
    print(f"[Orchestrator] Run complete. Outputs saved to outputs/ with run_id {run_id}")
    return log_entry

if __name__ == '__main__':
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Improve and fix this notebook"
    nb = sys.argv[2] if len(sys.argv) > 2 else "notebooks/example_input_notebook.ipynb"
    orchestrate(prompt, nb)
