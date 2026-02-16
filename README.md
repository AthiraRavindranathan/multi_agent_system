# Multi Agent System

## Features
- Multi-agent functionality for efficient task execution.
- User-friendly interface for interaction.
- Scalable architecture to accommodate varying loads.
- Supports RAG (Retrieve and Generate) for enhanced data retrieval and generation.

## Quick Start

### Option 1: Using Start Script (Recommended)
**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AthiraRavindranathan/multi_agent_system.git
   cd multi_agent_system
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. Access the API:
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Root: http://localhost:8000/

### Testing the API
Run the test script:
```bash
python test_api.py
```

## API Endpoints
- **GET /**: Root endpoint with API information
- **GET /health**: Health check endpoint
- **GET /agents**: List all available agents
- **POST /support**: Submit a support query
  - Request body:
    ```json
    {
      "question": "Your question here",
      "customer_id": "optional_customer_id",
      "priority": "normal"
    }
    ```
  - Response:
    ```json
    {
      "query": "Your question",
      "final_response": "Agent response",
      "agents_involved": ["faq", "technical"],
      "escalated": false,
      "total_steps": 2
    }
    ```

## Architecture
The system is based on a microservices architecture that allows for independent scaling and deployment of individual services, enhancing both flexibility and resilience.

## RAG Implementation
The RAG implementation allows for the retrieval of relevant data from various sources and the generation of responses using advanced language models.

## Docker Deployment
To deploy the system using Docker:
1. Build the Docker image:
   ```bash
   docker build -t multi_agent_system .
   ```
2. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 multi_agent_system
   ```

## ECS Fargate Instructions
1. Define your task definition in the AWS Management Console.
2. Choose Fargate as the launch type.
3. Configure networking and security settings.
4. Deploy the service to run the application in AWS ECS Fargate.