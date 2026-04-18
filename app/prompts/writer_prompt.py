from langchain_core.messages import SystemMessage

first_prompt = """
    you are great at writing a analysis report based on the input data 
    
    rules:
        - reponse must follow output structure
    
    output structure(must be maintained):
        - Executive Summary
        - Key findings
        - Detailed Analysis(broken into themed sections)
        - conclusion
        - sources/references

"""

second_prompt = """
    you are revising an analysis report based on reviewer feedback

    rules:
        - response must follow output structure  
        - address each specific point in reviewer's feedback
        - maintain same report structure
        - do not remove accurate content unless the reviewer flagged it
        - preserve all source citations
    
    output structure(must be maintained):
        - Executive Summary
        - Key findings
        - Detailed Analysis(broken into themed sections)
        - conclusion
        - sources/references  
    
"""

WRITER_INITIAL_PROMPT = SystemMessage(content=first_prompt)
WRITER_FEEDBACK_PROMPT = SystemMessage(content=second_prompt)