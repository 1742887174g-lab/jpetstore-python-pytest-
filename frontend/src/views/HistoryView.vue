<template>
  <div class="panel">
    <div class="panel-header">
      <div class="toolbar no-margin">
        <span>执行历史</span>
        <el-button :icon="Refresh" @click="loadRuns" :loading="loading">刷新</el-button>
      </div>
    </div>
    <el-table :data="runs" v-loading="loading" style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="suite" label="Suite" width="130" />
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="exit_code" label="退出码" width="90" />
      <el-table-column label="耗时" width="110">
        <template #default="{ row }">{{ formatDuration(row.duration_seconds) }}</template>
      </el-table-column>
      <el-table-column label="开始时间" min-width="180">
        <template #default="{ row }">{{ formatDateTime(row.started_at) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="120" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/history/${row.id}`)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { Refresh } from "@element-plus/icons-vue";

import { listTestRuns } from "../api";
import { formatDateTime, formatDuration, statusTagType } from "../utils";

const runs = ref([]);
const loading = ref(false);

async function loadRuns() {
  loading.value = true;
  try {
    runs.value = await listTestRuns({ limit: 100 });
  } finally {
    loading.value = false;
  }
}

onMounted(loadRuns);
</script>

<style scoped>
.no-margin {
  margin-bottom: 0;
}
</style>
