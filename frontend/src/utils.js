export function formatDateTime(value) {
  if (!value) {
    return "-";
  }
  return new Date(value).toLocaleString("zh-CN", { hour12: false });
}

export function formatDuration(value) {
  if (value === null || value === undefined) {
    return "-";
  }
  return `${Number(value).toFixed(2)}s`;
}

export function statusTagType(status) {
  return status === "passed" ? "success" : "danger";
}

export function openReport(reportUrl) {
  if (!reportUrl) {
    return;
  }
  window.open(reportUrl, "_blank", "noopener,noreferrer");
}
