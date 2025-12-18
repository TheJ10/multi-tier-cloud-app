# Multi-Tier Cloud Application (FastAPI + AWS ECS + Terraform + CI/CD)
A production-oriented cloud backend demonstrating real-world engineering practices
using FastAPI, Docker, AWS ECS (Fargate), Terraform, and GitHub Actions. The project
emphasizes reproducible infrastructure, safe CI/CD pipelines, and measurable
performance testing rather than over-automation or unnecessary complexity.


## Overview
This project demonstrates a **production-ready multi-tier cloud application** built with:

- **FastAPI** backend
- **Docker** containerization
- **AWS ECS (Fargate)** for compute
- **Amazon ECR** for container registry
- **Terraform** for Infrastructure as Code (IaC)
- **GitHub Actions** for CI/CD
- **k6** for performance benchmarking

The goal of this project is not just functionality, but **clarity, reproducibility, and engineering discipline** — so that **any engineer can understand, run, and extend the system**.

---

## Architecture

### High-Level Architecture
```text
┌──────────────────────────────┐
│          Developer           │
│   (Browser / curl / k6)      │
└──────────────┬───────────────┘
               │
               │ HTTP :8000
               ▼
┌──────────────────────────────┐
│      AWS Security Group      │
│  Inbound: TCP 8000 (My IP)   │
│  Outbound: All               │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Amazon ECS Cluster       │
│     (Fargate Launch Type)    │
│                              │
│  ┌────────────────────────┐  │
│  │   ECS Task (Backend)   │  │
│  │  -------------------   │  │
│  │  FastAPI Application   │  │
│  │  Uvicorn (workers=2)   │  │
│  │  Port: 8000            │  │
│  └────────────────────────┘  │
│                              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       AWS Networking         │
│  VPC + Private Subnets       │
│  ENI + Public IP (Fargate)   │
└──────────────────────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Amazon ECR Repository    │
│  (Docker Images Storage)     │
└──────────────────────────────┘

```

### CI/CD Flow
```text
	GitHub Push / PR
               │
               ▼
      ┌───────────────┐
      │ CI Pipeline   │
      │ - Tests       │
      │ - Docker      │
      └───────┬───────┘
     	 (on dev/main)
	      ▼
    ┌────────────────────┐
    │ Build & Push Image │
    │	 → Amazon ECR    │
    └────────────────────┘
```

---

## Prerequisites
Make sure you have installed:

- **Python 3.11**
- **Docker**
- **Git**

---

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd multi-tier-cloud-app
git checkout dev
```

### 2.  Run Backend Locally (Without Docker)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Verify:
```bash
curl http://localhost:8000/docs
```

### 3.  Run Backend with Docker
```bash
docker build -t mta-backend:local backend
docker run -p 8000:8000 mta-backend:local
```

Verify:
```bash
curl http://localhost:8000/docs
```
### How to Run on AWS 
>⚠️ AWS credentials are required
- Docker image is built & pushed to Amazon ECR
- ECS Task Definition references the image
- ECS Fargate task is launched inside a VPC
- Security Group allows inbound traffic on port 8000

Terraform is used to create ECS cluster and networking, but application deployment is intentionally kept manual for safety.

---

## CI/CD Pipeline 

### Workflow 1: ci.yml (Continuous Integration)

Triggered on:
- Push to **dev** or **main**
- Pull Requests

What it does:
1. Checks out code
2. Sets up Python 3.11
3. Installs dependencies
4. Runs pytest tests
5. Builds Docker image (no push)

Purpose:
Ensure code quality and Docker correctness before deployment.

### Workflow 2: build-and-push.yml (Artifact Delivery)

Triggered on:
- Push to **dev** or **main**

What it does:
1. Authenticates to AWS
2. Logs into Amazon ECR
3. Builds Docker image
4. Pushes image to ECR(latest + commit SHA)

Purpose:
Safely publish production-ready container images.

>ECS deployment and Terraform apply are intentionally not automated to avoid unsafe infrastructure changes.

---

## Design Decisions & Trade-Offs
### Why ECS Fargate?
Pros
- No server management
- Scales well
- Simple for backend APIs

Trade-off
- Less control than EC2
- Slightly higher cost

### Why Uvicorn Multiple Workers?
Reason
- Improves CPU utilization
- Better concurrency handling

Trade-off
- Not always beneficial for I/O-heavy workloads
- Requires benchmarking (done using k6)

### Why Terraform Only for Baseline Infra?
Reason
- Prevents accidental infra destruction
- Safer for demo / interview projects
- Clear separation of concerns

Trade-off
- Not full auto-deploy
- Requires manual ECS task run

### Why Not Auto-Deploy on Every Commit?
Reason
- Infrastructure changes should be deliberate
- Recruiters value safety over reckless automation

---

## Performance Testing (k6)
We used k6 to benchmark:
- Baseline ECS setup
- Infrastructure tuning
- Multiple Uvicorn workers

Results are stored in:
```text
	bench/
 	├── before/
	├── after/
 	└── workers2/
```
Each test includes:
- Raw JSON output
- Summary files for comparison

---

## Functionality Verification
Backend Health
```bash
curl http://<PUBLIC_IP>:8000/docs
```
Expected:
- HTTP 200 OK
- Swagger UI HTML

### ECS Task Status
```bash
aws ecs list-tasks --cluster <cluster-name>
aws ecs describe-tasks --tasks <task-arn>
```
Status should be:
```text
RUNNING
```

### Docker Image Check
```bash
aws ecr list-images --repository-name mta-backend
```

---

## Troubleshooting
### Cannot Access API (Timeout / No Response)
Possible Causes
- Your public IP changed
- Security Group only allows old IP

Fix
```bash
curl https://checkip.amazonaws.com
Update Security Group ingress rule with your new IP.
``` 

###ECS Task Stops Immediately
Check
```bash
aws ecs describe-tasks --tasks <task-arn>
```
Common causes:
- Invalid Docker CMD
- Missing port mapping
- Image pull failure

### Terraform Errors (Unauthorized / No VPC)
Cause
- Wrong AWS profile
- Incorrect VPC reference

Fix
- Verify profile = "infra"
- Confirm VPC ID exists

---

## Future Improvements
- If extended further, I would:
- Add Application Load Balancer
- Use OIDC instead of AWS secrets
- Add Terraform remote backend (S3 + DynamoDB)
- Enable autoscaling policies
- Add structured logging & metrics
- Add health check endpoints
 
---

## Final Notes
This project intentionally focuses on:
- Clarity over complexity
- Safety over blind automation
- Real-world engineering practices

It is designed to be:
- Readable
- Runnable
- Explainable in interviews

---

## Author:
Jaspal Gundla  
