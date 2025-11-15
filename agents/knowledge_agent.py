from tools.tool_wrappers import LLM

class KnowledgeAgent:
    """
    Simple research agent: uses LLM to summarize and propose steps.
    """
    def __init__(self, llm: LLM):
        self.llm = llm

    def research(self, task_description: str) -> dict:
        prompt = (
            "You are a technical research assistant. Given the following task, provide:\n"
            "1) A concise summary of what should be done (3-6 bullet points).\n"
            "2) A prioritized checklist of steps to fix or improve a Jupyter notebook for reliability and clarity.\n\n"
            f"Task: {task_description}\n\n"
            "Respond in clear text; label sections 'SUMMARY' and 'CHECKLIST'."
        )
        resp = self.llm.call(prompt, max_tokens=600)
        return {'notes': resp}
