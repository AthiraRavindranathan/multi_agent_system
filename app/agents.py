from langgraph.graph import Graph, END
from typing import Tuple, Dict, Any
from .rag import RAGRetriever
from .models import AgentResponse, AgentType
from .config import settings
import json

class FAQAgent:
    """Handles FAQ resolution using RAG"""
    
    def __init__(self, retriever: RAGRetriever):
        self.retriever = retriever
    
    def process(self, query: str) -> Dict[str, Any]:
        contexts = self.retriever.retrieve(query, top_k=3)
        
        # Simple scoring - check if contexts contain relevant keywords
        answer = "\n".join([f"• {ctx}" for ctx in contexts])
        
        should_escalate = (
            "urgent" in query.lower() or 
            "emergency" in query.lower() or
            "asap" in query.lower()
        )
        
        return {
            "answer": answer,
            "escalate": should_escalate,
            "confidence": 0.8 if contexts else 0.3,
            "sources": contexts,
            "agent_type": AgentType.FAQ
        }

class TechnicalAgent:
    """Handles technical support queries"""
    
    def process(self, query: str) -> Dict[str, Any]:
        is_technical = any(
            keyword in query.lower() 
            for keyword in ["error", "crash", "bug", "issue", "broken", "not working"]
        )
        
        if is_technical:
            return {
                "answer": "A technical support specialist will contact you shortly with step-by-step troubleshooting.",
                "escalate": True,
                "confidence": 0.9,
                "sources": [],
                "agent_type": AgentType.TECHNICAL
            }
        
        return {
            "answer": "",
            "escalate": False,
            "confidence": 0.0,
            "sources": [],
            "agent_type": AgentType.TECHNICAL
        }

class BillingAgent:
    """Handles billing-related queries"""
    
    def process(self, query: str) -> Dict[str, Any]:
        billing_keywords = ["billing", "invoice", "payment", "charge", "refund", "cost", "price"]
        is_billing = any(kw in query.lower() for kw in billing_keywords)
        
        if is_billing:
            return {
                "answer": "Please contact our billing department at billing@support.com with your order number. Response within 24 hours.",
                "escalate": True,
                "confidence": 0.85,
                "sources": [],
                "agent_type": AgentType.BILLING
            }
        
        return {
            "answer": "",
            "escalate": False,
            "confidence": 0.0,
            "sources": [],
            "agent_type": AgentType.BILLING
        }

class EscalationAgent:
    """Handles escalation to human support"""
    
    def process(self, query: str, previous_result: Dict) -> Dict[str, Any]:
        return {
            "answer": f"Your request has been escalated to our support team. A specialist will reach out within 2 hours.\n\nYour query: {query}\n\nPrevious analysis: {previous_result.get('answer', 'N/A')} ",
            "escalate": True,
            "confidence": 1.0,
            "sources": [],
            "agent_type": AgentType.ESCALATION
        }


def build_workflow_graph(retriever: RAGRetriever) -> Graph:
    """
    Build LangGraph workflow using MCP pattern
    """
    faq_agent = FAQAgent(retriever)
    technical_agent = TechnicalAgent()
    billing_agent = BillingAgent()
    escalation_agent = EscalationAgent()
    
    workflow = Graph()
    
    # Define nodes
    def route_to_agents(state: Dict[str, Any]) -> str:
        """Route query to appropriate agent based on content"""
        query = state["query"]
        
        # Check technical
        tech_result = technical_agent.process(query)
        if tech_result["escalate"]:
            return "technical"
        
        # Check billing
        billing_result = billing_agent.process(query)
        if billing_result["escalate"]:
            return "billing"
        
        # Default to FAQ
        return "faq"
    
    def faq_node(state: Dict[str, Any]) -> Dict[str, Any]:
        result = faq_agent.process(state["query"])
        state["agents_involved"].append(AgentType.FAQ)
        state["current_result"] = result
        state["total_steps"] += 1
        
        if result["escalate"]:
            return "escalation"
        return END
    
    def technical_node(state: Dict[str, Any]) -> Dict[str, Any]:
        result = technical_agent.process(state["query"])
        if result["answer"]:  # Only add if processed
            state["agents_involved"].append(AgentType.TECHNICAL)
            state["current_result"] = result
            state["total_steps"] += 1
            return "escalation"
        return "faq"
    
    def billing_node(state: Dict[str, Any]) -> Dict[str, Any]:
        result = billing_agent.process(state["query"])
        if result["answer"]:
            state["agents_involved"].append(AgentType.BILLING)
            state["current_result"] = result
            state["total_steps"] += 1
            return "escalation"
        return "faq"
    
    def escalation_node(state: Dict[str, Any]) -> str:
        result = escalation_agent.process(state["query"], state.get("current_result", {}))
        state["agents_involved"].append(AgentType.ESCALATION)
        state["current_result"] = result
        state["total_steps"] += 1
        state["escalated"] = True
        return END
    
    # Add nodes
    workflow.add_node("router", route_to_agents)
    workflow.add_node("faq", faq_node)
    workflow.add_node("technical", technical_node)
    workflow.add_node("billing", billing_node)
    workflow.add_node("escalation", escalation_node)
    
    # Add edges
    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        lambda x: x["next_step"],
        {
            "faq": "faq",
            "technical": "technical",
            "billing": "billing"
        }
    )
    workflow.add_edge("faq", END)
    workflow.add_edge("technical", END)
    workflow.add_edge("billing", END)
    workflow.add_edge("escalation", END)
    
    return workflow.compile()