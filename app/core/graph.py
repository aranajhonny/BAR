from langgraph.graph import StateGraph, END
from app.core.state import GraphState
from app.core.nodes import router_node, retrieval_node, generation_node

def build_graph() -> StateGraph:
    graph = StateGraph(GraphState)

    # nodes
    graph.add_node("router", router_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("generation", generation_node)

    # edges
    graph.set_entry_point("router")
    graph.add_edge("retrieval", "generation")
    graph.add_edge("generation", END)

    graph.add_conditional_edges(
        "router",
        lambda state: "retrieval" if state["selected_book"] else "generation",
    )
    compiled = graph.compile()
    return compiled

graph = build_graph()
