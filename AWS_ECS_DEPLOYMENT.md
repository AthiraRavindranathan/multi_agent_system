# AWS ECS Deployment Guide

## Introduction
This guide provides detailed instructions for deploying a containerized application on AWS ECS (Elastic Container Service) using Fargate.

## Prerequisites
- AWS Account
- AWS CLI installed and configured
- Docker installed

## Step 1: Push Docker Image to ECR
1. **Authenticate Docker to ECR**  
   Run the below command to log in to ECR:
   ```bash
   aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
   ```

2. **Build Your Docker Image**  
   Navigate to your project directory and build your Docker image:
   ```bash
   docker build -t <your-image-name> .
   ```

3. **Tag Your Image**  
   Tag the image with the ECR repository URI:
   ```bash
   docker tag <your-image-name>:latest <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repository-name>:latest
   ```

4. **Push the Image to ECR**  
   Once tagged, push your image to ECR:
   ```bash
   docker push <your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repository-name>:latest
   ```

## Step 2: Create an ECS Cluster
1. **Create the Cluster**  
   You can create a new ECS cluster using the following command:
   ```bash
   aws ecs create-cluster --cluster-name <your-cluster-name>
   ```

2. **Verify the Cluster**  
   List clusters to verify your newly created cluster:
   ```bash
   aws ecs list-clusters
   ```

## Step 3: Create a Task Definition
1. **Register Task Definition**  
   Create a task definition JSON file (e.g., `task-definition.json`):  
   ```json
   {
     "family": "<your-task-family>",
     "networkMode": "awsvpc",
     "containerDefinitions": [
       {
         "name": "<your-container-name>",
         "image": "<your-account-id>.dkr.ecr.<your-region>.amazonaws.com/<your-repository-name>:latest",
         "essential": true,
         "memory": 512,
         "cpu": 256,
         "portMappings": [
           {
             "containerPort": 80,
             "hostPort": 80
           }
         ]
       }
     ]
   }
   ```
   Register the task definition:
   ```bash
   aws ecs register-task-definition --cli-input-json file://task-definition.json
   ```

## Step 4: Create an ECS Service
1. **Create Service**  
   Use the following command to create a service:
   ```bash
   aws ecs create-service --cluster <your-cluster-name> --service-name <your-service-name> --task-definition <your-task-family> --desired-count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[<your-subnet-ids>],securityGroups=[<your-security-group-ids>],assignPublicIp='ENABLED'}"
   ```

## Step 5: Verify the Deployment
1. **Check Service Status**  
   Verify the service is running:
   ```bash
   aws ecs describe-services --cluster <your-cluster-name> --services <your-service-name>
   ```

2. **Access the Application**  
   Get the public IP of the tasks and access your application through the browser.

## Conclusion
This guide provided a step-by-step process of deploying an application using AWS ECS Fargate. Make sure to replace placeholder values with your actual configuration.
