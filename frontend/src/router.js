import { createRouter, createWebHistory } from "vue-router";

import DashboardView from "./views/DashboardView.vue";
import RunTestsView from "./views/RunTestsView.vue";
import HistoryView from "./views/HistoryView.vue";
import RunDetailView from "./views/RunDetailView.vue";

const routes = [
  { path: "/", redirect: "/dashboard" },
  { path: "/dashboard", component: DashboardView },
  { path: "/run", component: RunTestsView },
  { path: "/history", component: HistoryView },
  { path: "/history/:id", component: RunDetailView, props: true },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
