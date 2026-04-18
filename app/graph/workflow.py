from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
from app.models.state import AgentState
from app.agents import analyst, researcher, reviewer, supervisor, writer
from app.tools import search, rag
from app.agents.researcher import should_research_continue


graph = StateGraph(AgentState)

tools = [search.web_search, rag.knowledge_base_search]

graph.add_node("supervisor", lambda state: state)
graph.add_node("researcher", researcher.research_agent)
graph.add_node("analyst", analyst.analyst_agent)
graph.add_node("writer", writer.writer_agent)
graph.add_node("reviewer", reviewer.reviewer_agent)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.add_edge(START, "supervisor")

graph.add_conditional_edges(
    "supervisor",
    supervisor.supervisor_agent,
    {
        "researcher": "researcher",
        "analyst": "analyst",
        "writer": "writer",
        "reviewer": "reviewer",
        END: END
    }
)

graph.add_conditional_edges(
    "researcher",
    should_research_continue,
    {
        "tools": "tools",
        "supervisor": "supervisor"
    }
)

graph.add_edge("tools", "researcher")
graph.add_edge("analyst", "supervisor")
graph.add_edge("writer", "supervisor")
graph.add_edge("reviewer", "supervisor")

agent = graph.compile()