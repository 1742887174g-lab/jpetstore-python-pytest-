<template>
  <div class="panel">
    <div class="panel-header">创建测试执行</div>
    <div class="panel-body">
      <el-form :model="form" label-width="120px" class="run-form">
        <el-form-item label="Suite">
          <el-select v-model="form.suite" style="width: 260px">
            <el-option label="冒烟测试 smoke" value="smoke" />
            <el-option label="接口测试 api" value="api" />
            <el-option label="UI 测试 ui" value="ui" />
            <el-option label="回归测试 regression" value="regression" />
            <el-option label="全量测试 all" value="all" />
          </el-select>
        </el-form-item>
        <el-form-item label="Environment">
          <el-input v-model="form.environment" placeholder="local" style="width: 260px" />
        </el-form-item>
        <el-form-item label="Base URL">
          <el-input
            v-model="form.base_url"
            placeholder="http://localhost:8080/jpetstore"
            style="width: 420px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :icon="VideoPlay" :loading="running" @click="submitRun">
            执行测试
          </el-button>
          <el-button :icon="Clock" @click="$router.push('/history')">查看历史</el-button>
          <el-button
            :icon="Document"
            :disabled="!lastRun?.allure_report_url"
            @click="openReport(lastRun.allure_report_url)"
          >
            查看报告
          </el-button>
        </el-form-item>
      </el-form>

      <el-alert
        v-if="lastRun"
        class="result-alert"
        :title="`执行完成：${lastRun.status}`"
        :type="lastRun.status === 'passed' ? 'success' : 'error'"
        :closable="false"
        show-icon
      />

      <el-descriptions v-if="lastRun" border :column="2" class="result-table">
        <el-descriptions-item label="ID">{{ lastRun.id }}</el-descriptions-item>
        <el-descriptions-item label="Suite">{{ lastRun.suite }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(lastRun.status)">{{ lastRun.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="退出码">{{ lastRun.exit_code }}</el-descriptions-item>
        <el-descriptions-item label="耗时">{{ formatDuration(lastRun.duration_seconds) }}</el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ formatDateTime(lastRun.started_at) }}</el-descriptions-item>
        <el-descriptions-item label="Allure 报告" :span="2">
          <el-link
            v-if="lastRun.allure_report_url"
            type="primary"
            @click="openReport(lastRun.allure_report_url)"
          >
            {{ lastRun.allure_report_url }}
          </el-link>
          <span v-else>未生成</span>
        </el-descriptions-item>
        <el-descriptions-item label="命令" :span="2">{{ lastRun.command }}</el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import { Clock, Document, VideoPlay } from "@element-plus/icons-vue";

import { createTestRun } from "../api";
import { formatDateTime, formatDuration, openReport, statusTagType } from "../utils";

const form = reactive({
  suite: "smoke",
  environment: "local",
  base_url: "http://localhost:8080/jpetstore",
});
const running = ref(false);
const lastRun = ref(null);

async function submitRun() {
  running.value = true;
  try {
    const payload = {
      suite: form.suite,
      environment: form.environment || null,
      base_url: form.base_url || null,
    };
    lastRun.value = await createTestRun(payload);
    ElMessage.success("测试执行完成");
  } catch (error) {
    ElMessage.error(error?.response?.data?.detail || "执行失败");
  } finally {
    running.value = false;
  }
}
</script>

<style scoped>
.run-form {
  max-width: 720px;
}

.result-alert {
  margin: 8px 0 18px;
}

.result-table {
  margin-top: 16px;
}
</style>
