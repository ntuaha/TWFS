const state = {
  catalog: null,
  rows: [],
  filtered: [],
  institutions: [],
};

const modeSelect = document.getElementById("modeSelect");
const monthSelect = document.getElementById("monthSelect");
const institutionSelect = document.getElementById("institutionSelect");
const bankSearchInput = document.getElementById("bankSearchInput");
const datasetSelect = document.getElementById("datasetSelect");
const keywordInput = document.getElementById("keywordInput");
const monthWrap = document.getElementById("monthWrap");
const institutionWrap = document.getElementById("institutionWrap");
const summary = document.getElementById("summary");
const tableBody = document.getElementById("tableBody");
const meta = document.getElementById("meta");

function fmt(value) {
  if (value === null || value === undefined || value === "") {
    return "";
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    return new Intl.NumberFormat("zh-TW", { maximumFractionDigits: 2 }).format(value);
  }
  return String(value);
}

function fillSelect(selectEl, items, mapLabel = (x) => x, mapValue = (x) => x) {
  selectEl.innerHTML = "";
  for (const item of items) {
    const opt = document.createElement("option");
    opt.value = mapValue(item);
    opt.textContent = mapLabel(item);
    selectEl.appendChild(opt);
  }
}

function updateInstitutionOptions() {
  const query = bankSearchInput.value.trim().toLowerCase();
  const prev = institutionSelect.value;
  const items = !query
    ? state.institutions
    : state.institutions.filter((it) => it.name.toLowerCase().includes(query));

  fillSelect(institutionSelect, items, (it) => it.name, (it) => it.file);
  if (!items.length) {
    return false;
  }
  if (items.some((it) => it.file === prev)) {
    institutionSelect.value = prev;
  }
  return true;
}

async function loadCatalog() {
  const res = await fetch("./data/catalog.json", { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`catalog load failed: ${res.status}`);
  }
  state.catalog = await res.json();

  fillSelect(monthSelect, [...state.catalog.months].reverse());
  state.institutions = state.catalog.institutions || [];
  updateInstitutionOptions();

  for (const ds of state.catalog.datasets) {
    const opt = document.createElement("option");
    opt.value = ds;
    opt.textContent = ds;
    datasetSelect.appendChild(opt);
  }

  meta.textContent = `資料筆數: ${fmt(state.catalog.row_count)} | 更新時間: ${state.catalog.generated_at}`;
}

async function loadRows() {
  const mode = modeSelect.value;
  let url;

  if (mode === "month") {
    const month = monthSelect.value;
    url = `./data/by_month/${month}.json`;
  } else {
    const instFile = institutionSelect.value;
    url = `./data/by_institution/${instFile}`;
  }

  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`data load failed: ${res.status}`);
  }
  state.rows = await res.json();
  applyFilters();
}

function applyFilters() {
  const dataset = datasetSelect.value;
  const keyword = keywordInput.value.trim().toLowerCase();
  const bankQuery = bankSearchInput.value.trim().toLowerCase();

  state.filtered = state.rows.filter((r) => {
    if (dataset !== "ALL" && r.dataset !== dataset) {
      return false;
    }
    if (bankQuery && !String(r.institution || "").toLowerCase().includes(bankQuery)) {
      return false;
    }
    if (!keyword) {
      return true;
    }
    const haystack = `${r.month_key} ${r.dataset} ${r.institution} ${r.item_zh} ${r.item_en}`.toLowerCase();
    return haystack.includes(keyword);
  });

  render();
}

function render() {
  const total = state.filtered.length;
  const limited = state.filtered.slice(0, 500);

  const numericValues = state.filtered
    .map((r) => r.value_num)
    .filter((v) => typeof v === "number" && Number.isFinite(v));

  const sum = numericValues.reduce((acc, v) => acc + v, 0);
  const avg = numericValues.length ? sum / numericValues.length : 0;

  summary.innerHTML = [
    `<div class="card"><div class="k">結果筆數</div><div class="v">${fmt(total)}</div></div>`,
    `<div class="card"><div class="k">數值總和</div><div class="v">${fmt(sum)}</div></div>`,
    `<div class="card"><div class="k">數值平均</div><div class="v">${fmt(avg)}</div></div>`,
    `<div class="card"><div class="k">顯示上限</div><div class="v">500</div></div>`,
  ].join("");

  tableBody.innerHTML = limited
    .map(
      (r) => `
      <tr>
        <td>${r.month_key}</td>
        <td>${r.dataset}</td>
        <td>${r.institution}</td>
        <td>${r.institution_type}</td>
        <td>${r.item_zh}</td>
        <td>${r.item_en}</td>
        <td class="num">${fmt(r.value_num ?? r.value_raw)}</td>
      </tr>
    `
    )
    .join("");
}

function syncModeUI() {
  const isMonth = modeSelect.value === "month";
  monthWrap.classList.toggle("hidden", !isMonth);
  institutionWrap.classList.toggle("hidden", isMonth);
}

async function refreshData() {
  syncModeUI();
  if (!updateInstitutionOptions()) {
    state.rows = [];
    state.filtered = [];
    render();
    return;
  }
  await loadRows();
}

function wireEvents() {
  modeSelect.addEventListener("change", refreshData);
  monthSelect.addEventListener("change", refreshData);
  institutionSelect.addEventListener("change", refreshData);
  bankSearchInput.addEventListener("input", () => {
    if (modeSelect.value === "institution") {
      refreshData();
      return;
    }
    applyFilters();
  });
  datasetSelect.addEventListener("change", applyFilters);
  keywordInput.addEventListener("input", applyFilters);
}

async function main() {
  try {
    await loadCatalog();
    wireEvents();
    await refreshData();
  } catch (err) {
    console.error(err);
    summary.innerHTML = `<div class="error">載入失敗: ${err.message}</div>`;
  }
}

main();
