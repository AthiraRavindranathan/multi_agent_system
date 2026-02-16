# Quick Reference Guide

## Project Structure
```
multi_agent_system/
├── app/
│   ├── __init__.py          # Package initializer
│   ├── main.py              # FastAPI application & endpoints
│   ├── config.py            # Configuration settings
│   ├── models.py            # Pydantic models
│   ├── agents.py            # Agent implementations & workflow
│   └── rag.py               # RAG retriever implementation
├── data/
│   └── docs.json            # Knowledge base documents
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore patterns
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
├── start.bat                # Windows start script
├── start.sh                 # Linux/Mac start script
├── test_api.py              # API test suite
└── README.md                # Main documentation
```

## Key Components

### Agents
1. **FAQ Agent**: Handles general questions using RAG retrieval
2. **Technical Agent**: Routes technical issues to specialists
3. **Billing Agent**: Handles billing and payment queries
4. **Escalation Agent**: Escalates complex issues to human support

### Workflow
```
User Query → Router → [FAQ/Technical/Billing] → [Escalation if needed] → Response
```

## Common Commands

### Development
```bash
# Start server with auto-reload
uvicorn app.main:app --reload

# Run tests
python test_api.py

# Check Python syntax
python -m py_compile app/*.py
```

### Docker
```bash
# Build image
docker build -t multi-agent-system .

# Run container
docker run -d -p 8000:8000 multi-agent-system

# View logs
docker logs <container_id>
```

### API Usage Examples

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Submit Support Query
```bash
curl -X POST http://localhost:8000/support \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I reset my password?",
    "customer_id": "user123",
    "priority": "normal"
  }'
```

#### List Agents
```bash
curl http://localhost:8000/agents
```

## Troubleshooting

### Issue: Module not found
**Solution**: Ensure you're in the project root and virtual environment is activated

### Issue: Port 8000 already in use
**Solution**: Change port in command: `uvicorn app.main:app --port 8001`

### Issue: FAISS installation fails
**Solution**: Install build tools or use `faiss-cpu` instead of `faiss`

### Issue: Docker healthcheck fails
**Solution**: Ensure curl is installed in container (already fixed in Dockerfile)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | False |
| OPENAI_API_KEY | OpenAI API key (optional) | "" |
| MODEL_NAME | LLM model name | gpt-4-turbo-preview |
| AWS_REGION | AWS region for deployment | us-east-1 |

## Agent Response Format

```json
{
  "query": "User's question",
  "final_response": "Agent's answer",
  "agents_involved": ["faq", "technical"],
  "escalated": false,
  "total_steps": 2
}
```

## Adding New Documents

Edit `data/docs.json`:
```json
[
  {
    "id": 9,
    "category": "new_category",
    "content": "Your new FAQ content here"
  }
]
```

The RAG system will automatically load and index new documents on startup.
