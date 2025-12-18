# Performance Testing (k6)

This section documents performance testing conducted on the backend service
deployed on AWS ECS Fargate.

All tests were executed using **k6** with the same load profile to ensure fair
comparison across configurations.

---

## Test Configuration

- Tool: k6
- Virtual Users: 20
- Duration: 30 seconds
- Endpoint tested: `/docs`
- Expected response: HTTP 200

Test script:
- `bench/k6-baseline.js`

---

## 1. Baseline Performance (Single Uvicorn Worker)

**Configuration**
- ECS Fargate
- CPU: 1 vCPU
- Memory: 2 GB
- Uvicorn workers: 1

**Results (avg of 3 runs)**

| Metric      | Value   |
|-------------|---------|
| p95 latency | ~460 ms |
| p99 latency | ~650 ms |
| Avg latency | ~435 ms |
| Requests    | ~420    |
| Errors      | 0       |

📁 Files:
- `bench/before/`
- `docs/performance/baseline/`

---

## 2. Infra Optimization (CPU / Memory tuning)

**Change**
- ECS task CPU and memory optimized (no code changes)

**Results**

| Metric      | Value   |
|-------------|---------|
| p95 latency | ~450 ms |
| p99 latency | ~630 ms |
| Avg latency | ~430 ms |

📁 Files:
- `bench/after/`
- `docs/performance/infra-optimized/`

✅ Minor but measurable improvement due to infra tuning.

---

## 3. Application-Level Optimization (Uvicorn Workers = 2)

**Change**
- Increased Uvicorn workers from 1 → 2

**Results**

| Metric      | Value   |
|-------------|---------|
| p95 latency | ~790 ms |
| p99 latency | ~850 ms |
| Avg latency | ~615 ms |

📁 Files:
- `bench/workers2/`

⚠️ **Observation**
Increasing workers did **not** improve latency for this workload.
This is expected for:
- CPU-bound FastAPI apps
- Single-container ECS task without horizontal scaling

---

## Key Takeaways

- Infrastructure tuning provided small gains
- Application-level worker tuning alone is not sufficient
- Real performance gains require:
  - Horizontal scaling
  - Load balancer (ALB)
  - Autoscaling policies

---

## Next Improvements (Out of Scope)

- ECS Service + ALB
- Auto Scaling Groups
- Caching layer (Redis)
- Async I/O optimization

