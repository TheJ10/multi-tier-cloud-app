# Baseline Performance Test (k6)

This section documents the first performance test run on the deployed backend.

## 🔹 Test Command
k6 run --out json=bench/results-baseline.json bench/k6-baseline.js

Copy code

## 🔹 Summary (Baseline)
- **p95 latency:** ~426 ms  
- **p99 latency:** ~610 ms  
- **Average latency:** ~424 ms  
- **Total requests:** 440  
- **Checks passed:** 0%  
  *(The `/` endpoint does not return HTTP 200, so checks fail. This is expected and not a backend failure.)*

## 🔹 Files
- Raw results JSON: `bench/results-baseline.json`
- Test script: `bench/k6-baseline.js`
- Screenshot placeholder: `docs/performance/baseline-summary.png`

## 🔹 Notes
- Checks failed because the tested route does not return a 200 status.  
- I will adjust the target endpoint in the next steps for cleaner results.

