# Lab 11 — Docker + ECS Fargate

## Overview

In this lab, I deployed a containerized web application on AWS using Docker, Amazon ECR, Amazon ECS with Fargate, and an Application Load Balancer.

The lab demonstrated how a Docker image could be built, stored in a container registry, deployed as an ECS task, exposed through a load balancer, and automatically replaced when a running task was stopped.

## Architecture

```text
                         INTERNET
                            │
                            ▼
                    ┌───────────────┐
                    │      ALB      │
                    │  lab-11-alb   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ ECS Service   │
                    │ lab-11-service│
                    └───────┬───────┘
                            │
                    ┌───────┴───────┐
                    ▼               ▼
              ┌──────────┐    ┌──────────┐
              │ Fargate  │    │ Fargate  │
              │  Task 1  │    │  Task 2  │
              └────┬─────┘    └────┬─────┘
                   │               │
                   └───────┬───────┘
                           ▼
                    ┌─────────────┐
                    │     ECR     │
                    │ lab-11-web  │
                    └─────────────┘
```

## AWS Services Used

* Amazon ECR
* Amazon ECS
* AWS Fargate
* Application Load Balancer
* Amazon VPC
* Elastic Load Balancing
* IAM

## Technologies

* Docker
* Nginx
* HTML
* Linux containers
* AWS CLI
* AWS CloudShell

## Project Structure

```text
11-ecs-fargate/
├── Dockerfile
├── index.html
├── README.md
└── screenshots/
    ├── 01-ecr-image.png
    ├── 02-ecs-cluster.png
    ├── 03-task-definition.png
    ├── 04-ecs-service-tasks.png
    ├── 05-healthy-targets.png
    ├── 06-alb-response.png
    └── 07-self-healing.png
```

## 1. Created the Web Application

I created a simple HTML application to provide a lightweight workload for the container.

The application displayed:

```text
Lab 11 - ECS Fargate

This application is running inside a Docker container on Amazon ECS Fargate.
```

## 2. Created the Docker Image

The application was packaged using the following Dockerfile:

```dockerfile
FROM nginx:alpine

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80
```

The image used the lightweight `nginx:alpine` base image and served the HTML application through Nginx on port 80.

## 3. Tested the Container Locally

Because Docker was not installed on my Windows environment, I used AWS CloudShell, which already had Docker available.

I built the image and tested the container locally inside CloudShell.

The container successfully returned the expected HTML response before it was deployed to ECS.

## 4. Created an ECR Repository

I created an Amazon ECR repository named:

```text
lab-11-web
```

The Docker image was tagged for Amazon ECR and pushed to the repository.

The image was successfully stored in ECR and was later used by the ECS task definition.

## 5. Created the ECS Cluster

I created an ECS cluster named:

```text
lab-11-cluster
```

The cluster used AWS Fargate as the compute platform.

During the initial setup, ECS reported that its service-linked role was missing. I verified the AWSServiceRoleForECS service-linked role and retried the cluster creation successfully.

## 6. Created the Task Definition

I created the task definition family:

```text
lab-11-task
```

The task definition was configured with:

* Launch type: Fargate
* Operating system: Linux
* Architecture: x86_64
* CPU: 1024
* Memory: 3072 MiB
* Container name: `lab-11-web`
* Container port: 80
* Protocol: TCP
* Application protocol: HTTP

The task definition referenced the Docker image stored in the ECR repository.

## 7. Configured Security Groups

Two security groups were used to control traffic.

### Application Load Balancer Security Group

```text
lab-11-alb-sg
```

Inbound HTTP traffic was allowed on port 80 from:

```text
0.0.0.0/0
```

### ECS Web Security Group

The existing web security group was:

```text
lab-11-web-sgv
```

Inbound HTTP traffic on port 80 was restricted to the Application Load Balancer security group.

This created a security-group chain where public HTTP traffic reached the ALB first, while the ECS tasks only accepted HTTP traffic from the ALB.

## 8. Created the Target Group

I created the target group:

