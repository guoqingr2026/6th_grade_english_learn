/**
 * Study Hub v2 — PPT 16:9 全屏 · Part A/B/C/Reading · 词汇高亮 · 精讲导入导出
 */
(function studyHubModule() {
  const HUB_BASE = "data/study-hub";
  const LIBRARY_BASE = "data/study-hub/library";
  const STATE_KEY = "study_hub_state_v1";
  const CUSTOM_KNOWLEDGE_KEY = "study_hub_knowledge_custom_v1";

  const els = {};
  let readingBank = null;
  let knowledgeBank = null;
  let glossary = { words: [], phrases: [] };
  let appendixWordsBank = { words: [], byPage: {} };
  let pageMapMeta = { printPageOffset: 7 };
  let pdfPageMap = null;
  let hubCacheBust = Date.now();

  function applyPdfPageMapFromJson(pm) {
    if (!pm) return;
    pdfPageMap = pm;
    pageMapMeta = { printPageOffset: pm.printPageOffset || 7 };
    const imgBase = pm.imageDir || "assets/images/textbook/pages";
    const syncPage = (page) => {
      if (!page?.id) return;
      let sec = null;
      const introM = page.id.match(/^intro-(.+)$/);
      if (introM) sec = pm.intro?.[introM[1]];
      const appM = page.id.match(/^appendix-(?:k-)?(.+)$/);
      if (appM) sec = pm.appendix?.[appM[1]];
      const unitM = page.id.match(/^u(\d+)-(?:k-)?(.+)$/);
      if (unitM) sec = pm.units?.[unitM[1]]?.[unitM[2]];
      const pdfPages = sec?.pdfPages;
      if (!Array.isArray(pdfPages) || !pdfPages.length) return;
      page.pdfPages = [...pdfPages];
      page.image = `${imgBase}/page-${String(pdfPages[0]).padStart(3, "0")}.png?v=${hubCacheBust}`;
    };
    readingBank?.intro?.pages?.forEach(syncPage);
    readingBank?.appendix?.pages?.forEach(syncPage);
    readingBank?.units?.forEach((u) => u.pages?.forEach(syncPage));
    knowledgeBank?.appendix?.pages?.forEach(syncPage);
    knowledgeBank?.units?.forEach((u) => u.pages?.forEach(syncPage));
  }
  let mode = "reading";
  let section = "units";
  let currentUnit = 1;
  let currentPageId = "";
  let fontScale = 1;
  let darkReading = false;
  let glossaryTerms = [];
  const GLOSSARY_HIGHLIGHT_SEL = "p.en, li.en, td.en, th.en, .sentence-en";
  let imagePageIndex = 0;
  let activePdfPages = [];
  let activePageRef = null;
  let imgScale = 1;
  let imgPanX = 0;
  let imgPanY = 0;
  let imgDragging = false;
  let imgDragStart = { x: 0, y: 0, panX: 0, panY: 0 };
  let readHighlightTimer = null;
  let readHighlightIndex = -1;
  let ttsAbort = false;
  let activePlayback = null;
  let ttsSpeakGen = 0;
  let ttsKeepAliveTimer = null;
  let readingBgColor = "#ffffff";
  let readingEnFontFamily = "Georgia, 'Times New Roman', serif";
  let readingZhFontFamily = "'Microsoft YaHei', 'PingFang SC', sans-serif";
  let readingEnFontScale = 1;
  let readingZhFontScale = 1;
  let readingEnColor = "#1e293b";
  let readingZhColor = "#1d4ed8";
  let readingEnBold = false;
  let readingZhBold = true;
  let readingShowZh = true;
  let ttsRate = 0.88;
  let ttsVoiceUriZh = "";
  let ttsVoiceUriEn = "";
  let ttsVoiceUriLegacy = "";
  let allVoices = [];
  let voiceCache = { ready: false };
  let toastTimer = null;
  const libraryCache = new Map();
  let mobilePanel = "text";
  let audioBank = null;
  let officialAudioEl = null;
  let recordStream = null;
  let recordAudioCtx = null;
  let recordSource = null;
  let recordProcessor = null;
  let recordPcmChunks = [];
  let recordSampleRate = 44100;
  let recordStartMs = 0;
  let studentRecordingActive = false;
  let audioBarRenderedPageId = null;
  const recordUrlCache = new Map();
  const STUDENT_RECORD_DB = "pep6_student_readings_v1";
  const STUDENT_RECORD_STORE = "recordings";
  let snipPendingCategory = "task";
  let snipPendingBlob = null;

  function isMobileLayout() {
    return window.matchMedia("(max-width: 900px)").matches;
  }

  function updateMobilePanelUI() {
    if (!els.split) return;
    const mobile = isMobileLayout();
    if (els.mobileTabs) els.mobileTabs.classList.toggle("hidden", !mobile);
    els.split.classList.remove("mobile-panel-image", "mobile-panel-text", "mobile-panel-both");
    if (mobile) {
      els.split.classList.add(`mobile-panel-${mobilePanel}`);
    }
  }

  function setMobilePanel(panel) {
    mobilePanel = panel;
    if (els.mobileTabs) {
      els.mobileTabs.querySelectorAll(".study-hub-mobile-tab").forEach((btn) => {
        const active = btn.dataset.panel === panel;
        btn.classList.toggle("active", active);
        btn.setAttribute("aria-selected", active ? "true" : "false");
      });
    }
    updateMobilePanelUI();
  }

  function bindMobileTabs() {
    if (!els.mobileTabs) return;
    els.mobileTabs.querySelectorAll(".study-hub-mobile-tab").forEach((btn) => {
      btn.addEventListener("click", () => setMobilePanel(btn.dataset.panel || "text"));
    });
    window.addEventListener("resize", updateMobilePanelUI);
  }

  function cacheElements() {
    els.modal = document.getElementById("studyHubModal");
    if (!els.modal) return false;
    els.stage = document.getElementById("studyHubStage");
    els.title = document.getElementById("studyHubTitle");
    els.units = document.getElementById("studyHubUnits");
    els.parts = document.getElementById("studyHubParts");
    els.image = document.getElementById("studyHubImage");
    els.imageCaption = document.getElementById("studyHubImageCaption");
    els.content = document.getElementById("studyHubContent");
    els.close = document.getElementById("studyHubClose");
    els.fontDown = document.getElementById("studyHubEnFontDown");
    els.fontUp = document.getElementById("studyHubEnFontUp");
    els.zhFontDown = document.getElementById("studyHubZhFontDown");
    els.zhFontUp = document.getElementById("studyHubZhFontUp");
    els.theme = document.getElementById("studyHubTheme");
    els.fullscreen = document.getElementById("studyHubFullscreen");
    els.zoomIn = document.getElementById("studyHubZoomIn");
    els.zoomOut = document.getElementById("studyHubZoomOut");
    els.zoomReset = document.getElementById("studyHubZoomReset");
    els.imageViewport = document.getElementById("studyHubImageViewport");
    els.imageTransform = document.getElementById("studyHubImageTransform");
    els.readModeBtn = document.getElementById("studyHubReadMode");
    els.studentRecordBtn = document.getElementById("studyHubStudentRecord");
    els.readingLangBtn = document.getElementById("studyHubReadingLang");
    els.studentRecordPanel = document.getElementById("studyHubStudentRecordPanel");
    els.importCsv = document.getElementById("studyHubImportCsv");
    els.importCsvFile = document.getElementById("studyHubImportCsvFile");
    els.savePageText = document.getElementById("studyHubSavePageText");
    els.saveKnowledge = document.getElementById("studyHubSaveKnowledge");
    els.snipTask = document.getElementById("studyHubSnipTask");
    els.snipHomework = document.getElementById("studyHubSnipHomework");
    els.snipPanel = document.getElementById("studyHubSnipPanel");
    els.snipModal = document.getElementById("studyHubSnipModal");
    els.snipModalClose = document.getElementById("studyHubSnipModalClose");
    els.snipModalTitle = document.getElementById("studyHubSnipModalTitle");
    els.snipPasteZone = document.getElementById("studyHubSnipPasteZone");
    els.snipPickFile = document.getElementById("studyHubSnipPickFile");
    els.snipFileInput = document.getElementById("studyHubSnipFileInput");
    els.snipSave = document.getElementById("studyHubSnipSave");
    els.snipPreview = document.getElementById("studyHubSnipPreview");
    els.snipViewer = document.getElementById("studyHubSnipViewer");
    els.snipViewerImg = document.getElementById("studyHubSnipViewerImg");
    els.snipViewerCaption = document.getElementById("studyHubSnipViewerCaption");
    els.snipViewerClose = document.getElementById("studyHubSnipViewerClose");
    els.snipViewerBackdrop = document.getElementById("studyHubSnipViewerBackdrop");
    els.bgColor = document.getElementById("studyHubBgColor");
    els.bgPickerWrap = document.getElementById("studyHubBgPickerWrap");
    els.enFontFamily = document.getElementById("studyHubEnFontFamily");
    els.enFontFamilyWrap = document.getElementById("studyHubEnFontFamilyWrap");
    els.zhFontFamily = document.getElementById("studyHubZhFontFamily");
    els.zhFontFamilyWrap = document.getElementById("studyHubZhFontFamilyWrap");
    els.enBold = document.getElementById("studyHubEnBold");
    els.zhColor = document.getElementById("studyHubZhColor");
    els.zhColorWrap = document.getElementById("studyHubZhColorWrap");
    els.enColor = document.getElementById("studyHubEnColor");
    els.enColorWrap = document.getElementById("studyHubEnColorWrap");
    els.ttsRate = document.getElementById("studyHubTtsRate");
    els.ttsRateWrap = document.getElementById("studyHubTtsRateWrap");
    els.ttsRateVal = document.getElementById("studyHubTtsRateVal");
    els.ttsVoiceZh = document.getElementById("studyHubTtsVoiceZh");
    els.ttsVoiceZhWrap = document.getElementById("studyHubTtsVoiceZhWrap");
    els.ttsVoiceEn = document.getElementById("studyHubTtsVoiceEn");
    els.ttsVoiceEnWrap = document.getElementById("studyHubTtsVoiceEnWrap");
    els.zhBold = document.getElementById("studyHubZhBold");
    els.pageEditor = document.getElementById("studyHubPageEditor");
    els.audioBar = document.getElementById("studyHubAudioBar");
    els.pageLabel = document.getElementById("studyHubPageLabel");
    els.toast = document.getElementById("studyHubToast");
    els.refreshKnowledge = null;
    els.importUrl = null;
    els.importFile = null;
    els.imagePrev = document.getElementById("studyHubImagePrev");
    els.imageNext = document.getElementById("studyHubImageNext");
    els.imagePager = document.getElementById("studyHubImagePager");
    els.readAll = null;
    els.exportKnowledge = null;
    els.importKnowledge = null;
    els.openReading = document.getElementById("openTextbookReading");
    els.openKnowledge = document.getElementById("openKnowledgeLecture");
    els.switchKnowledge = document.getElementById("studyHubSwitchKnowledge");
    els.switchReading = document.getElementById("studyHubSwitchReading");
    els.richToolbar = document.getElementById("studyHubRichToolbar");
    els.imagePane = document.querySelector(".study-hub-image-pane");
    els.contentPane = document.querySelector(".study-hub-content-pane");
    els.mobileTabs = document.getElementById("studyHubMobileTabs");
    els.split = document.getElementById("studyHubSplit");
    els.insertImage = document.getElementById("studyHubInsertImage");
    els.insertImageFile = document.getElementById("studyHubInsertImageFile");
    els.insertTable = document.getElementById("studyHubInsertTable");
    els.insertLink = document.getElementById("studyHubInsertLink");
    els.insertAudio = document.getElementById("studyHubInsertAudio");
    els.insertAudioFile = document.getElementById("studyHubInsertAudioFile");
    els.insertVideo = document.getElementById("studyHubInsertVideo");
    return true;
  }

  function loadJson(key, fallback) {
    try {
      const raw = window.localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  }

  function saveJson(key, data) {
    window.localStorage.setItem(key, JSON.stringify(data));
  }

  function loadState() {
    return loadJson(STATE_KEY, {});
  }

  function saveState() {
    saveJson(STATE_KEY, {
      mode,
      section,
      currentUnit,
      currentPageId,
      fontScale,
      readingEnFontScale,
      readingZhFontScale,
      darkReading,
      readingBgColor,
      readingEnFontFamily,
      readingZhFontFamily,
      readingEnColor,
      readingZhColor,
      readingEnBold,
      readingZhBold,
      readingShowZh,
      ttsRate,
      ttsVoiceUriZh,
      ttsVoiceUriEn,
    });
    touchSyncTimestamp();
  }

  function loadCustomKnowledge() {
    return loadJson(CUSTOM_KNOWLEDGE_KEY, null);
  }

  function saveCustomKnowledge(bank) {
    saveJson(CUSTOM_KNOWLEDGE_KEY, bank);
    touchSyncTimestamp();
  }

  function mergeKnowledgeBanks(base, custom) {
    if (!custom?.units && !custom?.appendix?.pages) return base;
    const map = new Map();
    (base.units || []).forEach((u) => {
      (u.pages || []).forEach((p) => map.set(p.id, { ...p }));
    });
    (custom.units || []).forEach((u) => {
      (u.pages || []).forEach((p) => {
        map.set(p.id, { ...(map.get(p.id) || {}), ...p });
      });
    });
    const byUnit = {};
    map.forEach((page) => {
      const m = page.id.match(/^u(\d+)-/);
      const unitNum = m ? Number(m[1]) : 1;
      if (!byUnit[unitNum]) byUnit[unitNum] = [];
      byUnit[unitNum].push(page);
    });
    const appendixMap = new Map();
    (base.appendix?.pages || []).forEach((p) => appendixMap.set(p.id, { ...p }));
    (custom.appendix?.pages || []).forEach((p) => {
      appendixMap.set(p.id, { ...appendixMap.get(p.id), ...p });
    });
    return {
      ...base,
      ...custom,
      units: (base.units || []).map((u) => ({
        ...u,
        pages: (byUnit[u.unit] || u.pages).sort((a, b) => a.id.localeCompare(b.id)),
      })),
      appendix: base.appendix
        ? {
            ...base.appendix,
            pages: Array.from(appendixMap.values()).sort((a, b) => a.id.localeCompare(b.id)),
          }
        : custom.appendix,
    };
  }

  function getBank() {
    return mode === "reading" ? readingBank : knowledgeBank;
  }

  function getSectionPages() {
    const bank = getBank();
    if (section === "intro") return bank?.intro?.pages || [];
    if (section === "appendix") return bank?.appendix?.pages || [];
    const unit = bank?.units?.find((u) => u.unit === currentUnit);
    return unit?.pages || [];
  }

  function getUnitData(unitNum) {
    const bank = getBank();
    return bank?.units?.find((u) => u.unit === unitNum) || bank?.units?.[0];
  }

  function getCurrentPage() {
    const pages = getSectionPages();
    if (!pages.length) return null;
    return pages.find((p) => p.id === currentPageId) || pages[0];
  }

  function isReadableSentence(row) {
    const en = (row?.en || "").trim();
    if (!en && !row?.zh) return false;
    if (en.startsWith("<") || en.includes("</")) return false;
    if (en.includes("知识点精讲")) return false;
    return true;
  }

  function printedPageForPng(png) {
    const n = Number(png);
    if (n <= 8) return n;
    return n - (pageMapMeta.printPageOffset || 7);
  }

  function pngForPrintedPage(printed) {
    const p = Number(printed);
    if (p <= 8) return p;
    return p + (pageMapMeta.printPageOffset || 7);
  }

  function readingLibraryScope() {
    if (section === "intro") return "intro";
    if (section === "appendix") return "appendix";
    return "unit";
  }

  function libraryReadingPath(unit, png, scope) {
    const sc = scope || readingLibraryScope();
    const padded = String(png).padStart(3, "0");
    if (sc === "intro" || sc === "appendix") {
      return `${LIBRARY_BASE}/reading/${sc}-p${padded}.html`;
    }
    return `${LIBRARY_BASE}/reading/u${unit}-p${padded}.html`;
  }

  function libraryKnowledgePath(pageId) {
    return `${LIBRARY_BASE}/knowledge/${pageId}.html`;
  }

  function showToast(msg, isError) {
    if (!els.toast) {
      if (msg) window.alert(msg);
      return;
    }
    els.toast.textContent = msg;
    els.toast.classList.remove("hidden", "error");
    if (isError) els.toast.classList.add("error");
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      els.toast.classList.add("hidden");
    }, 4500);
  }

  function sanitizeForSave(text) {
    return String(text || "").replace(/[\x00-\x08\x0b\x0c\x0e-\x1f]/g, "");
  }

  async function parseApiResponse(res) {
    const text = await res.text();
    try {
      return { ok: res.ok, data: JSON.parse(text) };
    } catch {
      const hint = text.includes("<!DOCTYPE") || text.includes("<html")
        ? "8080 端口仍是旧服务：请关闭所有命令行窗口，重新双击根目录 启动.bat（应显示 Study Hub API v3）"
        : text.slice(0, 120);
      throw new Error(res.ok ? `服务器响应异常：${hint}` : `保存失败：${hint}`);
    }
  }

  function getEditorHtml(el) {
    if (!el) return "";
    return sanitizeRichHtml(el.innerHTML || "");
  }

  async function ensureSaveApiReady() {
    try {
      const res = await fetch("/api/ping");
      const data = await parseApiResponse(res);
      if (!data.data?.studyHubApi || data.data.studyHubApi < 3) {
        throw new Error(
          "当前 8080 端口仍是旧服务。请关闭所有黑色命令行窗口后，重新双击根目录 启动.bat；窗口中应出现 Study Hub API v3",
        );
      }
    } catch (err) {
      throw new Error(
        err?.message ||
          "无法连接本地服务。请关闭旧窗口，重新双击根目录 启动.bat，并用 http://localhost:8080 打开",
      );
    }
  }

  async function postSavePage(payload, rawQuery) {
    await ensureSaveApiReady();
    const adminPin =
      (typeof getAdminPin === "function" ? getAdminPin() : "") ||
      window.localStorage.getItem("english_grade6_admin_pin_v1") ||
      "";
    const deviceQ = `&device=${encodeURIComponent(/Mobile/i.test(navigator.userAgent) ? "手机" : "电脑")}`;
    const pinQ = adminPin ? `&adminPin=${encodeURIComponent(adminPin)}` : "";
    const res = await fetch(`/api/study-hub/save-page-raw?${rawQuery}${pinQ}${deviceQ}`, {
      method: "POST",
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        ...(adminPin ? { "X-Admin-Pin": adminPin } : {}),
      },
      body: sanitizeForSave(payload.html || payload.text || ""),
    });
    const { ok, data } = await parseApiResponse(res);
    if (!ok) throw new Error(data.error || "保存失败");
    if (data.pending) {
      showToast(data.message || "已提交主机管理员审核", false);
    }
    return data;
  }

  const EMOJI_FONT_STACK = '"Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif';
  const ZH_CHAR_RE = /[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]/;
  const EMOJI_SYMBOL_RE = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}\u{200D}\u{20E3}\u{E0020}-\u{E007F}]/u;
  const TTS_BLANK_MARK_RE = /[_＿﹍▁￣﹏﹉﹊﹋﹌]+/g;
  const TTS_BOX_DRAWING_RE =
    /[\u2500-\u257F\u2580-\u259F│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬]+/g;
  const TTS_DECORATIVE_SYMBOL_RE =
    /[★☆●○◆◇▪▫✓✔✗✘♪♫🎧🎵🎯🏰🔑📖✍️🌟🌿🌳📚📌✔️👦👧🧒🧑🤧🎂😴😢🤒😷]/g;
  const READABLE_CHAR_RE = /[\u4e00-\u9fffA-Za-z0-9]/;
  const KNOWLEDGE_TTS_BLOCK_TAGS = new Set(["P", "LI", "H1", "H2", "H3", "H4", "BLOCKQUOTE"]);
  const KNOWLEDGE_TTS_SKIP_SEL = ".tip-box, .grammar-hints, .katex";

  function hasChinese(text) {
    return ZH_CHAR_RE.test(text || "");
  }

  function isEmojiOrSymbolPrefix(text) {
    const t = (text || "").trim();
    if (!t || hasChinese(t)) return false;
    const latin = (t.match(/[A-Za-z]/g) || []).length;
    if (latin >= 4) return false;
    if (EMOJI_SYMBOL_RE.test(t)) return true;
    if (latin === 0) return true;
    return latin < 4 && !/[A-Za-z]{2,}/.test(t);
  }

  function combinePrefixZh(prefix, zh) {
    const p = (prefix || "").trim();
    const z = (zh || "").trim();
    if (!p) return z;
    if (z.startsWith(p)) return z;
    return `${p} ${z}`;
  }

  function mergePrefixBlocks(blocks) {
    const merged = [];
    let i = 0;
    while (i < blocks.length) {
      const cur = blocks[i];
      const kind = classifyLineText(cur.text, cur.hint);
      if (
        i + 1 < blocks.length &&
        kind === "en" &&
        isEmojiOrSymbolPrefix(cur.text) &&
        classifyLineText(blocks[i + 1].text, blocks[i + 1].hint) === "zh"
      ) {
        merged.push({
          text: combinePrefixZh(cur.text, blocks[i + 1].text),
          hint: "zh",
        });
        i += 2;
        continue;
      }
      merged.push({ ...cur });
      i += 1;
    }
    return merged;
  }

  function classifyLineText(text, hint) {
    if (hint === "en" || hint === "zh") return hint;
    const t = (text || "").trim();
    if (!t) return "en";
    if (!hasChinese(t)) return "en";
    const latin = (t.match(/[A-Za-z]/g) || []).length;
    const cjk = (t.match(ZH_CHAR_RE) || []).length;
    if (cjk > 0 && latin < 3) return "zh";
    if (cjk > latin) return "zh";
    if (cjk > 0 && latin > 0 && cjk >= latin * 0.6) return "zh";
    return "en";
  }

  function tableCellHint(headers, idx, text) {
    const h = (headers[idx] || "").toLowerCase();
    if (/英文|单词|音标|词性|例句|english|word|ipa|modal|phr|adj|n\.|v\./i.test(h)) return "en";
    if (/中文|释义|meaning|翻译/i.test(h)) return "zh";
    if (idx === 0) return "en";
    if (idx === 1 && hasChinese(text) && !/[A-Za-z]{3,}/.test(text)) return "zh";
    return classifyLineText(text, "");
  }

  function cleanKnowledgeDom(root) {
    if (!root) return;
    root.querySelectorAll("[style]").forEach((el) => {
      el.removeAttribute("style");
    });
    root.querySelectorAll("font").forEach((el) => {
      const span = document.createElement("span");
      span.innerHTML = el.innerHTML;
      el.replaceWith(span);
    });
    root.querySelectorAll("section.reading-excerpt").forEach((el) => el.remove());
    root.querySelectorAll("table").forEach((table) => {
      table.classList.add("rich-table");
      const headers = [...table.querySelectorAll("thead th, tr:first-child th")].map((th) =>
        (th.textContent || "").trim(),
      );
      table.querySelectorAll("tr").forEach((tr) => {
        [...tr.children].forEach((cell, idx) => {
          if (cell.tagName !== "TD" && cell.tagName !== "TH") return;
          const text = (cell.textContent || "").trim();
          if (!text) return;
          const kind = tableCellHint(headers, idx, text);
          cell.classList.remove("en", "zh");
          cell.classList.add(kind);
          cell.querySelectorAll("span, strong, code, em").forEach((inner) => {
            if (!inner.classList.contains("en") && !inner.classList.contains("zh")) {
              inner.classList.add(kind);
            }
          });
        });
      });
    });
    root.querySelectorAll("pre, code").forEach((el) => {
      const text = (el.textContent || "").trim();
      if (!text) return;
      el.classList.remove("en", "zh");
      el.classList.add(classifyLineText(text, ""));
    });
    root.querySelectorAll("h1, h2, h3, h4, h5, p, li, blockquote, td, th, span, strong").forEach((el) => {
      if (el.closest(".teaching-focus")) return;
      const text = (el.textContent || "").trim();
      if (!text || el.classList.contains("en") || el.classList.contains("zh")) return;
      if (el.children.length && el.tagName !== "TD" && el.tagName !== "TH") return;
      el.classList.add(classifyLineText(text, ""));
    });
  }

  function classifyKnowledgeContent(root) {
    if (!root) return;
    cleanKnowledgeDom(root);
    const skipSel = ".tip-box, .grammar-hints, .katex";
    root.querySelectorAll("p, li, h1, h2, h3, h4, blockquote, pre").forEach((el) => {
      if (el.closest(skipSel) || el.matches(skipSel)) return;
      const text = (el.textContent || "").trim();
      if (!text) return;
      if (!el.classList.contains("en") && !el.classList.contains("zh")) {
        el.classList.add(classifyLineText(text, ""));
      }
    });
    root.querySelectorAll(".teaching-focus").forEach((el) => el.classList.add("zh"));
    applyBilingualStyles(root);
  }

  function extractBlocksFromHtml(html) {
    const wrap = document.createElement("div");
    wrap.innerHTML = sanitizeForSave(html);
    const blocks = [];
    const blockTags = new Set(["P", "DIV", "LI", "H1", "H2", "H3", "H4", "H5", "H6"]);
    const walk = (node) => {
      if (node.nodeType === Node.TEXT_NODE) {
        const t = (node.textContent || "").trim();
        if (t) blocks.push({ text: t, hint: "" });
        return;
      }
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      const tag = node.tagName;
      if (tag === "BR") return;
      if (blockTags.has(tag)) {
        const text = (node.textContent || "").trim();
        if (!text) return;
        let hint = "";
        if (node.classList.contains("zh")) hint = "zh";
        else if (node.classList.contains("en")) hint = "en";
        blocks.push({ text, hint });
        return;
      }
      Array.from(node.childNodes).forEach(walk);
    };
    Array.from(wrap.childNodes).forEach(walk);
    if (!blocks.length) {
      htmlToPlainText(html)
        .split(/\n/)
        .map((l) => l.trim())
        .filter(Boolean)
        .forEach((text) => blocks.push({ text, hint: "" }));
    }
    return blocks;
  }

  function sanitizeRichHtml(html) {
    let out = sanitizeForSave(html || "");
    out = out.replace(/<script[\s\S]*?<\/script>/gi, "");
    out = out.replace(/<style[\s\S]*?<\/style>/gi, "");
    out = out.replace(/\s+on\w+\s*=\s*(['"]).*?\1/gi, "");
    out = out.replace(/javascript:/gi, "");
    return out.trim();
  }

  const sanitizeKnowledgeHtml = sanitizeRichHtml;

  function setContentPaneStyleVars() {
    if (!els.contentPane) return;
    els.contentPane.style.setProperty("--study-hub-font-scale", String(fontScale));
    els.contentPane.style.setProperty("--study-hub-en-font-scale", String(readingEnFontScale));
    els.contentPane.style.setProperty("--study-hub-zh-font-scale", String(readingZhFontScale));
    els.contentPane.style.setProperty("--study-hub-en-color", readingEnColor);
    els.contentPane.style.setProperty("--study-hub-zh-color", readingZhColor);
    els.contentPane.style.setProperty("--study-hub-en-weight", readingEnBold ? "700" : "400");
    els.contentPane.style.setProperty("--study-hub-zh-weight", readingZhBold ? "700" : "400");
    els.contentPane.style.setProperty("--study-hub-en-font-family", readingEnFontFamily);
    els.contentPane.style.setProperty("--study-hub-zh-font-family", readingZhFontFamily);
    els.contentPane.style.setProperty(
      "--study-hub-text-font",
      `${readingZhFontFamily}, ${EMOJI_FONT_STACK}`,
    );
    els.contentPane.style.setProperty("--study-hub-reading-bg", readingBgColor);
  }

  function applyBilingualStyles(root) {
    if (!root) return;
    root.querySelectorAll(".en, .zh").forEach((el) => {
      const isZh = el.classList.contains("zh");
      el.style.color = isZh ? readingZhColor : readingEnColor;
      el.style.fontWeight = (isZh ? readingZhBold : readingEnBold) ? "700" : "400";
      el.style.fontFamily = isZh ? readingZhFontFamily : readingEnFontFamily;
    });
  }

  function normalizeEditorHtml(html) {
    const blocks = mergePrefixBlocks(extractBlocksFromHtml(html));
    if (!blocks.length) return "";
    const zhStyle = `color:${readingZhColor};font-weight:${readingZhBold ? "700" : "400"};font-family:${readingZhFontFamily}`;
    const enStyle = `color:${readingEnColor};font-weight:${readingEnBold ? "700" : "400"};font-family:${readingEnFontFamily}`;
    return blocks
      .map((block) => {
        const kind = classifyLineText(block.text, block.hint);
        const text = escapeHtml(block.text);
        if (kind === "zh") return `<p class="zh" style="${zhStyle}">${text}</p>`;
        return `<p class="en" style="${enStyle}">${text}</p>`;
      })
      .join("\n");
  }

  function applyReadingLangDisplay() {
    if (els.contentPane) {
      els.contentPane.classList.toggle("reading-en-only", !readingShowZh);
    }
    updateReadingLangDisplayBtn();
  }

  function updateReadingLangDisplayBtn() {
    if (!els.readingLangBtn) return;
    if (readingShowZh) {
      els.readingLangBtn.textContent = "仅英文";
      els.readingLangBtn.title = "切换为仅显示英文";
      els.readingLangBtn.classList.remove("active");
    } else {
      els.readingLangBtn.textContent = "中英对照";
      els.readingLangBtn.title = "切换为中英文对照显示";
      els.readingLangBtn.classList.add("active");
    }
  }

  function toggleReadingLangDisplay() {
    readingShowZh = !readingShowZh;
    applyReadingLangDisplay();
    saveState();
    showToast(readingShowZh ? "已切换为中英文对照" : "已切换为仅英文显示", false);
  }

  function applyReadingZhStyles(root) {
    if (!root) return;
    classifyKnowledgeContent(root);
  }

  function applyKnowledgeDisplayStyles() {
    const body = getKnowledgeBodyEl();
    if (!body || mode !== "knowledge") return;
    const scaled = `${fontScale}rem`;
    if (els.contentPane) {
      els.contentPane.dataset.mode = "knowledge";
      setContentPaneStyleVars();
    }
    if (els.content) {
      els.content.style.fontSize = scaled;
      els.content.style.fontFamily = `${readingZhFontFamily}, ${EMOJI_FONT_STACK}`;
      els.content.style.backgroundColor = readingBgColor;
    }
    if (els.contentPane) {
      els.contentPane.style.backgroundColor = readingBgColor;
    }
    body.style.fontSize = scaled;
    body.style.fontFamily = `${readingZhFontFamily}, ${EMOJI_FONT_STACK}`;
    body.style.backgroundColor = "transparent";
    classifyKnowledgeContent(body);
  }

  function refreshEditableContent() {
    if (els.pageEditor && !els.pageEditor.classList.contains("hidden")) {
      applyReadingZhStyles(els.pageEditor);
    }
    if (mode === "knowledge") {
      const body = getKnowledgeBodyEl();
      if (body) classifyKnowledgeContent(body);
      applyKnowledgeDisplayStyles();
    }
  }

  function applyEditorStyle() {
    setContentPaneStyleVars();
    if (els.enBold) els.enBold.classList.toggle("active", readingEnBold);
    if (els.zhBold) els.zhBold.classList.toggle("active", readingZhBold);
    if (mode === "knowledge") {
      applyKnowledgeDisplayStyles();
      return;
    }
    const font = `${readingZhFontFamily}, ${EMOJI_FONT_STACK}`;
    const targets = [els.pageEditor, els.content].filter(Boolean);
    targets.forEach((el) => {
      el.style.fontSize = `${fontScale}rem`;
      el.style.fontFamily = font;
      el.style.backgroundColor = readingBgColor;
    });
    if (els.contentPane) {
      els.contentPane.style.backgroundColor = readingBgColor;
    }
    refreshEditableContent();
  }

  function htmlToPlainText(html) {
    const div = document.createElement("div");
    div.innerHTML = html || "";
    return (div.textContent || div.innerText || "").trim();
  }

  function plainTextToHtml(text) {
    return (text || "")
      .split(/\n/)
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => `<p>${escapeHtml(line)}</p>`)
      .join("\n");
  }

  function defaultReadingHtml(page) {
    const sentences = sentencesForCurrentImage(page);
    if (!sentences.length) return "";
    return sentences
      .filter(isReadableSentence)
      .map((s) => {
        const parts = [];
        if (s.en) parts.push(`<p class="en">${escapeHtml(s.en)}</p>`);
        if (s.zh) parts.push(`<p class="zh">${escapeHtml(s.zh)}</p>`);
        return parts.join("");
      })
      .join("\n");
  }

  async function fetchLibraryHtml(url) {
    const cacheKey = url;
    if (libraryCache.has(cacheKey)) return libraryCache.get(cacheKey);
    try {
      const res = await fetch(`${url}?t=${Date.now()}`);
      if (res.ok) {
        const text = (await res.text()).trim();
        if (text) {
          libraryCache.set(cacheKey, text);
          return text;
        }
      }
    } catch {
      /* static miss */
    }
    return null;
  }

  async function fetchReadingLibrary(unit, png) {
    const scope = readingLibraryScope();
    const apiUrl = `/api/study-hub/library-page?kind=reading&scope=${scope}&unit=${unit}&png=${png}`;
    const bust = `t=${Date.now()}`;
    try {
      const res = await fetch(`${apiUrl}&${bust}`, { cache: "no-store" });
      if (res.ok) {
        const data = await res.json();
        if (data.exists && data.html) return data.html;
      }
    } catch {
      /* offline */
    }
    let html = await fetchLibraryHtml(libraryReadingPath(unit, png, scope));
    if (!html && (scope === "intro" || scope === "appendix")) {
      html = await fetchLibraryHtml(libraryReadingPath(unit, png, "unit"));
    }
    return html;
  }

  async function fetchKnowledgeLibrary(pageId) {
    try {
      const res = await fetch(`/api/study-hub/library-page?kind=knowledge&pageId=${encodeURIComponent(pageId)}&t=${Date.now()}`, {
        cache: "no-store",
      });
      if (res.ok) {
        const data = await res.json();
        if (data.exists && data.html) return data.html;
      }
    } catch {
      /* offline */
    }
    return fetchLibraryHtml(libraryKnowledgePath(pageId));
  }

  async function getReadingContent(page) {
    const png = activePdfPages[imagePageIndex];
    if (!png) return { html: "", plain: "" };
    const lib = await fetchReadingLibrary(currentUnit, png);
    if (lib) return { html: lib, plain: htmlToPlainText(lib) };
    const def = defaultReadingHtml(page);
    return { html: def, plain: htmlToPlainText(def) };
  }

  async function saveReadingToLibrary(htmlContent) {
    const png = activePdfPages[imagePageIndex];
    if (!png) return;
    const scope = readingLibraryScope();
    const html = sanitizeRichHtml(htmlContent);
    const data = await postSavePage(
      { kind: "reading", unit: currentUnit, png, html, scope },
      `kind=reading&scope=${encodeURIComponent(scope)}&unit=${currentUnit}&png=${png}`,
    );
    libraryCache.set(libraryReadingPath(currentUnit, png, scope), html);
    if (els.pageEditor) els.pageEditor.innerHTML = html;
    touchSyncTimestamp();
    if (typeof scheduleLanSync === "function") scheduleLanSync(true);
    const pageLabel = data.printedPage || printedPageForPng(png);
    const toastMsg =
      scope === "unit"
        ? `已保存 Page ${pageLabel}（HTML 富文本；CSV 仅同步纯文本）`
        : `已保存 Page ${pageLabel}（HTML 富文本）`;
    showToast(toastMsg, false);
  }

  async function saveKnowledgeToLibrary(html) {
    const pageId = currentPageId;
    if (!pageId) return;
    const baked = sanitizeKnowledgeHtml(html);
    await postSavePage(
      { kind: "knowledge", pageId, html: baked },
      `kind=knowledge&pageId=${encodeURIComponent(pageId)}`,
    );
    libraryCache.set(libraryKnowledgePath(pageId), baked);
    const body = els.content?.querySelector(".knowledge-body");
    if (body) body.innerHTML = baked;
    touchSyncTimestamp();
    if (typeof scheduleLanSync === "function") scheduleLanSync(true);
    showToast("精讲已保存到 HTML 文档库（支持图片/表格/链接/音视频）", false);
  }

  function pngForBookPage(unit, bookPage) {
    return pngForPrintedPage(bookPage);
  }

  function sentencesToPlainText(sentences) {
    return sentences
      .filter(isReadableSentence)
      .map((s) => {
        const parts = [];
        if (s.en) parts.push(s.en);
        if (s.zh) parts.push(s.zh);
        return parts.join("\n");
      })
      .filter(Boolean)
      .join("\n\n");
  }

  function parseCsvSimple(text) {
    const raw = text.replace(/^\uFEFF/, "");
    const lines = raw.split(/\r?\n/).filter((l) => l.trim());
    if (!lines.length) return [];
    const splitRow = (line) => {
      const out = [];
      let cur = "";
      let inQ = false;
      for (let i = 0; i < line.length; i += 1) {
        const c = line[i];
        if (c === '"') inQ = !inQ;
        else if (c === "," && !inQ) {
          out.push(cur.trim());
          cur = "";
        } else cur += c;
      }
      out.push(cur.trim());
      return out;
    };
    const header = splitRow(lines[0]).map((h) => h.toLowerCase().replace(/"/g, ""));
    const hasHeader = header[0] === "page" || header[0] === "页码" || header[0] === "pages";
    const pi = hasHeader
      ? header.indexOf("page") >= 0
        ? header.indexOf("page")
        : header.indexOf("页码")
      : 0;
    const ei = hasHeader
      ? ["en", "english", "英文"].map((k) => header.indexOf(k)).find((i) => i >= 0) ?? 1
      : 1;
    const zi = hasHeader
      ? ["zh", "chinese", "中文"].map((k) => header.indexOf(k)).find((i) => i >= 0) ?? 2
      : 2;
    const rows = [];
    const start = hasHeader ? 1 : 0;
    for (let i = start; i < lines.length; i += 1) {
      const cols = splitRow(lines[i]);
      const page = parseInt(cols[pi], 10);
      if (!page) continue;
      rows.push({ page, en: (cols[ei] || "").replace(/^"|"$/g, ""), zh: (cols[zi] || "").replace(/^"|"$/g, "") });
    }
    return rows;
  }

  async function importCsvToLibrary(text, unitNum) {
    const adminPin =
      (typeof getAdminPin === "function" ? getAdminPin() : "") ||
      window.localStorage.getItem("english_grade6_admin_pin_v1") ||
      "";
    const res = await fetch("/api/study-hub/import-csv", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(adminPin ? { "X-Admin-Pin": adminPin } : {}),
      },
      body: JSON.stringify({
        unit: unitNum,
        csv: text,
        adminPin,
        device: /Mobile/i.test(navigator.userAgent) ? "手机" : "电脑",
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "CSV 导入失败，请用 启动.bat 启动服务");
    if (data.pending) {
      showToast(data.message || "CSV 已提交主机审核", false);
      return data;
    }
    libraryCache.clear();
    return data;
  }

  async function renderReadingEditor(page) {
    const pngNum = activePdfPages[imagePageIndex];
    const printed = pngNum ? printedPageForPng(pngNum) : null;
    if (els.pageLabel) {
      els.pageLabel.classList.remove("hidden");
      els.pageLabel.textContent = printed != null ? `Page ${printed}` : "";
    }
    if (els.pageEditor) {
      els.pageEditor.classList.remove("hidden");
      const content = await getReadingContent(page);
      const raw = content.html || plainTextToHtml(content.plain);
      els.pageEditor.innerHTML = sanitizeRichHtml(raw);
      applyEditorStyle();
      applyReadingZhStyles(els.pageEditor);
      applyGlossaryHighlights(els.pageEditor);
      renderMathIn(els.pageEditor);
    }
    if (els.content) {
      els.content.classList.add("hidden");
      els.content.contentEditable = "false";
      els.content.classList.remove("editable");
    }
    if (els.contentPane) els.contentPane.classList.add("reading-mode");
    applyReadingLangDisplay();
    await renderStudyHubAudioBar(page.id);
    await refreshStudentRecordPanel(page.id);
    if (els.snipPanel) {
      els.snipPanel.classList.add("hidden");
      els.snipPanel.innerHTML = "";
    }
  }

  async function saveCurrentPageText() {
    if (!els.pageEditor) return;
    try {
      await saveReadingToLibrary(getEditorHtml(els.pageEditor));
    } catch (err) {
      showToast(err?.message || "保存失败", true);
    }
  }

  async function importCsvFromFile(file) {
    const text = await file.text();
    try {
      const data = await importCsvToLibrary(text, currentUnit || 1);
      await renderReadingEditor(getCurrentPage());
      showToast(`已导入 ${data.rows} 行 CSV，写入 ${data.pages} 页 HTML`, false);
    } catch (err) {
      showToast(err?.message || "CSV 导入失败", true);
      throw err;
    }
  }

  function bookPageForPng(png) {
    return printedPageForPng(png);
  }

  function sentencesForCurrentImage(page) {
    if (!page) return [];
    const contents = page.pageContents || [];
    if (contents.length && activePdfPages.length) {
      const pg = activePdfPages[imagePageIndex];
      const block = contents.find((c) => c.page === pg);
      if (block?.sentences?.length) {
        return block.sentences.filter(isReadableSentence);
      }
    }
    return (page.sentences || []).filter(isReadableSentence);
  }

  function getCurrentBookPage() {
    const png = activePdfPages[imagePageIndex];
    if (!png) return null;
    const printed = printedPageForPng(png);
    return Number.isFinite(printed) ? printed : null;
  }

  function buildGlossaryTerms() {
    glossaryTerms = [];
  }

  function refreshGlossaryTermsForCurrentPage() {
    glossaryTerms = [];
    const page = getCurrentBookPage();
    if (page == null || !appendixWordsBank?.byPage) return;
    const pageKey = String(page);
    const wordsOnPage = appendixWordsBank.byPage[pageKey] || [];
    const metaByWord = new Map();
    (appendixWordsBank.words || []).forEach((entry) => {
      if (entry.page === page) {
        metaByWord.set(entry.word.toLowerCase(), entry);
      }
    });
    glossaryTerms = wordsOnPage.map((word) => {
      const meta = metaByWord.get(word.toLowerCase()) || { word, page, gloss: "" };
      return {
        word,
        page: meta.page || page,
        gloss: meta.gloss || "",
        level2: !!meta.level2,
      };
    });
    glossaryTerms.sort((a, b) => b.word.length - a.word.length);
  }

  function isGlossaryWordChar(ch) {
    return /[A-Za-z0-9]/.test(ch || "");
  }

  function isGlossaryTermBoundary(text, start, end) {
    const before = start > 0 ? text[start - 1] : "";
    const after = end < text.length ? text[end] : "";
    if (before && isGlossaryWordChar(before)) return false;
    if (after && isGlossaryWordChar(after)) return false;
    return true;
  }

  function findGlossaryTermSpans(text, term) {
    const spans = [];
    if (!term) return spans;
    const lower = text.toLowerCase();
    const tLower = term.toLowerCase();
    let idx = 0;
    while (idx < lower.length) {
      const pos = lower.indexOf(tLower, idx);
      if (pos === -1) break;
      const end = pos + term.length;
      if (isGlossaryTermBoundary(text, pos, end)) {
        spans.push({ start: pos, end });
      }
      idx = pos + 1;
    }
    return spans;
  }

  function getEditorSentencePairs() {
    if (!els.pageEditor) return [];
    const nodes = [...els.pageEditor.querySelectorAll("p.en, p.zh")];
    const pairs = [];
    let i = 0;
    while (i < nodes.length) {
      const node = nodes[i];
      if (node.classList.contains("en")) {
        const enEl = node;
        let zhEl = null;
        if (i + 1 < nodes.length && nodes[i + 1].classList.contains("zh")) {
          zhEl = nodes[i + 1];
          i += 2;
        } else {
          i += 1;
        }
        pairs.push({
          en: (enEl.textContent || "").trim(),
          zh: zhEl ? (zhEl.textContent || "").trim() : "",
          enEl,
          zhEl,
        });
      } else {
        pairs.push({ en: "", zh: (node.textContent || "").trim(), enEl: null, zhEl: node });
        i += 1;
      }
    }
    return pairs.filter((p) => p.en || p.zh);
  }

  function clearReadingLineHighlight() {
    els.pageEditor?.querySelectorAll(".reading-active").forEach((n) => {
      n.classList.remove("reading-active");
    });
    getKnowledgeBodyEl()?.querySelectorAll(".reading-active").forEach((n) => {
      n.classList.remove("reading-active");
    });
  }

  function getTtsScrollRoot() {
    if (mode === "reading" && els.pageEditor && !els.pageEditor.classList.contains("hidden")) {
      return els.pageEditor;
    }
    const body = getKnowledgeBodyEl();
    if (body) return body.closest(".study-hub-rich") || body;
    return els.contentPane || els.content;
  }

  function scrollSentenceIntoCenter(el) {
    if (!el?.isConnected) return;
    const container = getTtsScrollRoot();
    const behavior = activePlayback === "read" ? "auto" : "smooth";
    if (!container) {
      el.scrollIntoView({ behavior, block: "center", inline: "nearest" });
      return;
    }
    const elRect = el.getBoundingClientRect();
    const boxRect = container.getBoundingClientRect();
    const elCenter = elRect.top + elRect.height / 2;
    const boxCenter = boxRect.top + boxRect.height / 2;
    container.scrollBy({ top: elCenter - boxCenter, behavior });
  }

  function ttsSanitize(text) {
    let out = String(text || "").normalize("NFC");
    out = out.replace(/\uFE0F/g, "");
    out = out.replace(EMOJI_SYMBOL_RE, "");
    out = out.replace(TTS_DECORATIVE_SYMBOL_RE, "");
    out = out.replace(TTS_BLANK_MARK_RE, " ");
    out = out.replace(TTS_BOX_DRAWING_RE, " ");
    out = out
      .replace(/\s*\/\s*/g, " ")
      .replace(/\//g, "")
      .replace(/[\u{1F300}-\u{1F9FF}]/gu, "")
      .replace(/[\u2600-\u27BF]/g, "")
      .replace(/\s+([，。！？；：、])/g, "$1")
      .replace(/([（(])\s+/g, "$1")
      .replace(/\s+([）)])/g, "$1")
      .replace(/\s+/g, " ")
      .trim();
    return out;
  }

  function prepareTtsText(text) {
    return ttsSanitize(text);
  }

  function hasReadableTtsText(text) {
    const clean = ttsSanitize(text);
    return !!clean && READABLE_CHAR_RE.test(clean);
  }

  function splitReadableLines(text) {
    return String(text || "")
      .split(/\n+/)
      .map((line) => line.trim())
      .filter((line) => hasReadableTtsText(line));
  }

  function isKnowledgeTtsSkipped(el) {
    if (!el?.closest) return false;
    return !!el.closest(KNOWLEDGE_TTS_SKIP_SEL) || !!el.closest?.("script, style") || el.matches?.("hr");
  }

  function hasInnerKnowledgeBlock(el) {
    return !!el.querySelector?.("p, li, h1, h2, h3, h4, blockquote, pre, table");
  }

  function resolveElementLang(el, text) {
    if (el.classList?.contains("zh")) return "zh";
    if (el.classList?.contains("en")) return "en";
    return classifyLineText(text, "");
  }

  function pushKnowledgeBlock(blocks, text, lang, el) {
    const clean = ttsSanitize(text);
    if (!clean || !READABLE_CHAR_RE.test(clean)) return;
    blocks.push({ text: clean, lang, el });
  }

  function walkKnowledgeForTts(node, blocks) {
    if (!node || node.nodeType !== Node.ELEMENT_NODE) return;
    if (isKnowledgeTtsSkipped(node)) return;

    const tag = node.tagName;

    if (tag === "PRE") {
      splitReadableLines(node.textContent).forEach((line) => {
        pushKnowledgeBlock(blocks, line, resolveElementLang(node, line), node);
      });
      return;
    }

    if (tag === "TABLE") {
      node.querySelectorAll("td, th").forEach((cell) => {
        if (isKnowledgeTtsSkipped(cell)) return;
        const text = (cell.textContent || "").trim();
        if (!text) return;
        pushKnowledgeBlock(blocks, text, resolveElementLang(cell, text), cell);
      });
      return;
    }

    if (KNOWLEDGE_TTS_BLOCK_TAGS.has(tag)) {
      if (hasInnerKnowledgeBlock(node) && tag !== "BLOCKQUOTE") {
        Array.from(node.children).forEach((child) => walkKnowledgeForTts(child, blocks));
        return;
      }
      const text = (node.textContent || "").trim();
      pushKnowledgeBlock(blocks, text, resolveElementLang(node, text), node);
      return;
    }

    Array.from(node.children).forEach((child) => walkKnowledgeForTts(child, blocks));
  }

  function findKangkangVoice(voices) {
    return (voices || []).find((v) => /kangkang|康康/i.test(v.name || ""));
  }

  function voiceLangKind(voice) {
    const lang = (voice?.lang || "").toLowerCase();
    if (lang.startsWith("zh")) return "zh";
    if (lang.startsWith("en")) return "en";
    return "other";
  }

  function findVoiceByPatterns(voices, patterns) {
    for (const pattern of patterns) {
      const re = pattern instanceof RegExp ? pattern : new RegExp(pattern, "i");
      const hit = (voices || []).find((v) => re.test(v.name || ""));
      if (hit) return hit;
    }
    return null;
  }

  const DEFAULT_ZH_VOICE_PATTERNS = [/xiaoxiao.*online/i, /xiaoxiao/i, /晓晓/];
  const DEFAULT_EN_VOICE_PATTERNS = [/ava.*online/i, /\bava\b/i];

  function buildVoiceOptionList(voices, langKind) {
    const list = (voices || []).filter((v) => voiceLangKind(v) === langKind);
    const preferred =
      langKind === "zh"
        ? findVoiceByPatterns(list, DEFAULT_ZH_VOICE_PATTERNS)
        : findVoiceByPatterns(list, DEFAULT_EN_VOICE_PATTERNS);
    const used = new Set();
    const ordered = [];
    if (preferred) {
      ordered.push(preferred);
      used.add(preferred.voiceURI);
    }
    list
      .filter((v) => /online|natural/i.test(v.name || ""))
      .forEach((v) => {
        if (!used.has(v.voiceURI)) {
          ordered.push(v);
          used.add(v.voiceURI);
        }
      });
    list.forEach((v) => {
      if (!used.has(v.voiceURI)) {
        ordered.push(v);
        used.add(v.voiceURI);
      }
    });
    return ordered;
  }

  function fillVoiceSelect(selectEl, voices, langKind, savedUri) {
    if (!selectEl) return "";
    const list = buildVoiceOptionList(voices, langKind);
    if (!list.length) {
      selectEl.innerHTML = '<option value="">（无可用声色）</option>';
      return "";
    }
    selectEl.innerHTML = list
      .map((v) => {
        const label = `${v.name} (${v.lang || "?"})`;
        const safeUri = String(v.voiceURI || "").replace(/"/g, "&quot;");
        return `<option value="${safeUri}">${escapeHtml(label)}</option>`;
      })
      .join("");
    const saved = savedUri && list.some((v) => v.voiceURI === savedUri) ? savedUri : "";
    if (saved) {
      selectEl.value = saved;
      return saved;
    }
    const fallback =
      langKind === "zh"
        ? findVoiceByPatterns(list, DEFAULT_ZH_VOICE_PATTERNS) ||
          findKangkangVoice(list) ||
          list.find((v) => voiceLangKind(v) === "zh") ||
          list[0]
        : findVoiceByPatterns(list, DEFAULT_EN_VOICE_PATTERNS) ||
          list.find((v) => /english|zira|david|mark|samantha/i.test(v.name || "")) ||
          list[0];
    if (fallback) {
      selectEl.value = fallback.voiceURI;
      return fallback.voiceURI;
    }
    return "";
  }

  function applyLegacyVoiceUri(voices) {
    if (!ttsVoiceUriLegacy) return;
    const legacy = voices.find((v) => v.voiceURI === ttsVoiceUriLegacy);
    if (!legacy) {
      ttsVoiceUriLegacy = "";
      return;
    }
    const kind = voiceLangKind(legacy);
    if (kind === "zh" && !ttsVoiceUriZh) ttsVoiceUriZh = legacy.voiceURI;
    if (kind === "en" && !ttsVoiceUriEn) ttsVoiceUriEn = legacy.voiceURI;
    ttsVoiceUriLegacy = "";
  }

  function populateVoiceSelects(voices) {
    const list = voices || [];
    allVoices = list;
    applyLegacyVoiceUri(list);
    ttsVoiceUriZh = fillVoiceSelect(els.ttsVoiceZh, list, "zh", ttsVoiceUriZh);
    ttsVoiceUriEn = fillVoiceSelect(els.ttsVoiceEn, list, "en", ttsVoiceUriEn);
  }

  function resolveTtsVoiceForLang(lang) {
    const voices = allVoices.length ? allVoices : window.speechSynthesis?.getVoices() || [];
    const wantZh = lang === "zh";
    const savedUri = wantZh ? ttsVoiceUriZh : ttsVoiceUriEn;
    if (savedUri) {
      const picked = voices.find((v) => v.voiceURI === savedUri);
      if (picked) return picked;
    }
    if (wantZh) {
      return (
        findVoiceByPatterns(voices, DEFAULT_ZH_VOICE_PATTERNS) ||
        findKangkangVoice(voices) ||
        voices.find((v) => voiceLangKind(v) === "zh") ||
        voices[0] ||
        null
      );
    }
    return (
      findVoiceByPatterns(voices, DEFAULT_EN_VOICE_PATTERNS) ||
      voices.find((v) => voiceLangKind(v) === "en") ||
      voices.find((v) => /english|david|zira|mark|samantha/i.test(v.name || "")) ||
      voices[0] ||
      null
    );
  }

  async function ensureVoices() {
    if (!window.speechSynthesis) return;
    const load = () => {
      const voices = window.speechSynthesis.getVoices();
      if (!voices.length) return false;
      populateVoiceSelects(voices);
      voiceCache.ready = true;
      return true;
    };
    if (load()) return;
    await new Promise((resolve) => {
      const done = () => {
        load();
        resolve();
      };
      window.speechSynthesis.onvoiceschanged = done;
      window.setTimeout(done, 800);
    });
  }

  function startTtsKeepAlive() {
    stopTtsKeepAlive();
    if (!window.speechSynthesis) return;
    // Chrome / Edge：长时间朗读时合成引擎可能自动挂起，需周期性唤醒。
    ttsKeepAliveTimer = window.setInterval(() => {
      if (!window.speechSynthesis.speaking || ttsAbort || activePlayback !== "read") {
        stopTtsKeepAlive();
        return;
      }
      window.speechSynthesis.pause();
      window.speechSynthesis.resume();
    }, 10000);
  }

  function stopTtsKeepAlive() {
    if (ttsKeepAliveTimer) {
      window.clearInterval(ttsKeepAliveTimer);
      ttsKeepAliveTimer = null;
    }
  }

  function buildTtsUtterance(block, voiceEn, voiceZh) {
    const clean = ttsSanitize(block.text);
    if (!clean) return null;
    const utter = new SpeechSynthesisUtterance(clean);
    utter.lang = block.lang === "zh" ? "zh-CN" : "en-US";
    utter.rate = ttsRate;
    utter.pitch = 1;
    utter.volume = 1;
    const voice = block.lang === "zh" ? voiceZh : voiceEn;
    if (voice) utter.voice = voice;
    return utter;
  }

  function resolveTtsBlockElement(block) {
    if (block?.el?.isConnected) return block.el;
    const fresh = getTtsBlocks();
    const targetText = ttsSanitize(block?.text);
    if (!targetText) return null;
    const match = fresh.find(
      (b) => b.lang === block.lang && ttsSanitize(b.text) === targetText,
    );
    return match?.el?.isConnected ? match.el : null;
  }

  function applyTtsHighlight(el, idx) {
    clearReadingLineHighlight();
    if (!el?.isConnected) return null;
    el.classList.add("reading-active");
    readHighlightIndex = idx;
    window.requestAnimationFrame(() => scrollSentenceIntoCenter(el));
    return el;
  }

  function startTtsQueue(blocks) {
    if (!window.speechSynthesis || !blocks.length) return;
    const session = ++ttsSpeakGen;
    const queue = blocks
      .map((block) => ({ block, text: ttsSanitize(block.text) }))
      .filter((item) => item.text);
    if (!queue.length) {
      showToast("当前页没有可朗读的文本", true);
      return;
    }

    const voiceEn = resolveTtsVoiceForLang("en");
    const voiceZh = resolveTtsVoiceForLang("zh");
    let activeEl = null;
    let finished = false;

    const finishQueue = () => {
      if (finished || session !== ttsSpeakGen || ttsAbort) return;
      finished = true;
      if (activeEl?.isConnected) activeEl.classList.remove("reading-active");
      activeEl = null;
      stopTtsKeepAlive();
      stopAllReading();
      showToast("朗读完成", false);
    };

    const playAt = (idx) => {
      if (session !== ttsSpeakGen || ttsAbort || activePlayback !== "read") return;
      if (idx >= queue.length) {
        finishQueue();
        return;
      }

      const item = queue[idx];
      const utter = buildTtsUtterance(item.block, voiceEn, voiceZh);
      if (!utter) {
        playAt(idx + 1);
        return;
      }

      const el = resolveTtsBlockElement(item.block);
      if (activeEl?.isConnected) activeEl.classList.remove("reading-active");
      activeEl = applyTtsHighlight(el, idx);

      let highlighted = !!activeEl;
      utter.onstart = () => {
        if (session !== ttsSpeakGen || ttsAbort || activePlayback !== "read") return;
        const liveEl = resolveTtsBlockElement(item.block);
        if (liveEl && liveEl !== activeEl) {
          if (activeEl?.isConnected) activeEl.classList.remove("reading-active");
          activeEl = applyTtsHighlight(liveEl, idx);
        }
        highlighted = true;
      };
      utter.onend = () => {
        if (session !== ttsSpeakGen || ttsAbort) return;
        playAt(idx + 1);
      };
      utter.onerror = (event) => {
        if (session !== ttsSpeakGen || ttsAbort) return;
        if (event?.error === "canceled" || event?.error === "interrupted") return;
        playAt(idx + 1);
      };

      window.speechSynthesis.speak(utter);

      // 部分浏览器 onstart 触发偏晚，补一次高亮确保跟读可见。
      window.setTimeout(() => {
        if (session !== ttsSpeakGen || ttsAbort || activePlayback !== "read" || highlighted) return;
        const liveEl = resolveTtsBlockElement(item.block);
        if (liveEl) {
          if (activeEl?.isConnected) activeEl.classList.remove("reading-active");
          activeEl = applyTtsHighlight(liveEl, idx);
          highlighted = true;
        }
      }, 80);
    };

    startTtsKeepAlive();
    playAt(0);
  }

  function getKnowledgeReadBlocks() {
    const body = getKnowledgeBodyEl();
    if (!body) return [];
    const blocks = [];
    walkKnowledgeForTts(body, blocks);
    return blocks;
  }

  function getTtsBlocks() {
    if (mode === "reading") {
      return getEditorSentencePairs().flatMap((pair) => {
        const items = [];
        const enText = prepareTtsText(
          pair.enEl ? (pair.enEl.textContent || "").trim() : (pair.en || "").trim(),
        );
        const zhText = prepareTtsText(
          pair.zhEl ? (pair.zhEl.textContent || "").trim() : (pair.zh || "").trim(),
        );
        if (enText) {
          items.push({ text: enText, lang: "en", el: pair.enEl || null });
        }
        if (zhText && readingShowZh) {
          items.push({ text: zhText, lang: "zh", el: pair.zhEl || null });
        }
        return items;
      });
    }
    return getKnowledgeReadBlocks().filter(
      (block) => block.text && (readingShowZh || block.lang !== "zh"),
    );
  }

  function getKnowledgeBodyEl() {
    return els.content?.querySelector(".knowledge-body") || els.content;
  }

  function getRichEditorRoot() {
    if (mode === "reading" && els.pageEditor && !els.pageEditor.classList.contains("hidden")) {
      return els.pageEditor;
    }
    return getKnowledgeBodyEl();
  }

  function insertHtmlAtCursor(html) {
    const root = getRichEditorRoot();
    if (!root) return;
    root.focus();
    if (document.queryCommandSupported("insertHTML")) {
      document.execCommand("insertHTML", false, html);
      return;
    }
    const sel = window.getSelection();
    if (sel && sel.rangeCount) {
      const range = sel.getRangeAt(0);
      range.deleteContents();
      const frag = range.createContextualFragment(html);
      range.insertNode(frag);
    } else {
      root.insertAdjacentHTML("beforeend", html);
    }
  }

  async function uploadMediaFile(file) {
    const buf = await file.arrayBuffer();
    const bytes = new Uint8Array(buf);
    let binary = "";
    bytes.forEach((b) => {
      binary += String.fromCharCode(b);
    });
    const data = btoa(binary);
    const res = await fetch("/api/study-hub/upload-media", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename: file.name, data }),
    });
    const payload = await res.json();
    if (!res.ok) throw new Error(payload.error || "上传失败");
    return payload.url;
  }

  async function insertKnowledgeImage(file) {
    const url = await uploadMediaFile(file);
    insertHtmlAtCursor(
      `<figure class="media-embed"><img src="${url}" alt="${escapeHtml(file.name)}" /><figcaption>${escapeHtml(file.name)}</figcaption></figure>`,
    );
    showToast("图片已插入", false);
  }

  async function insertKnowledgeAudio(file) {
    const url = await uploadMediaFile(file);
    insertHtmlAtCursor(`<figure class="media-embed"><audio controls src="${url}"></audio></figure>`);
    showToast("音频已插入", false);
  }

  function insertKnowledgeTable() {
    const rows = Number(window.prompt("表格行数", "3")) || 3;
    const cols = Number(window.prompt("表格列数", "3")) || 3;
    let html = '<table class="rich-table"><thead><tr>';
    for (let c = 0; c < cols; c += 1) html += `<th>列 ${c + 1}</th>`;
    html += "</tr></thead><tbody>";
    for (let r = 0; r < rows; r += 1) {
      html += "<tr>";
      for (let c = 0; c < cols; c += 1) html += "<td>&nbsp;</td>";
      html += "</tr>";
    }
    html += "</tbody></table>";
    insertHtmlAtCursor(html);
  }

  function insertKnowledgeLink() {
    const url = window.prompt("链接地址 (https://...)", "https://");
    if (!url) return;
    const text = window.prompt("链接文字", url) || url;
    insertHtmlAtCursor(`<p><a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(text)}</a></p>`);
  }

  function insertKnowledgeVideo() {
    const url = window.prompt("视频或嵌入链接（支持 B站/YouTube/直链）", "");
    if (!url) return;
    const embed = toEmbedUrl(url.trim());
    if (embed.includes("youtube.com/embed") || embed.includes("bilibili.com/player")) {
      insertHtmlAtCursor(`<figure class="media-embed"><iframe src="${escapeHtml(embed)}" allowfullscreen loading="lazy"></iframe></figure>`);
    } else {
      insertHtmlAtCursor(`<figure class="media-embed"><video controls src="${escapeHtml(url.trim())}"></video></figure>`);
    }
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function highlightTextSimple(text) {
    if (!text || !glossaryTerms.length) return escapeHtml(text);
    const spans = [];
    glossaryTerms.forEach((entry) => {
      const term = typeof entry === "string" ? entry : entry.word;
      findGlossaryTermSpans(text, term).forEach((span) => {
        spans.push({ ...span, entry: typeof entry === "string" ? { word: term, page: "", gloss: "" } : entry });
      });
    });
    if (!spans.length) return escapeHtml(text);
    spans.sort((a, b) => a.start - b.start || b.end - a.end);
    const merged = [];
    spans.forEach((span) => {
      const last = merged[merged.length - 1];
      if (!last || span.start >= last.end) merged.push({ ...span });
      else if (span.end - span.start > last.end - last.start) merged[merged.length - 1] = { ...span };
    });
    let html = "";
    let cursor = 0;
    merged.forEach((span) => {
      html += escapeHtml(text.slice(cursor, span.start));
      const chunk = text.slice(span.start, span.end);
      const title = span.entry.page
        ? `附录2 P.${span.entry.page}${span.entry.gloss ? ` · ${span.entry.gloss}` : ""}`
        : "附录2 词汇";
      html += `<mark class="glossary-hit" title="${escapeHtml(title)}">${escapeHtml(chunk)}</mark>`;
      cursor = span.end;
    });
    html += escapeHtml(text.slice(cursor));
    return html;
  }

  function applyGlossaryHighlights(root) {
    if (!root) return;
    refreshGlossaryTermsForCurrentPage();
    if (!glossaryTerms.length) return;
    root.querySelectorAll(GLOSSARY_HIGHLIGHT_SEL).forEach((el) => {
      if (el.closest("table.rich-table thead")) return;
      const text = (el.textContent || "").trim();
      if (!text) return;
      el.innerHTML = highlightTextSimple(text);
    });
  }

  function refreshHighlightsOnPageChange() {
    if (mode === "reading" && els.pageEditor && !els.pageEditor.classList.contains("hidden")) {
      applyGlossaryHighlights(els.pageEditor);
    } else if (mode === "knowledge") {
      const body = getKnowledgeBodyEl();
    if (body) applyGlossaryHighlights(body);
    applyReadingLangDisplay();
  }
    const png = activePdfPages[imagePageIndex];
    if (els.pageLabel && png) {
      els.pageLabel.classList.remove("hidden");
      els.pageLabel.textContent = `Page ${printedPageForPng(png)}`;
    }
  }

  function ttsLine(row) {
    const raw = row.tts || row.en || "";
    return ttsSanitize(raw);
  }

  function renderMathIn(container) {
    if (typeof window.katex === "undefined") return;
    container.querySelectorAll(".math-inline[data-tex]").forEach((node) => {
      try {
        window.katex.render(node.getAttribute("data-tex") || "", node, { throwOnError: false, displayMode: false });
      } catch { /* ignore */ }
    });
    container.querySelectorAll(".math-block[data-tex]").forEach((node) => {
      try {
        window.katex.render(node.getAttribute("data-tex") || "", node, { throwOnError: false, displayMode: true });
      } catch { /* ignore */ }
    });
  }

  function applyImageTransform() {
    if (!els.imageTransform) return;
    els.imageTransform.style.transformOrigin = "center center";
    els.imageTransform.style.transform = `translate(${imgPanX}px, ${imgPanY}px) scale(${imgScale})`;
    if (els.imageViewport) {
      els.imageViewport.classList.toggle("is-panning", imgScale > 1);
    }
  }

  function resetImageTransform() {
    imgScale = 1;
    imgPanX = 0;
    imgPanY = 0;
    applyImageTransform();
    fitImageInViewport();
  }

  function zoomImage(delta) {
    imgScale = Math.max(1, Math.min(4, imgScale + delta));
    if (imgScale === 1) {
      imgPanX = 0;
      imgPanY = 0;
    }
    applyImageTransform();
  }

  function bindImagePanZoom() {
    if (!els.imageViewport || !els.image) return;
    els.imageViewport.addEventListener("mousedown", (e) => {
      if (imgScale <= 1) return;
      imgDragging = true;
      imgDragStart = { x: e.clientX, y: e.clientY, panX: imgPanX, panY: imgPanY };
      els.imageViewport.classList.add("dragging");
    });
    window.addEventListener("mousemove", (e) => {
      if (!imgDragging) return;
      imgPanX = imgDragStart.panX + (e.clientX - imgDragStart.x);
      imgPanY = imgDragStart.panY + (e.clientY - imgDragStart.y);
      applyImageTransform();
    });
    window.addEventListener("mouseup", () => {
      imgDragging = false;
      if (els.imageViewport) els.imageViewport.classList.remove("dragging");
    });
    els.imageViewport.addEventListener(
      "wheel",
      (e) => {
        e.preventDefault();
        zoomImage(e.deltaY < 0 ? 0.12 : -0.12);
      },
      { passive: false },
    );
    els.imageViewport.addEventListener("touchstart", (e) => {
      if (imgScale <= 1 || e.touches.length !== 1) return;
      imgDragging = true;
      imgDragStart = {
        x: e.touches[0].clientX,
        y: e.touches[0].clientY,
        panX: imgPanX,
        panY: imgPanY,
      };
    }, { passive: true });
    els.imageViewport.addEventListener("touchmove", (e) => {
      if (!imgDragging || e.touches.length !== 1) return;
      imgPanX = imgDragStart.panX + (e.touches[0].clientX - imgDragStart.x);
      imgPanY = imgDragStart.panY + (e.touches[0].clientY - imgDragStart.y);
      applyImageTransform();
    }, { passive: true });
    els.imageViewport.addEventListener("touchend", () => {
      imgDragging = false;
    });
  }

  function getOfficialAudioTrack(pageId) {
    if (!audioBank?.tracks?.length || !pageId) return null;
    return audioBank.tracks.find((t) => t.pageId === pageId) || null;
  }

  function audioSrcUrl(src) {
    if (!src) return "";
    const base = src.split("?")[0];
    const bust = hubCacheBust ? `?v=${hubCacheBust}` : "";
    return encodeURI(base) + bust;
  }

  function stopStudentRecordingCleanup() {
    try {
      recordProcessor?.disconnect();
    } catch {
      /* ignore */
    }
    try {
      recordSource?.disconnect();
    } catch {
      /* ignore */
    }
    recordProcessor = null;
    recordSource = null;
    if (recordStream) {
      recordStream.getTracks().forEach((t) => t.stop());
      recordStream = null;
    }
    if (recordAudioCtx) {
      recordAudioCtx.close().catch(() => {});
      recordAudioCtx = null;
    }
    recordPcmChunks = [];
  }

  function stopStudentRecording() {
    studentRecordingActive = false;
    stopStudentRecordingCleanup();
    updateStudentRecordToolbar();
  }

  function openStudentRecordDb() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(STUDENT_RECORD_DB, 1);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(STUDENT_RECORD_STORE)) {
          db.createObjectStore(STUDENT_RECORD_STORE, { keyPath: "id" });
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  async function listStudentRecordings(pageId) {
    try {
      const db = await openStudentRecordDb();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STUDENT_RECORD_STORE, "readonly");
        const store = tx.objectStore(STUDENT_RECORD_STORE);
        const req = store.getAll();
        req.onsuccess = () => {
          const all = (req.result || []).filter((r) => r.pageId === pageId);
          all.sort((a, b) => b.createdAt - a.createdAt);
          resolve(all);
        };
        req.onerror = () => reject(req.error);
      });
    } catch {
      return [];
    }
  }

  function getLameMp3Encoder() {
    if (window.lamejs?.Mp3Encoder) return window.lamejs.Mp3Encoder;
    if (typeof window.Mp3Encoder === "function") return window.Mp3Encoder;
    return null;
  }

  function encodePcmToMp3(floatChunks, sampleRate) {
    const Mp3Encoder = getLameMp3Encoder();
    if (!Mp3Encoder) throw new Error("lamejs not loaded");
    const total = floatChunks.reduce((n, c) => n + c.length, 0);
    if (total < sampleRate * 0.25) throw new Error("recording too short");
    const merged = new Float32Array(total);
    let pos = 0;
    floatChunks.forEach((chunk) => {
      merged.set(chunk, pos);
      pos += chunk.length;
    });
    const int16 = new Int16Array(merged.length);
    for (let i = 0; i < merged.length; i++) {
      const s = Math.max(-1, Math.min(1, merged[i]));
      int16[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
    }
    const encoder = new Mp3Encoder(1, sampleRate, 128);
    const block = 1152;
    const parts = [];
    for (let i = 0; i < int16.length; i += block) {
      const mp3buf = encoder.encodeBuffer(int16.subarray(i, i + block));
      if (mp3buf?.length) parts.push(new Uint8Array(mp3buf));
    }
    const tail = encoder.flush();
    if (tail?.length) parts.push(new Uint8Array(tail));
    return new Blob(parts, { type: "audio/mpeg" });
  }

  function mimeToFileExt(mime) {
    if (!mime) return "mp3";
    if (mime.includes("mpeg") || mime.includes("mp3")) return "mp3";
    if (mime.includes("mp4")) return "m4a";
    if (mime.includes("ogg")) return "ogg";
    return "webm";
  }

  function buildStudentRecordFilename(page) {
    const unit = currentUnit || 0;
    const part = (page?.part || page?.label || "page").replace(/\s+/g, "-");
    const d = new Date();
    const date = [
      d.getFullYear(),
      String(d.getMonth() + 1).padStart(2, "0"),
      String(d.getDate()).padStart(2, "0"),
    ].join("-");
    const time = [
      String(d.getHours()).padStart(2, "0"),
      String(d.getMinutes()).padStart(2, "0"),
      String(d.getSeconds()).padStart(2, "0"),
    ].join("-");
    return `Unit${unit}-${part}_${date}_${time}`;
  }

  async function blobToBase64(blob) {
    const buf = await blob.arrayBuffer();
    const bytes = new Uint8Array(buf);
    let binary = "";
    const step = 0x8000;
    for (let i = 0; i < bytes.length; i += step) {
      binary += String.fromCharCode(...bytes.subarray(i, i + step));
    }
    return btoa(binary);
  }

  async function uploadStudentAudioBlob(blob, filename) {
    const data = await blobToBase64(blob);
    const res = await fetch("/api/study-hub/save-student-audio", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ filename, data }),
    });
    const payload = await res.json();
    if (!res.ok) throw new Error(payload.error || "保存到单元音频目录失败");
    return payload.path || payload.url?.replace(/^\//, "") || "";
  }

  function downloadBlobFile(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 60000);
  }

  function releaseRecordUrl(id) {
    const url = recordUrlCache.get(id);
    if (url) {
      URL.revokeObjectURL(url);
      recordUrlCache.delete(id);
    }
  }

  function resolveRecordPlaybackUrl(row) {
    if (row.fileUrl) {
      const path = row.fileUrl.startsWith("/") ? row.fileUrl : `/${row.fileUrl}`;
      return `${encodeURI(path)}?t=${row.createdAt || Date.now()}`;
    }
    if (row.blob && !recordUrlCache.has(row.id)) {
      const url = URL.createObjectURL(new Blob([row.blob], { type: row.mimeType || "audio/mpeg" }));
      recordUrlCache.set(row.id, url);
    }
    return recordUrlCache.get(row.id) || "";
  }

  function updateStudentRecordToolbar() {
    if (!els.studentRecordBtn) return;
    if (studentRecordingActive) {
      els.studentRecordBtn.textContent = "停止录音";
      els.studentRecordBtn.classList.add("recording");
      els.studentRecordBtn.title = "结束录音并保存为音频文件";
    } else {
      els.studentRecordBtn.textContent = "课文录音";
      els.studentRecordBtn.classList.remove("recording");
      els.studentRecordBtn.title = "录制本课课文朗读，停止后自动保存";
    }
  }

  async function saveStudentRecording(pageId, blob, mimeType, filename, fileUrl) {
    const db = await openStudentRecordDb();
    const id = `${pageId}_${Date.now()}`;
    const entry = {
      id,
      pageId,
      unit: currentUnit,
      part: getCurrentPage()?.part || "",
      createdAt: Date.now(),
      label: filename,
      filename,
      fileUrl: fileUrl || "",
      mimeType: mimeType || "audio/mpeg",
      blob,
    };
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STUDENT_RECORD_STORE, "readwrite");
      tx.objectStore(STUDENT_RECORD_STORE).put(entry);
      tx.oncomplete = () => resolve(entry);
      tx.onerror = () => reject(tx.error);
    });
  }

  async function deleteStudentRecording(id) {
    const db = await openStudentRecordDb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STUDENT_RECORD_STORE, "readwrite");
      tx.objectStore(STUDENT_RECORD_STORE).delete(id);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }

  async function refreshStudentRecordPanel(pageId) {
    const panel = els.studentRecordPanel;
    if (!panel) return;
    const rows = await listStudentRecordings(pageId);
    const keepIds = new Set(rows.map((r) => r.id));
    recordUrlCache.forEach((url, id) => {
      if (!keepIds.has(id)) releaseRecordUrl(id);
    });
    if (!rows.length) {
      panel.classList.add("hidden");
      panel.innerHTML = "";
      return;
    }
    panel.classList.remove("hidden");
    panel.innerHTML = `
      <p class="study-hub-student-record-title">本课朗读录音（${rows.length} 条）· MP3 已保存至 assets/audios/student/</p>
      <ul class="study-hub-record-list">
        ${rows
          .map((row) => {
            const url = resolveRecordPlaybackUrl(row);
            const name = row.filename || row.label || "录音";
            return `<li class="study-hub-record-item" data-id="${escapeHtml(row.id)}">
              <span class="study-hub-record-filename" title="${escapeHtml(name)}">${escapeHtml(name)}</span>
              <audio controls preload="metadata" playsinline src="${escapeHtml(url)}"></audio>
              <button type="button" class="study-hub-record-download" data-id="${escapeHtml(row.id)}" title="下载">下载</button>
              <button type="button" class="study-hub-record-del" data-id="${escapeHtml(row.id)}">删除</button>
            </li>`;
          })
          .join("")}
      </ul>
    `;
    panel.querySelectorAll(".study-hub-record-del").forEach((btn) => {
      btn.addEventListener("click", async () => {
        releaseRecordUrl(btn.dataset.id);
        await deleteStudentRecording(btn.dataset.id);
        await refreshStudentRecordPanel(pageId);
        showToast("已删除录音", false);
      });
    });
    panel.querySelectorAll(".study-hub-record-download").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const rowsNow = await listStudentRecordings(pageId);
        const row = rowsNow.find((r) => r.id === btn.dataset.id);
        if (!row?.blob) return;
        downloadBlobFile(row.blob, row.filename || "recording.mp3");
      });
    });
  }

  function getSnipPageMeta(page) {
    const p = page || getCurrentPage();
    const part = (p?.part || "").trim() || "page";
    const partLabel = (p?.label || part).trim();
    const pageId = p?.id || currentPageId || "";
    return { pageId, part, partLabel };
  }

  function buildSnipFilename(category, page) {
    const meta = getSnipPageMeta(page);
    const unit = currentUnit || 0;
    const partSlug = meta.part.replace(/\s+/g, "-");
    const cat = category === "homework" ? "homework" : "task";
    const d = new Date();
    const date = [
      d.getFullYear(),
      String(d.getMonth() + 1).padStart(2, "0"),
      String(d.getDate()).padStart(2, "0"),
    ].join("-");
    const time = [
      String(d.getHours()).padStart(2, "0"),
      String(d.getMinutes()).padStart(2, "0"),
      String(d.getSeconds()).padStart(2, "0"),
    ].join("-");
    return `Unit${unit}-${partSlug}_${cat}_${date}_${time}.png`;
  }

  function resetSnipModalPreview() {
    snipPendingBlob = null;
    if (els.snipPreview) {
      els.snipPreview.classList.add("hidden");
      els.snipPreview.innerHTML = "";
    }
    if (els.snipSave) els.snipSave.disabled = true;
    if (els.snipSave) els.snipSave.textContent = "保存截图";
  }

  function setSnipPendingBlob(blob) {
    if (!blob) {
      showToast("请粘贴或选择图片文件", true);
      return;
    }
    const type = (blob.type || "").toLowerCase();
    if (type && !type.startsWith("image/")) {
      showToast("请粘贴或选择图片文件", true);
      return;
    }
    snipPendingBlob = blob.type ? blob : new Blob([blob], { type: "image/png" });
    if (els.snipPreview) {
      const url = URL.createObjectURL(snipPendingBlob);
      els.snipPreview.innerHTML = `<img src="${url}" alt="截图预览" />`;
      els.snipPreview.classList.remove("hidden");
      window.setTimeout(() => URL.revokeObjectURL(url), 60000);
    }
    if (els.snipSave) {
      els.snipSave.disabled = false;
      els.snipSave.textContent = "保存截图";
    }
    showToast("已识别截图，请点击「保存截图」", false);
  }

  function openSnipModal(category) {
    if (mode !== "knowledge") {
      showToast("请在知识点精讲模式下使用截图存档", true);
      return;
    }
    const cat = category === "homework" ? "homework" : "task";
    const meta = getSnipPageMeta(getCurrentPage());
    if (!meta.pageId) {
      showToast("请先选择本课 Part 后再保存截图", true);
      return;
    }
    countSnipCategory(cat, meta.pageId)
      .then((n) => {
        if (n >= SNIP_GRID_COLS) {
          const label = cat === "task" ? "作业布置" : "作业提交";
          showToast(`本 Part「${label}」已满 ${SNIP_GRID_COLS} 张，请先删除再添加`, true);
          return;
        }
        snipPendingCategory = cat;
        resetSnipModalPreview();
        if (els.snipModalTitle) {
          els.snipModalTitle.textContent =
            snipPendingCategory === "homework" ? "保存作业提交截图" : "保存作业布置截图";
        }
        if (els.snipModal) els.snipModal.classList.remove("hidden");
        window.setTimeout(() => els.snipPasteZone?.focus(), 50);
      })
      .catch(() => {
        snipPendingCategory = cat;
        resetSnipModalPreview();
        if (els.snipModal) els.snipModal.classList.remove("hidden");
      });
  }

  function closeSnipModal() {
    resetSnipModalPreview();
    if (els.snipModal) els.snipModal.classList.add("hidden");
  }

  function openSnipViewer(url, title) {
    if (!url || !els.snipViewer || !els.snipViewerImg) return;
    const src = url.includes("?") ? url : `${url}?t=${Date.now()}`;
    els.snipViewerImg.src = src;
    els.snipViewerImg.alt = title || "截图";
    if (els.snipViewerCaption) {
      const label = title || "";
      els.snipViewerCaption.textContent = label;
      els.snipViewerCaption.classList.toggle("hidden", !label);
    }
    els.snipViewer.classList.remove("hidden");
    document.body.classList.add("study-hub-snip-viewer-open");
  }

  function closeSnipViewer() {
    if (!els.snipViewer) return;
    els.snipViewer.classList.add("hidden");
    if (els.snipViewerImg) els.snipViewerImg.removeAttribute("src");
    document.body.classList.remove("study-hub-snip-viewer-open");
  }

  function handleSnipPasteEvent(e) {
    if (!els.snipModal || els.snipModal.classList.contains("hidden")) return;
    const items = e.clipboardData?.items;
    if (items?.length) {
      for (const item of items) {
        if (item.kind === "file" && (item.type.startsWith("image/") || item.type === "")) {
          e.preventDefault();
          const blob = item.getAsFile();
          if (blob) {
            setSnipPendingBlob(blob);
            return;
          }
        }
      }
    }
    const files = e.clipboardData?.files;
    if (files?.length) {
      for (const file of files) {
        if ((file.type || "").startsWith("image/") || /\.(png|jpe?g|webp|gif|bmp)$/i.test(file.name || "")) {
          e.preventDefault();
          setSnipPendingBlob(file);
          return;
        }
      }
    }
  }

  async function uploadSnipBlob(blob, category) {
    const page = getCurrentPage();
    const meta = getSnipPageMeta(page);
    if (!meta.pageId) {
      throw new Error("请先选择本课 Part 后再保存截图");
    }
    const filename = buildSnipFilename(category, page);
    const data = await blobToBase64(blob);
    const res = await fetch("/api/study-hub/save-snip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        unit: currentUnit || 1,
        category,
        filename,
        data,
        pageId: meta.pageId,
        part: meta.part,
      }),
    });
    const payload = await res.json();
    if (!res.ok) throw new Error(payload.error || "截图保存失败");
    return payload.item || payload;
  }

  function formatSnipTime(ts) {
    if (!ts) return "";
    const d = new Date(Number(ts));
    if (Number.isNaN(d.getTime())) return "";
    const pad = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  const SNIP_GRID_COLS = 4;
  const SNIP_THUMB_PX = 20;
  const SNIP_SLOT_LABELS = ["①", "②", "③", "④"];

  function buildSnipSlots(rows) {
    const ordered = Array.isArray(rows)
      ? [...rows].sort((a, b) => Number(a.createdAt || 0) - Number(b.createdAt || 0)).slice(0, SNIP_GRID_COLS)
      : [];
    const slots = [...ordered];
    while (slots.length < SNIP_GRID_COLS) slots.push(null);
    return slots;
  }

  async function fetchSnipItemsForPage(pageId) {
    const qs = new URLSearchParams({
      unit: String(currentUnit || 1),
      pageId: pageId || "",
    });
    const res = await fetch(`/api/study-hub/list-snips?${qs.toString()}&t=${Date.now()}`);
    const payload = await res.json();
    if (!res.ok) throw new Error(payload.error || "list failed");
    return payload.items || [];
  }

  async function countSnipCategory(category, pageId) {
    const meta = getSnipPageMeta(getCurrentPage());
    const pid = pageId || meta.pageId || currentPageId || "";
    if (!pid) return 0;
    const items = await fetchSnipItemsForPage(pid);
    const cat = category === "homework" ? "homework" : "task";
    return items.filter((r) => r.category === cat).length;
  }

  function renderSnipThumbCell(row, slotIndex) {
    const label = SNIP_SLOT_LABELS[slotIndex] || String((slotIndex || 0) + 1);
    if (!row) {
      return `<article class="study-hub-snip-thumb study-hub-snip-thumb-empty" aria-label="空位 ${label}" title="空位 ${label}">
        <span class="study-hub-snip-thumb-placeholder"></span>
      </article>`;
    }
    const path = row.path || "";
    const url = path.startsWith("/") ? path : `/${path}`;
    const name = row.filename || "截图";
    const when = formatSnipTime(row.createdAt);
    const tip = when ? `${when} · ${name}` : name;
    return `<article class="study-hub-snip-thumb" data-id="${escapeHtml(row.id || "")}" title="${escapeHtml(tip)} · ${label}">
      <button type="button" class="study-hub-snip-thumb-view" data-url="${escapeHtml(url)}" data-title="${escapeHtml(name)}" aria-label="查看 ${label} ${escapeHtml(name)}">
        <img src="${escapeHtml(`${url}?t=${row.createdAt || Date.now()}`)}" alt="${escapeHtml(name)}" loading="lazy" />
      </button>
      <button type="button" class="study-hub-snip-thumb-del" data-id="${escapeHtml(row.id || "")}" aria-label="删除" title="删除">×</button>
    </article>`;
  }

  function renderSnipSection(title, rows) {
    const slots = buildSnipSlots(rows);
    const filled = Math.min(rows.length, SNIP_GRID_COLS);
    return `
      <section class="study-hub-snip-section">
        <h4 class="study-hub-snip-section-title">${escapeHtml(title)} <span class="study-hub-snip-count">${filled}/${SNIP_GRID_COLS}</span></h4>
        <div class="study-hub-snip-grid" style="--snip-cols:${SNIP_GRID_COLS};--snip-size:${SNIP_THUMB_PX}px">
          ${slots.map((row, idx) => renderSnipThumbCell(row, idx)).join("")}
        </div>
      </section>
    `;
  }

  function renderSnipPanelContent(tasks, homework, pageMeta) {
    const label = pageMeta?.partLabel || "本 Part";
    return `
      <p class="study-hub-snip-panel-title">作业截图存档 · Unit ${currentUnit || 1} · ${escapeHtml(label)}</p>
      <p class="study-hub-snip-panel-hint">每个 Part 独立保存：<strong>作业布置</strong> 与 <strong>作业提交</strong> 各 4 格（①–④）。切换 Part 会显示对应记录。</p>
      ${renderSnipSection("作业布置", tasks)}
      ${renderSnipSection("作业提交", homework)}
    `;
  }

  function bindSnipPanelActions(panel, pageId) {
    panel.querySelectorAll(".study-hub-snip-thumb-view").forEach((btn) => {
      btn.addEventListener("click", () => {
        const url = btn.dataset.url;
        const title = btn.dataset.title || "";
        if (url) openSnipViewer(url, title);
      });
    });
    panel.querySelectorAll(".study-hub-snip-thumb-del").forEach((btn) => {
      btn.addEventListener("click", async (e) => {
        e.stopPropagation();
        const id = btn.dataset.id;
        if (!id) return;
        try {
          const res = await fetch("/api/study-hub/delete-snip", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id }),
          });
          const payload = await res.json();
          if (!res.ok) throw new Error(payload.error || "删除失败");
          await refreshSnipPanel(pageId);
          showToast("已删除截图", false);
        } catch (err) {
          showToast(err?.message || "删除失败", true);
        }
      });
    });
  }

  async function refreshSnipPanel(pageId) {
    const panel = els.snipPanel;
    if (!panel) return;
    if (mode !== "knowledge") {
      panel.classList.add("hidden");
      panel.innerHTML = "";
      return;
    }
    const meta = getSnipPageMeta(getCurrentPage());
    const activePageId = pageId || meta.pageId || currentPageId || "";
    let items = [];
    let apiOk = false;
    try {
      const qs = new URLSearchParams({
        unit: String(currentUnit || 1),
        pageId: activePageId,
      });
      const res = await fetch(`/api/study-hub/list-snips?${qs.toString()}&t=${Date.now()}`);
      const payload = await res.json();
      apiOk = res.ok;
      if (res.ok) items = payload.items || [];
    } catch {
      apiOk = false;
      items = [];
    }
    panel.classList.remove("hidden");
    if (!apiOk) {
      panel.innerHTML = `
        <p class="study-hub-snip-panel-title">截图存档</p>
        <p class="study-hub-snip-empty-hint">无法连接本地保存服务。请双击项目根目录的 <strong>启动.bat</strong>，用浏览器打开 <strong>http://localhost:8080</strong> 后再保存截图（不能直接双击 index.html）。</p>
      `;
      return;
    }
    const tasks = items.filter((r) => r.category === "task");
    const homework = items.filter((r) => r.category === "homework");
    panel.innerHTML = renderSnipPanelContent(tasks, homework, meta);
    bindSnipPanelActions(panel, activePageId);
  }

  async function saveSnipFromModal() {
    if (!snipPendingBlob) {
      showToast("请先粘贴或选择截图", true);
      return;
    }
    try {
      const meta = getSnipPageMeta(getCurrentPage());
      const n = await countSnipCategory(snipPendingCategory, meta.pageId);
      if (n >= SNIP_GRID_COLS) {
        const label = snipPendingCategory === "task" ? "作业布置" : "作业提交";
        showToast(`本 Part「${label}」已满 ${SNIP_GRID_COLS} 张`, true);
        return;
      }
      const item = await uploadSnipBlob(snipPendingBlob, snipPendingCategory);
      closeSnipModal();
      await refreshSnipPanel(currentPageId);
      const name = item?.filename || buildSnipFilename(snipPendingCategory, getCurrentPage());
      showToast(`截图已保存：${name}`, false);
      if (els.snipPanel) {
        els.snipPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    } catch (err) {
      const msg = String(err?.message || "");
      showToast(
        msg.includes("Failed to fetch") || msg.includes("NetworkError")
          ? "保存失败：请用 启动.bat 打开 http://localhost:8080，不要直接打开 html 文件"
          : msg || "保存失败；请通过启动.bat 运行本地服务",
        true,
      );
    }
  }

  async function finishStudentRecording(page, pcmChunks, sampleRate) {
    if (!pcmChunks?.length) {
      showToast("录音太短，请重试", true);
      return;
    }
    let blob;
    try {
      blob = encodePcmToMp3(pcmChunks, sampleRate);
    } catch (err) {
      const msg = String(err?.message || "");
      showToast(
        msg.includes("lamejs") ? "MP3 编码库未加载，请刷新页面后重试" : "录音编码失败，请重试",
        true,
      );
      return;
    }
    const filename = `${buildStudentRecordFilename(page)}.mp3`;
    let fileUrl = "";
    try {
      fileUrl = await uploadStudentAudioBlob(blob, filename);
    } catch {
      showToast("已保存到本机；启动本地服务后可同步到 assets/audios/student/", true);
    }
    await saveStudentRecording(page.id, blob, "audio/mpeg", filename, fileUrl);
    downloadBlobFile(blob, filename);
    await refreshStudentRecordPanel(page.id);
    showToast(`课文 MP3 已保存：${filename}`, false);
  }

  async function startStudentRecording() {
    const page = getCurrentPage();
    if (!page?.id || mode !== "reading") {
      showToast("请在课文朗读模式下录音", true);
      return;
    }
    if (studentRecordingActive) return;
    if (!getLameMp3Encoder()) {
      showToast("MP3 编码库未加载，请刷新页面", true);
      return;
    }
    try {
      stopStudentRecording();
      recordPcmChunks = [];
      recordStream = await navigator.mediaDevices.getUserMedia({
        audio: { echoCancellation: true, noiseSuppression: true, channelCount: 1 },
      });
      recordAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
      recordSampleRate = recordAudioCtx.sampleRate;
      recordSource = recordAudioCtx.createMediaStreamSource(recordStream);
      recordProcessor = recordAudioCtx.createScriptProcessor(4096, 1, 1);
      recordProcessor.onaudioprocess = (e) => {
        if (!studentRecordingActive) return;
        recordPcmChunks.push(new Float32Array(e.inputBuffer.getChannelData(0)));
      };
      recordSource.connect(recordProcessor);
      recordProcessor.connect(recordAudioCtx.destination);
      recordStartMs = Date.now();
      studentRecordingActive = true;
      updateStudentRecordToolbar();
      showToast("正在录音，请朗读课文…", false);
    } catch {
      stopStudentRecordingCleanup();
      studentRecordingActive = false;
      updateStudentRecordToolbar();
      showToast("无法使用麦克风，请检查浏览器权限", true);
    }
  }

  async function stopStudentRecordingAndSave() {
    if (!studentRecordingActive) return;
    const page = getCurrentPage();
    if (!page?.id) return;
    studentRecordingActive = false;
    updateStudentRecordToolbar();
    const pcmChunks = recordPcmChunks.slice();
    const sampleRate = recordSampleRate;
    stopStudentRecordingCleanup();
    await finishStudentRecording(page, pcmChunks, sampleRate);
  }

  async function toggleStudentRecording() {
    if (studentRecordingActive) {
      stopStudentRecordingAndSave();
    } else {
      await startStudentRecording();
    }
  }

  async function renderStudyHubAudioBar(pageId) {
    if (!els.audioBar) return;
    const track = getOfficialAudioTrack(pageId);
    if (!track || mode !== "reading") {
      els.audioBar.classList.add("hidden");
      els.audioBar.innerHTML = "";
      officialAudioEl = null;
      audioBarRenderedPageId = null;
      return;
    }

    if (audioBarRenderedPageId === pageId && els.audioBar.querySelector("#studyHubOfficialAudio")) {
      els.audioBar.classList.remove("hidden");
      return;
    }

    audioBarRenderedPageId = pageId;
    els.audioBar.classList.remove("hidden");
    const src = audioSrcUrl(track.src);
    els.audioBar.innerHTML = `
      <p class="study-hub-audio-bar-title">🎧 ${escapeHtml(track.title || track.label || "补充听力")}</p>
      <p class="study-hub-audio-bar-hint">课堂补充听力材料，可使用下方播放器完整收听</p>
      <audio id="studyHubOfficialAudio" controls preload="metadata" src="${escapeHtml(src)}"></audio>
    `;
    officialAudioEl = els.audioBar.querySelector("#studyHubOfficialAudio");
  }

  function stopAllReading() {
    ttsAbort = true;
    activePlayback = null;
    ttsSpeakGen += 1;
    stopTtsKeepAlive();
    if (window.speechSynthesis) window.speechSynthesis.cancel();
    if (readHighlightTimer) {
      clearTimeout(readHighlightTimer);
      readHighlightTimer = null;
    }
    readHighlightIndex = -1;
    clearReadingLineHighlight();
    if (els.readModeBtn) {
      els.readModeBtn.classList.remove("active");
      els.readModeBtn.textContent = "朗读";
    }
  }

  function clearReadingHighlight() {
    readHighlightIndex = -1;
    els.content?.querySelectorAll(".sentence-pair.reading-active").forEach((n) => {
      n.classList.remove("reading-active");
    });
  }

  function startReadingMode() {
    // 仅本按钮启动：逐句向下朗读（不自动翻页、不自动进入下一 Part）。
    if (activePlayback === "read") {
      stopAllReading();
      return;
    }
    stopAllReading();
    if (!getTtsBlocks().length) {
      showToast("当前页没有可朗读的文本", true);
      return;
    }
    activePlayback = "read";
    ttsAbort = false;
    if (els.readModeBtn) els.readModeBtn.classList.add("active");
    ensureVoices().then(() => {
      if (activePlayback !== "read" || ttsAbort) return;
      const blocks = getTtsBlocks();
      if (!blocks.length) {
        stopAllReading();
        showToast("当前页没有可朗读的文本", true);
        return;
      }
      startTtsQueue(blocks);
    });
  }

  function patchCustomKnowledgePage(patch) {
    const custom = loadCustomKnowledge() || { version: 2, title: "知识点精讲（自定义）", units: [] };
    let unit = custom.units.find((u) => u.unit === currentUnit);
    if (!unit) {
      unit = { unit: currentUnit, pages: [] };
      custom.units.push(unit);
    }
    const idx = unit.pages.findIndex((p) => p.id === currentPageId);
    if (idx >= 0) unit.pages[idx] = { ...unit.pages[idx], ...patch };
    else unit.pages.push({ id: currentPageId, ...patch });
    saveCustomKnowledge(custom);
    return custom;
  }

  async function reloadKnowledgeWithCustom() {
    const kRes = await fetch(`${HUB_BASE}/knowledge-bank.json`);
    const baseKnowledge = await kRes.json();
    knowledgeBank = mergeKnowledgeBanks(baseKnowledge, loadCustomKnowledge());
  }

  function touchSyncTimestamp() {
    if (typeof touchDataUpdatedAt === "function") touchDataUpdatedAt();
  }

  function pageImagePath(num) {
    return `assets/images/textbook/pages/page-${String(num).padStart(3, "0")}.png?v=${hubCacheBust}`;
  }

  function updateImageNav() {
    const multi = activePdfPages.length > 1;
    if (els.imagePrev) els.imagePrev.classList.toggle("hidden", !multi);
    if (els.imageNext) els.imageNext.classList.toggle("hidden", !multi);
    if (els.imagePager) {
      const png = activePdfPages[imagePageIndex];
      if (png) {
        els.imagePager.classList.remove("hidden");
        const printed = printedPageForPng(png);
        els.imagePager.textContent = multi
          ? `Page ${printed}（${imagePageIndex + 1}/${activePdfPages.length}）`
          : `Page ${printed}`;
      } else {
        els.imagePager.classList.add("hidden");
      }
    }
  }

  function fitImageInViewport() {
    if (!els.image || !els.imageViewport) return;
    const img = els.image;
    if (!img.naturalWidth || !img.naturalHeight) return;
    const vw = els.imageViewport.clientWidth - 16;
    const vh = els.imageViewport.clientHeight - 16;
    if (vw <= 0 || vh <= 0) return;
    const scale = Math.min(vw / img.naturalWidth, vh / img.naturalHeight, 1);
    img.style.width = `${Math.floor(img.naturalWidth * scale)}px`;
    img.style.height = `${Math.floor(img.naturalHeight * scale)}px`;
    img.style.maxWidth = "100%";
    img.style.maxHeight = "100%";
  }

  function showImageAt(index) {
    if (!activePageRef || !els.image) return;
    resetImageTransform();
    const apply = (src) => {
      els.image.onload = () => {
        fitImageInViewport();
        renderContent(activePageRef);
      };
      els.image.src = src;
      els.image.alt = activePageRef.label || "课本图片";
    };
    const fail = () => {
      if (activePageRef.fallbackImage) {
        const img = new Image();
        img.onload = () => apply(activePageRef.fallbackImage);
        img.onerror = () => { els.image.removeAttribute("src"); };
        img.src = activePageRef.fallbackImage;
      }
    };
    if (activePdfPages.length) {
      imagePageIndex = Math.max(0, Math.min(index, activePdfPages.length - 1));
      const src = pageImagePath(activePdfPages[imagePageIndex]);
      const img = new Image();
      img.onload = () => {
        apply(src);
      };
      img.onerror = fail;
      img.src = src;
      updateImageNav();
      refreshHighlightsOnPageChange();
      return;
    }
    if (!activePageRef.image) {
      fail();
      return;
    }
    const img = new Image();
    img.onload = () => apply(activePageRef.image);
    img.onerror = fail;
    img.src = activePageRef.image;
    updateImageNav();
  }

  function setImage(page) {
    activePageRef = page;
    activePdfPages = Array.isArray(page?.pdfPages) ? page.pdfPages.filter(Boolean) : [];
    imagePageIndex = 0;
    showImageAt(0);
    if (els.imageCaption) els.imageCaption.textContent = page?.label || "";
  }

  function renderContent(page) {
    if (!page) {
      if (els.content) {
        els.content.classList.remove("hidden");
        els.content.innerHTML = "<p class=\"model\">暂无内容</p>";
      }
      return;
    }
    if (mode === "reading") {
      renderReadingEditor(page);
    } else {
      if (els.pageEditor) els.pageEditor.classList.add("hidden");
      if (els.pageLabel) els.pageLabel.classList.add("hidden");
      if (els.contentPane) els.contentPane.classList.remove("reading-mode");
      if (els.content) els.content.classList.remove("hidden");
      if (els.audioBar) {
        els.audioBar.classList.add("hidden");
        els.audioBar.innerHTML = "";
      }
      if (els.studentRecordPanel) {
        els.studentRecordPanel.classList.add("hidden");
        els.studentRecordPanel.innerHTML = "";
      }
      if (els.snipPanel) {
        els.snipPanel.classList.add("hidden");
        els.snipPanel.innerHTML = "";
      }
      officialAudioEl = null;
      audioBarRenderedPageId = null;
      renderKnowledge(page);
      els.content.style.fontSize = `${fontScale}rem`;
      applyReadingLangDisplay();
    }
  }
  async function renderKnowledge(page) {
    const png = activePdfPages[imagePageIndex];
    if (els.pageLabel) {
      if (png) {
        els.pageLabel.classList.remove("hidden");
        els.pageLabel.textContent = `Page ${printedPageForPng(png)}`;
      } else {
        els.pageLabel.classList.add("hidden");
      }
    }
    if (els.pageEditor) els.pageEditor.classList.add("hidden");
    const lib = await fetchKnowledgeLibrary(page.id);
    const html = lib || page.bodyHtml || "";
    els.content.innerHTML = `<div class="knowledge-body">${sanitizeKnowledgeHtml(html)}</div>`;
    els.content.contentEditable = "true";
    els.content.classList.add("editable");
    const body = els.content.querySelector(".knowledge-body");
    if (body) classifyKnowledgeContent(body);
    applyEditorStyle();
    renderMathIn(els.content);
    if (body) applyGlossaryHighlights(body);
    applyReadingLangDisplay();
    await refreshSnipPanel(page.id);
  }

  async function saveCurrentKnowledge() {
    if (!els.content) return;
    const body = els.content.querySelector(".knowledge-body");
    if (body) classifyKnowledgeContent(body);
    const html = body ? body.innerHTML : els.content.innerHTML;
    try {
      await saveKnowledgeToLibrary(html);
    } catch (err) {
      showToast(err?.message || "保存失败", true);
    }
  }

  function toEmbedUrl(url) {
    if (!url) return "";
    if (url.includes("bilibili.com")) {
      const m = url.match(/BV[\w]+/);
      if (m) return `https://player.bilibili.com/player.html?bvid=${m[0]}&high_quality=1`;
    }
    if (url.includes("youtube.com/watch")) {
      const id = new URL(url).searchParams.get("v");
      if (id) return `https://www.youtube.com/embed/${id}`;
    }
    if (url.includes("youtu.be/")) {
      const id = url.split("youtu.be/")[1]?.split("?")[0];
      if (id) return `https://www.youtube.com/embed/${id}`;
    }
    return url;
  }

  function renderParts() {
    const pages = getSectionPages();
    if (!els.parts) return;
    els.parts.innerHTML = pages
      .map(
        (p) =>
          `<button type="button" class="study-hub-part-btn${p.id === currentPageId ? " active" : ""}" data-page-id="${p.id}">${p.label}</button>`,
      )
      .join("");
    els.parts.querySelectorAll(".study-hub-part-btn").forEach((btn) => {
      btn.addEventListener("click", () => selectPage(btn.dataset.pageId));
    });
  }

  function selectPage(pageId) {
    stopAllReading();
    if (studentRecordingActive) {
      stopStudentRecordingAndSave();
    } else {
      stopStudentRecording();
    }
    audioBarRenderedPageId = null;
    currentPageId = pageId;
    renderParts();
    const page = getCurrentPage();
    setImage(page);
    renderContent(page);
    saveState();
  }

  function renderUnits() {
    const bank = getBank();
    if (!bank || !els.units) return;
    const tabs = [
      `<button type="button" class="study-hub-section-btn${section === "intro" ? " active" : ""}" data-section="intro">开篇</button>`,
    ];
    (bank.units || []).forEach((u) => {
      tabs.push(
        `<button type="button" class="study-hub-unit-btn${section === "units" && u.unit === currentUnit ? " active" : ""}" data-section="units" data-unit="${u.unit}">Unit ${u.unit}</button>`,
      );
    });
    tabs.push(
      `<button type="button" class="study-hub-section-btn${section === "appendix" ? " active" : ""}" data-section="appendix">附录</button>`,
    );
    els.units.innerHTML = tabs.join("");
    els.units.querySelectorAll("[data-section]").forEach((btn) => {
      btn.addEventListener("click", () => {
        section = btn.dataset.section;
        if (section === "units") {
          currentUnit = Number(btn.dataset.unit || currentUnit);
        }
        const pages = getSectionPages();
        currentPageId = pages[0]?.id || "";
        renderUnits();
        renderParts();
        selectPage(currentPageId);
      });
    });
  }

  function applyTheme() {
    els.modal.classList.toggle("study-hub-dark", darkReading);
    if (els.theme) els.theme.textContent = darkReading ? "浅色" : "护眼";
  }

  function toggleToolbar() {
    const showReading = mode === "reading";
    const showKnowledge = mode === "knowledge";
    const showEdit = showReading || showKnowledge;
    const showZoom = showEdit;
    if (els.richToolbar) els.richToolbar.classList.toggle("hidden", !showKnowledge);
    if (els.readModeBtn) els.readModeBtn.classList.toggle("hidden", !showEdit);
    if (els.studentRecordBtn) els.studentRecordBtn.classList.toggle("hidden", !showReading);
    if (els.readingLangBtn) els.readingLangBtn.classList.toggle("hidden", !showEdit);
    if (els.ttsRateWrap) els.ttsRateWrap.classList.toggle("hidden", !showEdit);
    if (els.ttsVoiceZhWrap) els.ttsVoiceZhWrap.classList.toggle("hidden", !showEdit || !readingShowZh);
    if (els.ttsVoiceEnWrap) els.ttsVoiceEnWrap.classList.toggle("hidden", !showEdit);
    if (els.importCsv) els.importCsv.classList.toggle("hidden", !showReading);
    if (els.savePageText) els.savePageText.classList.toggle("hidden", !showReading);
    if (els.saveKnowledge) els.saveKnowledge.classList.toggle("hidden", !showKnowledge);
    if (els.snipTask) els.snipTask.classList.toggle("hidden", !showKnowledge);
    if (els.snipHomework) els.snipHomework.classList.toggle("hidden", !showKnowledge);
    if (els.bgPickerWrap) els.bgPickerWrap.classList.toggle("hidden", !showEdit);
    if (els.enFontFamilyWrap) els.enFontFamilyWrap.classList.toggle("hidden", !showEdit);
    if (els.zhFontFamilyWrap) els.zhFontFamilyWrap.classList.toggle("hidden", !showEdit || !readingShowZh);
    if (els.fontDown) els.fontDown.classList.toggle("hidden", !showEdit);
    if (els.fontUp) els.fontUp.classList.toggle("hidden", !showEdit);
    if (els.zhFontDown) els.zhFontDown.classList.toggle("hidden", !showEdit || !readingShowZh);
    if (els.zhFontUp) els.zhFontUp.classList.toggle("hidden", !showEdit || !readingShowZh);
    if (els.enBold) els.enBold.classList.toggle("hidden", !showEdit);
    if (els.enColorWrap) els.enColorWrap.classList.toggle("hidden", !showEdit);
    if (els.zhColorWrap) els.zhColorWrap.classList.toggle("hidden", !showEdit || !readingShowZh);
    if (els.zhBold) els.zhBold.classList.toggle("hidden", !showEdit || !readingShowZh);
    if (els.zoomIn) els.zoomIn.classList.toggle("hidden", !showZoom);
    if (els.zoomOut) els.zoomOut.classList.toggle("hidden", !showZoom);
    if (els.zoomReset) els.zoomReset.classList.toggle("hidden", !showZoom);
    if (els.readModeBtn) els.readModeBtn.textContent = activePlayback === "read" ? "停止" : "朗读";
    if (els.switchKnowledge) els.switchKnowledge.classList.toggle("hidden", !showReading);
    if (els.switchReading) els.switchReading.classList.toggle("hidden", !showKnowledge);
    updateReadingLangDisplayBtn();
  }

  async function loadBanks() {
    libraryCache.clear();
    hubCacheBust = Date.now();
    const bust = `t=${hubCacheBust}`;
    const [rRes, kRes, gRes, aRes, mRes, auRes] = await Promise.all([
      fetch(`${HUB_BASE}/reading-bank.json?${bust}`),
      fetch(`${HUB_BASE}/knowledge-bank.json?${bust}`),
      fetch(`${HUB_BASE}/glossary.json?${bust}`),
      fetch(`${HUB_BASE}/appendix-words.json?${bust}`),
      fetch(`${HUB_BASE}/pdf-page-map.json?${bust}`),
      fetch(`${HUB_BASE}/audio-bank.json?${bust}`),
    ]);
    if (!rRes.ok || !kRes.ok) throw new Error("load failed");
    readingBank = await rRes.json();
    const baseKnowledge = await kRes.json();
    try {
      knowledgeBank = mergeKnowledgeBanks(baseKnowledge, loadCustomKnowledge());
    } catch {
      knowledgeBank = baseKnowledge;
    }
    if (gRes.ok) glossary = await gRes.json();
    if (aRes.ok) appendixWordsBank = await aRes.json();
    if (mRes.ok) {
      const pm = await mRes.json();
      applyPdfPageMapFromJson(pm);
    }
    if (auRes.ok) audioBank = await auRes.json();
    else audioBank = null;
    buildGlossaryTerms();
  }

  function mapPageIdBetweenModes(pageId, fromMode, toMode) {
    if (!pageId || fromMode === toMode) return pageId;
    if (toMode === "knowledge") {
      if (/^u(\d+)-unit-(start|next)$/.test(pageId)) {
        const u = pageId.match(/^u(\d+)/)[1];
        return `u${u}-k-part-a`;
      }
      if (/^u(\d+)-part-[abc]$/.test(pageId)) return pageId.replace(/^u(\d+)-/, "u$1-k-");
      if (/^u(\d+)-reading$/.test(pageId)) return pageId.replace("-reading", "-k-reading");
      if (pageId.startsWith("appendix-") && !pageId.includes("-k-")) {
        return pageId.replace(/^appendix-/, "appendix-k-");
      }
      return pageId;
    }
    if (/^u(\d+)-k-part-[abc]$/.test(pageId)) return pageId.replace(/^u(\d+)-k-/, "u$1-");
    if (/^u(\d+)-k-reading$/.test(pageId)) return pageId.replace("-k-reading", "-reading");
    if (pageId.startsWith("appendix-k-")) return pageId.replace("appendix-k-", "appendix-");
    return pageId;
  }

  function pageExistsInBank(pageId, bank) {
    if (!pageId || !bank) return false;
    const intro = bank.intro?.pages?.some((p) => p.id === pageId);
    if (intro) return true;
    const appendix = bank.appendix?.pages?.some((p) => p.id === pageId);
    if (appendix) return true;
    return (bank.units || []).some((u) => (u.pages || []).some((p) => p.id === pageId));
  }

  function resolvePageIdForBank(pageId, bank) {
    if (pageExistsInBank(pageId, bank)) return pageId;
    const unit = currentUnit;
    const unitData = bank?.units?.find((u) => u.unit === unit);
    const partMatch = pageId?.match(/part-[abc]|reading/);
    if (partMatch && unitData?.pages?.length) {
      const want = partMatch[0].includes("reading") ? "reading" : partMatch[0];
      const found = unitData.pages.find((p) => p.id.includes(want));
      if (found) return found.id;
    }
    return unitData?.pages?.[0]?.id || pageId;
  }

  function switchHubMode(targetMode) {
    if (mode === targetMode) return;
    stopAllReading();
    const nextId = mapPageIdBetweenModes(currentPageId, mode, targetMode);
    mode = targetMode;
    const bank = getBank();
    els.title.textContent = bank?.title || "";
    currentPageId = resolvePageIdForBank(nextId, bank);
    toggleToolbar();
    renderUnits();
    renderParts();
    selectPage(currentPageId);
    saveState();
    showToast(targetMode === "knowledge" ? "已切换到知识点精讲" : "已切换到课文中英文讲读", false);
  }

  function openHub(hubMode) {
    loadBanks()
      .then(() => {
        mode = hubMode;
        const bank = getBank();
        els.title.textContent = bank?.title || "";
        const saved = loadState();
        if (saved.mode === mode && saved.currentUnit) {
          section = saved.section || "units";
          currentUnit = saved.currentUnit;
          currentPageId = saved.currentPageId || "";
          fontScale = saved.fontScale || 1;
          readingEnFontScale = saved.readingEnFontScale || saved.fontScale || 1;
          readingZhFontScale = saved.readingZhFontScale || saved.fontScale || 1;
          darkReading = !!saved.darkReading;
          readingBgColor = saved.readingBgColor || "#ffffff";
          const legacyFont = saved.readingFontFamily || "system-ui, sans-serif";
          readingEnFontFamily = saved.readingEnFontFamily || legacyFont;
          readingZhFontFamily = saved.readingZhFontFamily || legacyFont;
          readingEnColor = saved.readingEnColor || "#1e293b";
          readingZhColor = saved.readingZhColor || "#1d4ed8";
          readingEnBold = saved.readingEnBold !== undefined ? !!saved.readingEnBold : false;
          readingZhBold = saved.readingZhBold !== undefined ? !!saved.readingZhBold : true;
          readingShowZh = saved.readingShowZh !== undefined ? !!saved.readingShowZh : true;
          ttsRate = Math.min(2.5, Math.max(0.65, Number(saved.ttsRate) || 0.88));
          ttsVoiceUriZh = saved.ttsVoiceUriZh || "";
          ttsVoiceUriEn = saved.ttsVoiceUriEn || "";
          ttsVoiceUriLegacy = saved.ttsVoiceUri || "";
        }
        if (els.bgColor) els.bgColor.value = readingBgColor;
        if (els.enFontFamily) els.enFontFamily.value = readingEnFontFamily;
        if (els.zhFontFamily) els.zhFontFamily.value = readingZhFontFamily;
        if (els.enColor) els.enColor.value = readingEnColor;
        if (els.zhColor) els.zhColor.value = readingZhColor;
        if (els.ttsRate) els.ttsRate.value = String(ttsRate);
        if (els.ttsRateVal) els.ttsRateVal.textContent = ttsRate.toFixed(2);
        applyReadingLangDisplay();
        ensureVoices().then(() => {
          if (els.ttsVoiceZh && ttsVoiceUriZh) els.ttsVoiceZh.value = ttsVoiceUriZh;
          if (els.ttsVoiceEn && ttsVoiceUriEn) els.ttsVoiceEn.value = ttsVoiceUriEn;
        });
        if (!getUnitData(currentUnit) && section === "units") {
          currentUnit = bank.units?.[0]?.unit || 1;
        }
        if (section === "intro") {
          currentPageId = bank.intro?.pages?.[0]?.id || "";
        } else if (section === "appendix") {
          currentPageId = bank.appendix?.pages?.[0]?.id || "";
        } else {
          const unit = getUnitData(currentUnit);
          if (!currentPageId) currentPageId = unit?.pages?.[0]?.id || "";
        }
        applyTheme();
        toggleToolbar();
        renderUnits();
        renderParts();
        selectPage(currentPageId);
        if (isMobileLayout()) setMobilePanel("text");
        else updateMobilePanelUI();
        els.modal.classList.remove("hidden");
        document.body.classList.add("study-hub-open");
      })
      .catch(() => {
        window.alert("无法加载讲读/精讲内容。请用 启动.bat 访问，并运行 scripts/build-study-hub.py");
      });
  }

  function closeHub() {
    stopAllReading();
    els.modal.classList.add("hidden");
    document.body.classList.remove("study-hub-open");
    resetImageTransform();
  }

  function exportKnowledge() {
    const data = loadCustomKnowledge() || knowledgeBank;
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `knowledge-bank-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function importKnowledgeFile(file) {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const data = JSON.parse(String(reader.result || ""));
        if (!data.units) throw new Error("invalid");
        saveCustomKnowledge(data);
        knowledgeBank = mergeKnowledgeBanks(knowledgeBank, data);
        if (mode === "knowledge") {
          renderUnits();
          renderParts();
          selectPage(currentPageId);
        }
        window.alert("知识点已导入并刷新。自定义内容保存在本机浏览器。");
      } catch {
        window.alert("导入失败：请使用导出的 JSON 格式。");
      }
    };
    reader.readAsText(file, "UTF-8");
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      els.stage?.requestFullscreen?.().catch(() => {});
    } else {
      document.exitFullscreen?.();
    }
  }

  function bindEvents() {
    if (els.openReading) els.openReading.addEventListener("click", () => openHub("reading"));
    if (els.openKnowledge) els.openKnowledge.addEventListener("click", () => openHub("knowledge"));
    if (els.switchKnowledge) els.switchKnowledge.addEventListener("click", () => switchHubMode("knowledge"));
    if (els.switchReading) els.switchReading.addEventListener("click", () => switchHubMode("reading"));
    if (els.close) els.close.addEventListener("click", closeHub);
    els.modal.addEventListener("click", (e) => {
      if (e.target === els.modal) closeHub();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !els.modal.classList.contains("hidden")) closeHub();
    });
    if (els.fontDown) {
      els.fontDown.addEventListener("click", () => {
        readingEnFontScale = Math.max(0.85, readingEnFontScale - 0.05);
        applyEditorStyle();
        saveState();
      });
    }
    if (els.fontUp) {
      els.fontUp.addEventListener("click", () => {
        readingEnFontScale = Math.min(1.5, readingEnFontScale + 0.05);
        applyEditorStyle();
        saveState();
      });
    }
    if (els.zhFontDown) {
      els.zhFontDown.addEventListener("click", () => {
        readingZhFontScale = Math.max(0.85, readingZhFontScale - 0.05);
        applyEditorStyle();
        saveState();
      });
    }
    if (els.zhFontUp) {
      els.zhFontUp.addEventListener("click", () => {
        readingZhFontScale = Math.min(1.5, readingZhFontScale + 0.05);
        applyEditorStyle();
        saveState();
      });
    }
    if (els.theme) {
      els.theme.addEventListener("click", () => {
        darkReading = !darkReading;
        applyTheme();
        saveState();
      });
    }
    if (els.fullscreen) els.fullscreen.addEventListener("click", toggleFullscreen);
    if (els.zoomIn) els.zoomIn.addEventListener("click", () => zoomImage(0.25));
    if (els.zoomOut) els.zoomOut.addEventListener("click", () => zoomImage(-0.25));
    if (els.zoomReset) els.zoomReset.addEventListener("click", resetImageTransform);
    if (els.savePageText) els.savePageText.addEventListener("click", saveCurrentPageText);
    if (els.saveKnowledge) els.saveKnowledge.addEventListener("click", saveCurrentKnowledge);
    if (els.bgColor) {
      els.bgColor.addEventListener("input", () => {
        readingBgColor = els.bgColor.value;
        applyEditorStyle();
        saveState();
      });
    }
    if (els.enFontFamily) {
      els.enFontFamily.addEventListener("change", () => {
        readingEnFontFamily = els.enFontFamily.value;
        applyEditorStyle();
        saveState();
      });
    }
    if (els.zhFontFamily) {
      els.zhFontFamily.addEventListener("change", () => {
        readingZhFontFamily = els.zhFontFamily.value;
        applyEditorStyle();
        saveState();
      });
    }
    if (els.zhColor) {
      els.zhColor.addEventListener("input", () => {
        readingZhColor = els.zhColor.value;
        applyEditorStyle();
        saveState();
      });
    }
    if (els.enColor) {
      els.enColor.addEventListener("input", () => {
        readingEnColor = els.enColor.value;
        applyEditorStyle();
        saveState();
      });
    }
    if (els.ttsRate) {
      els.ttsRate.addEventListener("input", () => {
        ttsRate = Math.min(2.5, Math.max(0.65, Number(els.ttsRate.value) || 0.88));
        if (els.ttsRateVal) els.ttsRateVal.textContent = ttsRate.toFixed(2);
        saveState();
      });
    }
    if (els.ttsVoiceZh) {
      els.ttsVoiceZh.addEventListener("change", () => {
        ttsVoiceUriZh = els.ttsVoiceZh.value || "";
        saveState();
      });
    }
    if (els.ttsVoiceEn) {
      els.ttsVoiceEn.addEventListener("change", () => {
        ttsVoiceUriEn = els.ttsVoiceEn.value || "";
        saveState();
      });
    }
    if (els.enBold) {
      els.enBold.addEventListener("click", () => {
        readingEnBold = !readingEnBold;
        applyEditorStyle();
        saveState();
      });
    }
    if (els.zhBold) {
      els.zhBold.addEventListener("click", () => {
        readingZhBold = !readingZhBold;
        applyEditorStyle();
        saveState();
      });
    }
    if (els.pageEditor) {
      els.pageEditor.addEventListener("blur", () => refreshEditableContent());
    }
    if (els.content) {
      els.content.addEventListener("blur", () => refreshEditableContent(), true);
      els.content.addEventListener("input", () => {
        if (mode === "knowledge") {
          const body = getKnowledgeBodyEl();
          if (body) classifyKnowledgeContent(body);
        }
      });
    }
    if (els.importCsv && els.importCsvFile) {
      els.importCsv.addEventListener("click", () => els.importCsvFile.click());
      els.importCsvFile.addEventListener("change", async () => {
        const f = els.importCsvFile.files?.[0];
        els.importCsvFile.value = "";
        if (!f) return;
        try {
          await importCsvFromFile(f);
        } catch {
          /* toast shown */
        }
      });
    }
    if (els.readModeBtn) els.readModeBtn.addEventListener("click", startReadingMode);
    if (els.readingLangBtn) els.readingLangBtn.addEventListener("click", toggleReadingLangDisplay);
    if (els.studentRecordBtn) els.studentRecordBtn.addEventListener("click", toggleStudentRecording);
    if (els.snipTask) els.snipTask.addEventListener("click", () => openSnipModal("task"));
    if (els.snipHomework) els.snipHomework.addEventListener("click", () => openSnipModal("homework"));
    if (els.snipModalClose) els.snipModalClose.addEventListener("click", closeSnipModal);
    if (els.snipModal) {
      els.snipModal.addEventListener("click", (e) => {
        if (e.target === els.snipModal) closeSnipModal();
      });
    }
    if (els.snipPasteZone) {
      els.snipPasteZone.addEventListener("click", () => els.snipPasteZone.focus());
      els.snipPasteZone.addEventListener("paste", handleSnipPasteEvent);
    }
    document.addEventListener("paste", handleSnipPasteEvent);
    if (els.snipPickFile && els.snipFileInput) {
      els.snipPickFile.addEventListener("click", () => els.snipFileInput.click());
      els.snipFileInput.addEventListener("change", () => {
        const f = els.snipFileInput.files?.[0];
        els.snipFileInput.value = "";
        if (f) setSnipPendingBlob(f);
      });
    }
    if (els.snipSave) els.snipSave.addEventListener("click", saveSnipFromModal);
    if (els.snipViewerClose) els.snipViewerClose.addEventListener("click", closeSnipViewer);
    if (els.snipViewerBackdrop) els.snipViewerBackdrop.addEventListener("click", closeSnipViewer);
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && els.snipViewer && !els.snipViewer.classList.contains("hidden")) {
        closeSnipViewer();
      }
    });
    if (els.imagePrev) {
      els.imagePrev.addEventListener("click", () => showImageAt(imagePageIndex - 1));
    }
    if (els.imageNext) {
      els.imageNext.addEventListener("click", () => showImageAt(imagePageIndex + 1));
    }
    if (els.insertImage && els.insertImageFile) {
      els.insertImage.addEventListener("click", () => els.insertImageFile.click());
      els.insertImageFile.addEventListener("change", async () => {
        const f = els.insertImageFile.files?.[0];
        els.insertImageFile.value = "";
        if (!f) return;
        try {
          await insertKnowledgeImage(f);
        } catch (err) {
          showToast(err?.message || "图片上传失败", true);
        }
      });
    }
    if (els.insertAudio && els.insertAudioFile) {
      els.insertAudio.addEventListener("click", () => {
        const url = window.prompt("音频链接 (https://...) 或留空选择本地文件", "");
        if (url) {
          insertHtmlAtCursor(`<figure class="media-embed"><audio controls src="${escapeHtml(url.trim())}"></audio></figure>`);
          return;
        }
        els.insertAudioFile.click();
      });
      els.insertAudioFile.addEventListener("change", async () => {
        const f = els.insertAudioFile.files?.[0];
        els.insertAudioFile.value = "";
        if (!f) return;
        try {
          await insertKnowledgeAudio(f);
        } catch (err) {
          showToast(err?.message || "音频上传失败", true);
        }
      });
    }
    if (els.insertTable) els.insertTable.addEventListener("click", insertKnowledgeTable);
    if (els.insertLink) els.insertLink.addEventListener("click", insertKnowledgeLink);
    if (els.insertVideo) els.insertVideo.addEventListener("click", insertKnowledgeVideo);
  }

  async function applyLanSync() {
    libraryCache.clear();
    hubCacheBust = Date.now();
    if (pdfPageMap) applyPdfPageMapFromJson(pdfPageMap);
    try {
      await reloadKnowledgeWithCustom();
    } catch {
      /* offline */
    }
    if (!els.modal || els.modal.classList.contains("hidden")) return;
    const active = document.activeElement;
    if (active && els.modal.contains(active) && active.isContentEditable) return;
    const page = getCurrentPage();
    if (!page) return;
    if (mode === "knowledge") {
      await renderKnowledge(page);
    } else if (mode === "reading") {
      await renderReadingEditor(page);
    }
  }

  function init() {
    if (!cacheElements()) return;
    bindImagePanZoom();
    bindMobileTabs();
    bindEvents();
    window.addEventListener("resize", () => {
      if (!els.modal?.classList.contains("hidden")) fitImageInViewport();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.StudyHub = {
    applyLanSync,
    clearLibraryCache: () => libraryCache.clear(),
  };
})();
