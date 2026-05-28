<template>
  <div>
    <div class="toolbar">
      <el-button :icon="ArrowLeft" @click="$router.push('/history')">返回历史</el-button>
      <div>
        <el-button
          type="primary"
          :icon="Document"
          :disabled="!run?.allure_report_url"
          @click="openReport(run.allure_report_url)"
        >
          查看 Allure 报告
        </el-button>
        <el-button :icon="Refresh" @click="loadRun" :loading="loading">刷新</el-button>
      </div>
    </div>

    <div class="panel section" v-loading="loading">
      <div class="panel-header">执行详情</div>
      <div class="panel-body" v-if="run">
        <el-descriptions border :column="2">
          <el-descriptions-item label="ID">{{ run.id }}</el-descriptions-item>
          <el-descriptions-item label="Suite">{{ run.suite }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="statusTagType(run.status)">{{ run.status }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="退出码">{{ run.exit_code }}</el-descriptions-item>
          <el-descriptions-item label="Environment">{{ run.environment || "-" }}</el-descriptions-item>
          <el-descriptions-item label="Base URL">{{ run.base_url || "-" }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ formatDateTime(run.started_at) }}</el-descriptions-item>
          <el-descriptions-item label="结束时间">{{ formatDateTime(run.finished_at) }}</el-descriptions-item>
          <el-descriptions-item label="耗时">{{ formatDuration(run.duration_seconds) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(run.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="Allure 结果目录" :span="2">
            {{ run.allure_results_dir }}
          </el-descriptions-item>
          <el-descriptions-item label="Allure 报告目录" :span="2">
            {{ run.allure_report_dir || "未生成" }}
          </el-descriptions-item>
          <el-descriptions-item label="Allure 报告地址" :span="2">
            <el-link
              v-if="run.allure_report_url"
              type="primary"
              @click="openReport(run.allure_report_url)"
            >
              {{ run.allure_report_url }}
            </el-link>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="执行命令" :span="2">
            {{ run.command }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>

    <div class="panel section" v-if="run">
      <div class="panel-header">stdout</div>
      <div class="panel-body">
        <pre class="code-block">{{ run.stdout || "无输出" }}</pre>
      </div>
    </div>

    <div class="panel" v-if="run">
      <div class="panel-header">stderr</div>
      <div class="panel-body">
        <pre class="code-block">{{ run.stderr || "无输出" }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { ArrowLeft, Document, Refresh } from "@element-plus/icons-vue";

import { getTestRun } from "../api";
import { formatDateTime, formatDuration, openReport, statusTagType } from "../utils";

const props = defineProps({
  id: {
    type: String,
    required: true,
  },
});

const run = ref(null);
const loading = ref(false);

async function loadRun() {
  loading.value = true;
  try {
    run.value = await getTestRun(props.id);
  } finally {
    loading.value = false;
  }
}

onMounted(loadRun);
</script>
