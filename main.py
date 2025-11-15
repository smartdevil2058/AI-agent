import os
from dotenv import load_dotenv
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns

load_dotenv()

genai.configure(api_key="AIzaSyCmW4HrIOhnkVOpUdck5YcsPSzaDtB-Exs")
model = genai.GenerativeModel("gemini-2.5-flash")

class KnowledgeAgent:
    def run(self, query):
        prompt = f"""
        You are the Knowledge Agent.
        Analyze the question deeply.

        Query: {query}

        Respond in JSON:
        {{
            "key_points": [],
            "analysis": ""
        }}
        """
        return model.generate_content(prompt).text

class DebugAgent:
    def run(self, knowledge_output):
        prompt = f"""
        You are the Debug Agent.
        Check issues in reasoning.

        Input:
        {knowledge_output}

        Respond in JSON:
        {{
            "issues_found": [],
            "improvements": []
        }}
        """
        return model.generate_content(prompt).text

class ReportAgent:
    def run(self, knowledge_output, debug_output):
        prompt = f"""
        You are the Report Agent.
        Combine outputs into a clean final answer.

        Knowledge Output:
        {knowledge_output}

        Debug Output:
        {debug_output}

        Respond cleanly.
        """
        return model.generate_content(prompt).text

def evaluate_agent_system(query):
    knowledge = KnowledgeAgent().run(query)
    debug = DebugAgent().run(knowledge)
    final = ReportAgent().run(knowledge, debug)
    return knowledge, debug, final

def dashboard():
    data = [12, 19, 7, 14, 5]
    plt.figure(figsize=(6,4))
    sns.barplot(y=data, x=["A","B","C","D","E"])
    plt.title("Agent Evaluation Dashboard")
    plt.xlabel("Test Cases")
    plt.ylabel("Score")
    plt.show()

if __name__ == "__main__":
    print("=== Multi-Agent System Running ===")
    query = input("Enter your question: ")

    knowledge, debug, final = evaluate_agent_system(query)

    print("\n--- Knowledge Agent ---")
    print(knowledge)

    print("\n--- Debug Agent ---")
    print(debug)

    print("\n--- Final Answer ---")
    print(final)

    print("\nOpening Dashboard…")
    dashboard()
