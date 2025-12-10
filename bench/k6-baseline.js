import http from "k6/http";
import { check, sleep } from "k6";

const TARGET = "http://3.110.151.12:8000/docs";

export let options = {
  vus: 20,
  duration: "30s",
  thresholds: {
    "http_req_duration": ["p(95)<500", "p(99)<1500"]
  }
};

export default function () {
  let res = http.get(TARGET);
  check(res, { "status is 200": (r) => r.status === 200 });
  sleep(1);
}
