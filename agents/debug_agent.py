import os
import nbformat
from nbclient import NotebookClient, CellExecutionError
from tools.tool_wrappers import LLM
from tools.tool_wrappers import save_json

class DebugAgent:
    """
    Runs a notebook top-to-bottom using nbclient.
    If execution fails, capture the error and ask the LLM for a fix suggestion.
    This implementation DOES NOT automatically apply patches; it returns suggestions for manual review.
    """
    def __init__(self, llm: LLM, timeout=120):
        self.llm = llm
        self.timeout = timeout

    def inspect_and_fix_notebook(self, notebook_path: str) -> dict:
        if not os.path.exists(notebook_path):
            return {'status': 'error', 'error': f'Notebook {notebook_path} not found'}

        nb = nbformat.read(notebook_path, as_version=4)
        client = NotebookClient(nb, timeout=self.timeout, kernel_name='python3')
        try:
            client.execute()
            # Save run notebook to outputs
            out_path = 'outputs/fixed_notebook_executed.ipynb'
            nbformat.write(nb, out_path)
            return {'status': 'ran_ok', 'executed_notebook': out_path}
        except CellExecutionError as e:
            tb = str(e)
            # Ask LLM for a patch suggestion (human-review)
            prompt = (
                "You are a code debugging assistant. A Jupyter notebook execution raised the following exception:\n\n"
                f"{tb}\n\n"
                "Provide: 1) The likely root cause in one sentence. 2) A minimal code patch or suggested change to fix the issue. "
                "If the fix requires environment changes (e.g., missing package), mention them explicitly."
            )
            suggestion = self.llm.call(prompt, max_tokens=512)
            # Save suggestion for traceability
            save_json('outputs/debug_suggestion.json', {'error': tb, 'suggestion': suggestion})
            return {'status': 'error', 'error': tb, 'fix_suggestion': suggestion}
        except Exception as e:
            tb = str(e)
            suggestion = self.llm.call(f"Generic error during notebook run: {tb}. Suggest next steps.", max_tokens=300)
            save_json('outputs/debug_suggestion.json', {'error': tb, 'suggestion': suggestion})
            return {'status': 'error', 'error': tb, 'fix_suggestion': suggestion}
