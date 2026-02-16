# Multi Agent System

## Features
- Multi-agent functionality for efficient task execution.
- User-friendly interface for interaction.
- Scalable architecture to accommodate varying loads.
- Supports RAG (Retrieve and Generate) for enhanced data retrieval and generation.

## Quick Start
1. Clone the repository:
   ```bash
   git clone https://github.com/AthiraRavindranathan/multi_agent_system.git
   cd multi_agent_system
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## API Endpoints
- **GET /api/tasks**: Retrieve all tasks.
- **POST /api/tasks**: Create a new task.
- **GET /api/tasks/{id}**: Retrieve a specific task by ID.
- **PUT /api/tasks/{id}**: Update a task by ID.
- **DELETE /api/tasks/{id}**: Delete a task by ID.

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