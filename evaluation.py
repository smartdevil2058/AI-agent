import json
import os
from tools.tool_wrappers import save_json

def evaluate_run(log_entry: dict, out_path='outputs/evaluation.json'):
    """
    Lightweight evaluation harness that:
    - checks debug status
    - assigns simple scores
    - writes evaluation summary
    """
    debug_result = None
    report_result = None
    for step in log_entry.get('steps', []):
        if step.get('name') == 'debug':
            debug_result = step.get('out')
        if step.get('name') == 'report':
            report_result = step.get('out')

    score_auto = 0
    notes = []
    if debug_result:
        if debug_result.get('status') == 'ran_ok':
            score_auto += 70
            notes.append("Notebook executed successfully.")
        else:
            score_auto += 10
            notes.append("Notebook had errors; LLM suggested fixes.")
    else:
        notes.append("No debug output found.")

    if report_result and report_result.get('report_md'):
        score_auto += 30
        notes.append("Report generated.")
    else:
        notes.append("No report generated.")

    score_auto = min(100, score_auto)
    evaluation = {
        'auto_score': score_auto,
        'notes': notes,
    }
    save_json(out_path, evaluation)
    return evaluation

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python evaluation.py <path_to_orchestrator_log_json>")
        sys.exit(1)
    log_path = sys.argv[1]
    log = json.load(open(log_path, 'r', encoding='utf-8'))
    print(evaluate_run(log))
