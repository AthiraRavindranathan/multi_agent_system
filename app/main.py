from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import settings
from .rag import init_retriever
from .agents import build_workflow_graph
from .models import SupportQuery, WorkflowResponse, AgentType
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG and workflow
logger.info("Initializing RAG retriever...")
retriever = init_retriever()

logger.info("Building workflow graph...")
workflow = build_workflow_graph(retriever)

@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} started")

@app.get("/")
async def root():
    return {
        "message": "Multi-Agent Support System API",
        "version": settings.APP_VERSION,
        "endpoints": {
            "support": "/support",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}

@app.post("/support", response_model=WorkflowResponse)
async def handle_support_query(query: SupportQuery):
    """
    Main endpoint for handling customer support queries
    
    - Uses RAG to retrieve relevant documentation
    - Routes through multiple agents (FAQ, Technical, Billing)
    - Escalates when necessary
    """
    try:
        logger.info(f"Processing query: {query.question}")
        
        # Initialize workflow state
        state = {
            "query": query.question,
            "customer_id": query.customer_id,
            "priority": query.priority,
            "agents_involved": [],
            "current_result": {},
            "total_steps": 0,
            "escalated": False,
            "next_step": "router"
        }
        
        # Execute workflow - using simple routing logic
        # Check technical agent
        from .agents import TechnicalAgent, BillingAgent
        technical_agent = TechnicalAgent()
        billing_agent = BillingAgent()
        
        tech_result = technical_agent.process(query.question)
        if tech_result["answer"]:
            state["agents_involved"].append(AgentType.TECHNICAL)
            state["current_result"] = tech_result
            state["total_steps"] += 1
            state["escalated"] = True
        else:
            # Check billing agent
            billing_result = billing_agent.process(query.question)
            if billing_result["answer"]:
                state["agents_involved"].append(AgentType.BILLING)
                state["current_result"] = billing_result
                state["total_steps"] += 1
                state["escalated"] = True
            else:
                # Use FAQ agent
                from .agents import FAQAgent
                faq_agent = FAQAgent(retriever)
                faq_result = faq_agent.process(query.question)
                state["agents_involved"].append(AgentType.FAQ)
                state["current_result"] = faq_result
                state["total_steps"] += 1
        
        # Extract final response
        final_response = state.get("current_result", {}).get("answer", "Unable to process your request")
        
        return WorkflowResponse(
            query=query.question,
            final_response=final_response,
            agents_involved=state.get("agents_involved", []),
            escalated=state.get("escalated", False),
            total_steps=state.get("total_steps", 0)
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents")
async def list_agents():
    """List available agents in the system"""
    return {
        "agents": [
            {"name": AgentType.FAQ, "description": "FAQ and knowledge base retrieval"},
            {"name": AgentType.TECHNICAL, "description": "Technical issue resolution"},
            {"name": AgentType.BILLING, "description": "Billing and payment support"},
            {"name": AgentType.ESCALATION, "description": "Human escalation handler"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )