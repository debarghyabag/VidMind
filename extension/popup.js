const DEFAULT_API_URL = "https://vidmind-45l8.onrender.com";

const elements = {
  analyzeButton: document.querySelector("#analyzeButton"),
  apiUrl: document.querySelector("#apiUrl"),
  message: document.querySelector("#message"),
  productSpecsButton: document.querySelector("#productSpecsButton"),
  result: document.querySelector("#result"),
  saveApiUrl: document.querySelector("#saveApiUrl"),
  settingsPanel: document.querySelector("#settingsPanel"),
  settingsToggle: document.querySelector("#settingsToggle"),
  summaryButton: document.querySelector("#summaryButton"),
  videoStatus: document.querySelector("#videoStatus")
};

let currentTabUrl = "";

document.addEventListener("DOMContentLoaded", init);

elements.settingsToggle.addEventListener("click", () => {
  elements.settingsPanel.hidden = !elements.settingsPanel.hidden;
});

elements.saveApiUrl.addEventListener("click", async () => {
  const apiUrl = normalizeApiUrl(elements.apiUrl.value);
  await chrome.storage.sync.set({ apiUrl });
  elements.apiUrl.value = apiUrl;
  showMessage("API URL saved.");
});

elements.analyzeButton.addEventListener("click", () => runAction("analyze"));
elements.summaryButton.addEventListener("click", () => runAction("summary"));
elements.productSpecsButton.addEventListener("click", () => runAction("product-specs"));

async function init() {
  const { apiUrl = DEFAULT_API_URL } = await chrome.storage.sync.get("apiUrl");
  elements.apiUrl.value = apiUrl;

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  currentTabUrl = tab?.url || "";

  if (isYouTubeUrl(currentTabUrl)) {
    elements.videoStatus.textContent = new URL(currentTabUrl).hostname;
    elements.result.innerHTML = `<div class="empty">Choose what to extract from this video.</div>`;
    setActionsDisabled(false);
  } else {
    elements.videoStatus.textContent = "Open a YouTube video first";
    elements.result.innerHTML = `<div class="empty">VidMind works from YouTube video pages.</div>`;
    setActionsDisabled(true);
  }
}

async function runAction(action) {
  clearMessage();
  setActionsDisabled(true);

  try {
    const apiUrl = normalizeApiUrl(elements.apiUrl.value);
    let data;

    if (action === "analyze") {
      showMessage("Reading video ID...");
      data = await postJson(`${apiUrl}/video/analyze`, { url: currentTabUrl });
      renderVideoId(data);
    }

    if (action === "summary") {
      showMessage("Preparing transcript chunks...");
      const analysis = await postJson(`${apiUrl}/video/analyze`, { url: currentTabUrl });
      ensureNoApiError(analysis);
      await getJson(`${apiUrl}/video/${encodeURIComponent(analysis.video_id)}/chunks`);
      showMessage("Generating summary...");
      data = await getJson(`${apiUrl}/video/${encodeURIComponent(analysis.video_id)}/summary`);
      renderSummary(data);
    }

    if (action === "product-specs") {
      showMessage("Extracting product specs...");
      data = await postJson(`${apiUrl}/video/product-specs`, { url: currentTabUrl });
      renderProductSpecs(data);
    }

    clearMessage();
  } catch (error) {
    showMessage(error.message || "Something went wrong.", true);
  } finally {
    setActionsDisabled(!isYouTubeUrl(currentTabUrl));
  }
}

async function postJson(url, body) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  return parseApiResponse(response);
}

async function getJson(url) {
  const response = await fetch(url);
  return parseApiResponse(response);
}

async function parseApiResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || data.error || `Request failed with status ${response.status}.`);
  }

  ensureNoApiError(data);
  return data;
}

function ensureNoApiError(data) {
  if (data?.error) {
    throw new Error(data.error);
  }
}

function renderVideoId(data) {
  elements.result.innerHTML = `
    <div class="section-title">Video ID</div>
    <div class="video-id">${escapeHtml(data.video_id || "Unknown")}</div>
  `;
}

function renderSummary(data) {
  elements.result.innerHTML = `
    <div class="section-title">Summary</div>
    <div class="summary">${escapeHtml(data.summary || "No summary returned.")}</div>
  `;
}

function renderProductSpecs(data) {
  const products = Array.isArray(data.products) ? data.products : [];

  if (!products.length) {
    elements.result.innerHTML = `<div class="empty">No products were found in this video.</div>`;
    return;
  }

  elements.result.innerHTML = products.map(renderProduct).join("");
}

function renderProduct(product) {
  const meta = [product.brand, product.category, product.price, product.availability]
    .filter(Boolean)
    .map(escapeHtml)
    .join(" / ");

  const specs = Array.isArray(product.specifications) ? product.specifications : [];
  const features = Array.isArray(product.notable_features) ? product.notable_features : [];

  return `
    <article class="product">
      <h2>${escapeHtml(product.product_name || "Unnamed product")}</h2>
      ${meta ? `<div class="meta">${meta}</div>` : ""}
      ${specs.length ? `
        <div class="section-title">Specifications</div>
        <ul class="spec-list">
          ${specs.map((spec) => `
            <li>
              <span class="spec-name">${escapeHtml(spec.name || "")}</span>
              <span class="spec-value">${escapeHtml(spec.value || "")}</span>
            </li>
          `).join("")}
        </ul>
      ` : ""}
      ${features.length ? `
        <div class="section-title">Notes</div>
        <ul class="feature-list">
          ${features.map((feature) => `<li>${escapeHtml(feature)}</li>`).join("")}
        </ul>
      ` : ""}
    </article>
  `;
}

function showMessage(text, isError = false) {
  elements.message.textContent = text;
  elements.message.classList.toggle("error", isError);
  elements.message.hidden = false;
}

function clearMessage() {
  elements.message.textContent = "";
  elements.message.classList.remove("error");
  elements.message.hidden = true;
}

function setActionsDisabled(disabled) {
  elements.analyzeButton.disabled = disabled;
  elements.summaryButton.disabled = disabled;
  elements.productSpecsButton.disabled = disabled;
}

function normalizeApiUrl(value) {
  return (value || DEFAULT_API_URL).trim().replace(/\/+$/, "");
}

function isYouTubeUrl(value) {
  try {
    const url = new URL(value);
    return ["www.youtube.com", "youtube.com", "m.youtube.com", "youtu.be"].includes(url.hostname);
  } catch {
    return false;
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
