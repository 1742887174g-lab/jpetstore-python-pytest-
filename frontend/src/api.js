import axios from "axios";

const client = axios.create({
  baseURL: "/api",
  timeout: 300000,
});

export function listTestRuns(params = {}) {
  return client.get("/test-runs", { params }).then((response) => response.data);
}

export function getTestRun(id) {
  return client.get(`/test-runs/${id}`).then((response) => response.data);
}

export function createTestRun(payload) {
  return client.post("/test-runs", payload).then((response) => response.data);
}
