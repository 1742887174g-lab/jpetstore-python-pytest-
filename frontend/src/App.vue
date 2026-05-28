<template>
  <el-container class="app-shell">
    <el-aside width="220px" class="sidebar">
      <div class="brand">
        <div class="brand-mark">JP</div>
        <div>
          <div class="brand-title">JPetStore</div>
          <div class="brand-subtitle">测试平台</div>
        </div>
      </div>
      <el-menu router :default-active="$route.path" class="nav-menu">
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/run">
          <el-icon><VideoPlay /></el-icon>
          <span>执行测试</span>
        </el-menu-item>
        <el-menu-item index="/history">
          <el-icon><Clock /></el-icon>
          <span>执行历史</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="topbar">
        <div>
          <div class="page-title">{{ routeTitle }}</div>
          <div class="page-meta">pytest + Allure + FastAPI</div>
        </div>
        <el-tag effect="plain" type="success">Local</el-tag>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const titleMap = {
  "/dashboard": "仪表盘",
  "/run": "执行测试",
  "/history": "执行历史",
};

const routeTitle = computed(() => {
  if (route.path.startsWith("/history/")) {
    return "执行详情";
  }
  return titleMap[route.path] || "测试平台";
});
</script>
