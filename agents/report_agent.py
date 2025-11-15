import os
from tools.tool_wrappers import LLM
from tools.tool_wrappers import save_json
import datetime

class ReportAgent:
    """
    Creates a lightweight markdown report and optional simple artifact log.
    Converting to PDF can be done with nbconvert or pandoc in environments where available.
    """
    def __init__(self, llm: LLM):
        self.llm = llm

    def make_report(self, summary_text: str, outputs: dict, out_dir: str = 'outputs') -> dict:
        os.makedirs(out_dir, exist_ok=True)
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        md_path = os.path.join(out_dir, f'final_report_{timestamp}.md')
        # Use LLM to generate nicer prose for executive summary
        prompt = (
            "You are a technical writer. Given the following short notes, write a concise executive summary (3-6 sentences):\n\n"
            f"{summary_text}\n\n"
            "Then append a 'Results' section describing outputs and how to reproduce them."
        )
        try:
            exec_summary = self.llm.call(prompt, max_tokens=400)
        except Exception:
            exec_summary = "Executive summary generation failed; using raw notes."

        md_lines = [
            "# Final Report",
            f"**Generated:** {timestamp} UTC",
            "",
            "## Executive Summary",
            "",
            exec_summary,
            "",
            "## Outputs",
            "",
            "```json",
            json_safe(outputs),
            "```",
            "",
            "## Reproduction",
            "",
            "Run `python orchestrator.py \"<your prompt>\" <path_to_notebook>`",
            ""
        ]
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_lines))
        # Save a simple index of artifacts
        save_json(os.path.join(out_dir, f'report_index_{timestamp}.json'), {'report_md': md_path, 'outputs': outputs})
        return {'report_md': md_path}


def json_safe(obj):
    import json
    try:
        return json.dumps(obj, indent=2, default=str)
    except Exception:
        return str(obj)