```text
lab-11-web-targets
```

Configuration included:

* Target type: IP
* Protocol: HTTP
* Port: 80
* Health check path: `/`
* Successful response: HTTP 200

The target group was used by the ALB to route requests to the Fargate tasks.

## 9. Created the Application Load Balancer

I created an internet-facing Application Load Balancer named:

```text
lab-11-alb
```

The ALB used:

* IPv4
* HTTP listener on port 80
* Multiple Availability Zones
* `lab-11-alb-sg`
* `lab-11-web-targets`

The listener forwarded incoming requests to the ECS target group.

## 10. Created the ECS Service

I created the ECS service:

```text
lab-11-service
```

The service was configured to maintain:

```text
Desired tasks: 2
```

Both tasks were launched using AWS Fargate.

The service was connected to the Application Load Balancer and target group.

## 11. Verified Healthy Tasks

After deployment, the ECS service reached:

```text
Desired: 2
Running: 2
Pending: 0
```

Both Fargate tasks registered successfully with the target group and reported a healthy status.

This confirmed that:

```text
ALB → Target Group → Fargate Tasks
```

was working correctly.

## 12. Tested the Application

I tested the application through the ALB endpoint using `curl`.

The response returned:

```text
HTTP/1.1 200 OK
```

The expected application content was also returned:

```text
Lab 11 - ECS Fargate

This application is running inside a Docker container on Amazon ECS Fargate.
```

This confirmed that traffic successfully travelled through the load balancer to the containerized application.

## 13. Tested ECS Self-Healing

To test the ECS service's ability to maintain its desired task count, I deliberately stopped one of the running Fargate tasks.

The service temporarily dropped below the desired count and ECS automatically started a replacement task.

The service eventually returned to:

```text
Desired: 2
Running: 2
Pending: 0
```

The replacement task registered with the target group and became healthy.

This demonstrated ECS service self-healing.

## 14. Troubleshooting

### Security Group CIDR Error

During deployment, I encountered:

```text
CIDR block lab-11-alb-sg is malformed
```

The problem occurred because the security group name had been entered where an IP address/CIDR value was expected.

I corrected the configuration by using the actual security group ID for the source of the inbound rule.

This reinforced the distinction between:

* Security group name
* Security group ID
* CIDR block

### ECS Service-Linked Role

The initial ECS cluster creation also failed because the required ECS service-linked role was not available.

I verified the `AWSServiceRoleForECS` role and retried the operation successfully.

## 15. What I Learned

This lab helped me understand the complete container deployment workflow on AWS:

```text
Application
    ↓
Docker
    ↓
Amazon ECR
    ↓
ECS Task Definition
    ↓
ECS Service
    ↓
AWS Fargate
    ↓
Target Group
    ↓
Application Load Balancer
    ↓
Internet
```

Key lessons included:

* How Docker packages an application into a container image
* How Amazon ECR stores container images
* How ECS task definitions describe container workloads
* How Fargate runs containers without managing EC2 servers
* How ECS services maintain a desired number of running tasks
* How ALBs distribute traffic to containerized applications
* How target groups perform health checks
* How security groups can restrict traffic between AWS components
* How ECS can replace a stopped task automatically
* How to troubleshoot AWS networking and deployment configuration errors

## 16. Cleanup

After completing the lab, I removed the temporary AWS resources to avoid unnecessary ongoing costs.

The cleanup included:

* ECS service
* ECS cluster
* Application Load Balancer
* Target group
* ECR repository and image
* Lab-specific security groups
* Lab-specific IAM resources where applicable

Shared/default VPC networking resources were preserved.

The local Docker container and temporary Docker authentication data were also cleaned up after testing.

## Result

The lab successfully demonstrated a complete container deployment workflow using:

**Docker → ECR → ECS/Fargate → ALB**

The application was successfully deployed, accessed through the load balancer, monitored through target health checks, and tested for ECS self-healing.

This was the next step in my AWS Cloud Learning Journey from running applications directly on EC2 toward modern containerized deployments.
