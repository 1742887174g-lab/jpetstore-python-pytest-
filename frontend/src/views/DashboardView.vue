<template>
  <div>
    <div class="toolbar">
      <div>
        <el-button :icon="Refresh" @click="loadRuns" :loading="loading">刷新</el-button>
      </div>
    </div>

    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-label">总执行次数</div>
        <div class="stat-value">{{ stats.total }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">通过次数</div>
        <div class="stat-value">{{ stats.passed }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">失败次数</div>
        <div class="stat-value">{{ stats.failed }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">最近通过率</div>
        <div class="stat-value">{{ stats.passRate }}%</div>
      </div>
    </div>

    <div class="section panel">
      <div class="panel-header">Suite 执行分布</div>
      <div class="panel-body">
        <div ref="chartRef" class="chart"></div>
      </div>
    </div>

    <div class="panel">
      <div class="panel-header">最近执行</div>
      <el-table :data="runs.slice(0, 8)" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="suite" label="Suite" width="130" />
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="耗时" width="110">
          <template #default="{ row }">{{ formatDuration(row.duration_seconds) }}</template>
        </el-table-column>
        <el-table-column label="执行时间">
          <template #default="{ row }">{{ formatDateTime(row.started_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button link type="primary" @click="$router.push(`/history/${row.id}`)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from "vue";
import * as echarts from "echarts";
import { Refresh } from "@element-plus/icons-vue";

import { listTestRuns } from "../api";
import { formatDateTime, formatDuration, statusTagType } from "../utils";

const runs = ref([]);
const loading = ref(false);
const chartRef = ref(null);
let chart;

const stats = computed(() => {
  const total = runs.value.length;
  const passed = runs.value.filter((run) => run.status === "passed").length;
  const failed = runs.value.filter((run) => run.status === "failed").length;
  const passRate = total ? Math.round((passed / total) * 100) : 0;
  return { total, passed, failed, passRate };
});

function renderChart() {
  if (!chartRef.value) {
    return;
  }
  chart ||= echarts.init(chartRef.value);
  const grouped = runs.value.reduce((acc, run) => {
    acc[run.suite] = (acc[run.suite] || 0) + 1;
    return acc;
  }, {});
  chart.setOption({
    tooltip: { trigger: "axis" },
    grid: { left: 32, right: 16, top: 24, bottom: 28 },
    xAxis: { type: "category", data: Object.keys(grouped) },
    yAxis: { type: "value", minInterval: 1 },
    series: [
      {
        type: "bar",
        data: Object.values(grouped),
        itemStyle: { color: "#2f80ed", borderRadius: [4, 4, 0, 0] },
      },
    ],
  });
}

async function loadRuns() {
  loading.value = true;
  try {
    runs.value = await listTestRuns({ limit: 100 });
    await nextTick();
    renderChart();
  } finally {
    loading.value = false;
  }
}

onMounted(loadRuns);
</script>
