from langchain_core.messages import SystemMessage

prompt = """
    Evaluate this report on these criteria, scoring each 1-10:
        Accuracy: Does the report correctly represent the research data?
        Completeness: Are all key findings from the analysis included?
        Clarity: Is the writing clear and easy to understand?
        Structure: Does the report follow the required format?
        Coherence: Does the report flow logically from section to section?
    
    If the average score ≥ 7: Respond with APPROVED
        - output format(Respond with ONLY the JSON object, no additional text):
            {
                "status": "APPROVED",
                "feedback": ...,
            }
    If the average score < 7: Respond with NEEDS_REVISION followed by specific, actionable feedback
        - output format(Respond with ONLY the JSON object, no additional text):
            {
                "status": "NEEDS_REVISION",
                "feedback": ...,
            }
"""

REVIEWER_PROMPT = SystemMessage(content=prompt)