/**
 * Daily Gratitude · 每日感恩
 * Warm family-friendly gratitude journal with optional scenic background.
 */
(function () {
  const ENTRIES_KEY = "english_grade6_gratitude_entries_v1";
  const SETTINGS_KEY = "english_grade6_gratitude_settings_v1";

  const DEFAULT_SETTINGS = {
    backgroundDataUrl: "",
    applyGlobalBg: true,
    reminderEnabled: false,
    reminderTime: "20:00",
    lastReminderDate: "",
  };

  const WARM_QUOTES = [
    { zh: "每天一点点，梦想就会靠近一点。", en: "Small steps every day lead to big dreams." },
    { zh: "感恩让心变得更柔软，也让家更温暖。", en: "Gratitude softens the heart and warms the home." },
    { zh: "你已经很棒了，继续加油！", en: "You are doing great — keep going!" },
    { zh: "把今天的好事记下来，明天会更明亮。", en: "Write down today's good things; tomorrow will feel brighter." },
    { zh: "感谢身边的人，也感谢努力的自己。", en: "Thank the people around you — and yourself too." },
    { zh: "每一次表达感谢，都是成长。", en: "Every thank-you is a little act of growth." },
    { zh: "家是因为爱而发光的地方。", en: "Home shines because of love." },
    { zh: "用心发现美好，世界会回应你。", en: "Notice the good, and the world answers back." },
  ];

  let entries = [];
  let settings = { ...DEFAULT_SETTINGS };
  let reminderTimer = null;

  const $ = (id) => document.getElementById(id);

  function todayKey() {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  }

  function formatDisplayDate(key) {
    if (!key) return "";
    const [y, m, d] = key.split("-");
    return `${y}年${Number(m)}月${Number(d)}日`;
  }

  function loadEntries() {
    try {
      const raw = window.localStorage.getItem(ENTRIES_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function loadSettings() {
    try {
      const raw = window.localStorage.getItem(SETTINGS_KEY);
      if (!raw) return { ...DEFAULT_SETTINGS };
      return { ...DEFAULT_SETTINGS, ...JSON.parse(raw) };
    } catch {
      return { ...DEFAULT_SETTINGS };
    }
  }

  function saveEntries() {
    window.localStorage.setItem(ENTRIES_KEY, JSON.stringify(entries));
    if (typeof window.touchDataUpdatedAt === "function") window.touchDataUpdatedAt();
  }

  function saveSettings() {
    window.localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
    if (typeof window.touchDataUpdatedAt === "function") window.touchDataUpdatedAt();
  }

  function pickDailyQuote() {
    const day = new Date().getDate();
    return WARM_QUOTES[day % WARM_QUOTES.length];
  }

  function applyBackground() {
    const url = settings.backgroundDataUrl;
    const useGlobal = settings.applyGlobalBg !== false;
    if (url && useGlobal) {
      document.body.classList.add("has-gratitude-bg");
      document.body.style.setProperty("--gratitude-bg-image", `url("${url}")`);
    } else {
      document.body.classList.remove("has-gratitude-bg");
      document.body.style.removeProperty("--gratitude-bg-image");
    }
    const panel = $("gratitude");
    if (panel) {
      panel.classList.toggle("gratitude-has-panel-bg", Boolean(url));
      if (url) panel.style.setProperty("--gratitude-panel-bg", `url("${url}")`);
      else panel.style.removeProperty("--gratitude-panel-bg");
    }
  }

  function compressImageFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onerror = () => reject(new Error("read failed"));
      reader.onload = (e) => {
        const img = new Image();
        img.onerror = () => reject(new Error("image load failed"));
        img.onload = () => {
          const maxW = 1920;
          const scale = Math.min(1, maxW / img.width);
          const w = Math.max(1, Math.round(img.width * scale));
          const h = Math.max(1, Math.round(img.height * scale));
          const canvas = document.createElement("canvas");
          canvas.width = w;
          canvas.height = h;
          canvas.getContext("2d").drawImage(img, 0, 0, w, h);
          resolve(canvas.toDataURL("image/jpeg", 0.82));
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    });
  }

  function renderQuote() {
    const q = pickDailyQuote();
    const el = $("gratitudeDailyQuote");
    if (!el) return;
    el.innerHTML = `<span class="gratitude-quote-zh">${q.zh}</span><span class="gratitude-quote-en">${q.en}</span>`;
  }

  function renderTodayForm() {
    const key = todayKey();
    const label = $("gratitudeTodayLabel");
    const input = $("gratitudeInput");
    const parentNote = $("gratitudeParentNoteInput");
    if (label) {
      label.textContent = `今天是 ${formatDisplayDate(key)} · Today is ${key}`;
    }
    const today = entries.find((e) => e.date === key);
    if (input) input.value = today?.text || "";
    if (parentNote) parentNote.value = today?.parentNote || "";
  }

  function renderWall() {
    const wall = $("gratitudeWall");
    if (!wall) return;
    const sorted = [...entries].sort((a, b) => (b.date < a.date ? -1 : b.date > a.date ? 1 : 0));
    if (sorted.length === 0) {
      wall.innerHTML = `<p class="gratitude-wall-empty">还没有记录呢，写下第一条感恩吧 🌱<br><span class="gratitude-wall-empty-en">No entries yet — start your first gratitude note!</span></p>`;
      return;
    }
    wall.innerHTML = sorted
      .map((entry, idx) => {
        const hues = ["peach", "mint", "sky", "lilac", "cream"];
        const tone = hues[idx % hues.length];
        const note = entry.parentNote
          ? `<p class="gratitude-card-parent">💌 家长鼓励：${escapeHtml(entry.parentNote)}</p>`
          : "";
        return `<article class="gratitude-card gratitude-card-${tone}">
          <time class="gratitude-card-date" datetime="${entry.date}">${formatDisplayDate(entry.date)}</time>
          <p class="gratitude-card-text">${escapeHtml(entry.text)}</p>
          ${note}
        </article>`;
      })
      .join("");
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function setFeedback(msg, ok) {
    const el = $("gratitudeFeedback");
    if (!el) return;
    el.textContent = msg;
    el.dataset.tone = ok ? "ok" : "error";
  }

  function saveTodayGratitude() {
    const input = $("gratitudeInput");
    const text = (input?.value || "").trim();
    if (!text) {
      setFeedback("请先写下今天感恩的一件事哦。", false);
      return;
    }
    if (text.length > 500) {
      setFeedback("内容太长啦，请控制在 500 字以内。", false);
      return;
    }
    const key = todayKey();
    const existing = entries.find((e) => e.date === key);
    if (existing) {
      existing.text = text;
      existing.updatedAt = new Date().toISOString();
    } else {
      entries.push({
        date: key,
        text,
        parentNote: "",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      });
    }
    saveEntries();
    setFeedback("今天的感恩已保存！谢谢你愿意分享温暖 💛", true);
    renderWall();
    if (typeof window.updateTabCounts === "function") window.updateTabCounts();
    if (typeof window.scheduleLanSync === "function") window.scheduleLanSync(true);
  }

  function saveParentEncouragement() {
    const run = () => {
      const note = ($("gratitudeParentNoteInput")?.value || "").trim();
      if (!note) {
        setFeedback("请先写下鼓励语。", false);
        return;
      }
      const key = todayKey();
      let today = entries.find((e) => e.date === key);
      if (!today) {
        today = {
          date: key,
          text: ($("gratitudeInput")?.value || "").trim() || "（家长先留下了鼓励语）",
          parentNote: note,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        entries.push(today);
      } else {
        today.parentNote = note;
        today.updatedAt = new Date().toISOString();
      }
      saveEntries();
      setFeedback("家长的鼓励语已保存！", true);
      renderWall();
      if (typeof window.scheduleLanSync === "function") window.scheduleLanSync(true);
    };
    run();
  }

  async function onBackgroundSelected(file) {
    if (!file || !file.type.startsWith("image/")) {
      setFeedback("请选择图片文件（风景照最佳）。", false);
      return;
    }
    if (file.size > 12 * 1024 * 1024) {
      setFeedback("图片较大，正在压缩…", true);
    }
    try {
      const dataUrl = await compressImageFile(file);
      settings.backgroundDataUrl = dataUrl;
      saveSettings();
      applyBackground();
      setFeedback("风景背景已设置！没有图片时会恢复默认配色。", true);
    } catch {
      setFeedback("背景图片处理失败，请换一张试试。", false);
    }
  }

  function clearBackground() {
    settings.backgroundDataUrl = "";
    saveSettings();
    applyBackground();
    const fileInput = $("gratitudeBgFile");
    if (fileInput) fileInput.value = "";
    setFeedback("已恢复默认配色。", true);
  }

  function saveReminderSettings() {
    settings.reminderEnabled = Boolean($("gratitudeReminderEnabled")?.checked);
    settings.reminderTime = $("gratitudeReminderTime")?.value || "20:00";
    saveSettings();
    setupReminder();
    setFeedback(settings.reminderEnabled ? `已开启每日提醒（${settings.reminderTime}）` : "已关闭每日提醒。", true);
  }

  async function requestNotificationPermission() {
    if (!("Notification" in window)) {
      setFeedback("当前浏览器不支持桌面提醒。", false);
      return;
    }
    const perm = await Notification.requestPermission();
    if (perm === "granted") {
      setFeedback("提醒权限已开启！", true);
    } else {
      setFeedback("未获得提醒权限，可在浏览器设置中允许通知。", false);
    }
  }

  function setupReminder() {
    if (reminderTimer) {
      clearInterval(reminderTimer);
      reminderTimer = null;
    }
    if (!settings.reminderEnabled) return;
    reminderTimer = setInterval(() => {
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, "0");
      const mm = String(now.getMinutes()).padStart(2, "0");
      const current = `${hh}:${mm}`;
      const today = todayKey();
      if (current !== settings.reminderTime) return;
      if (settings.lastReminderDate === today) return;
      const hasToday = entries.some((e) => e.date === today);
      if (hasToday) return;
      settings.lastReminderDate = today;
      saveSettings();
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("每日感恩 🌻", {
          body: "今天，你想感谢什么呢？和家人一起写下一句话吧。",
        });
      }
    }, 30000);
  }

  function bindEvents() {
    $("saveGratitude")?.addEventListener("click", saveTodayGratitude);
    $("saveGratitudeParentNote")?.addEventListener("click", saveParentEncouragement);
    $("gratitudeBgFile")?.addEventListener("change", (e) => {
      const file = e.target.files?.[0];
      if (file) onBackgroundSelected(file);
    });
    $("clearGratitudeBg")?.addEventListener("click", clearBackground);
    $("gratitudeApplyGlobalBg")?.addEventListener("change", (e) => {
      settings.applyGlobalBg = e.target.checked;
      saveSettings();
      applyBackground();
    });
    $("saveGratitudeReminder")?.addEventListener("click", saveReminderSettings);
    $("requestGratitudeNotify")?.addEventListener("click", requestNotificationPermission);
  }

  function syncFormFromSettings() {
    const global = $("gratitudeApplyGlobalBg");
    const reminder = $("gratitudeReminderEnabled");
    const time = $("gratitudeReminderTime");
    if (global) global.checked = settings.applyGlobalBg !== false;
    if (reminder) reminder.checked = Boolean(settings.reminderEnabled);
    if (time) time.value = settings.reminderTime || "20:00";
  }

  function onTabActivate() {
    renderQuote();
    renderTodayForm();
    renderWall();
    syncFormFromSettings();
    applyBackground();
  }

  function getEntryCount() {
    return entries.length;
  }

  function getSyncPayload() {
    return {
      gratitudeEntries: entries,
      gratitudeSettings: {
        ...settings,
        backgroundDataUrl: settings.backgroundDataUrl || "",
      },
    };
  }

  function applySyncPayload(payload) {
    if (!payload || typeof payload !== "object") return;
    if (Array.isArray(payload.gratitudeEntries)) {
      entries = payload.gratitudeEntries;
      window.localStorage.setItem(ENTRIES_KEY, JSON.stringify(entries));
    }
    if (payload.gratitudeSettings && typeof payload.gratitudeSettings === "object") {
      settings = { ...DEFAULT_SETTINGS, ...payload.gratitudeSettings };
      window.localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
      applyBackground();
      syncFormFromSettings();
    }
    renderWall();
    renderTodayForm();
  }

  function init() {
    entries = loadEntries();
    settings = loadSettings();
    bindEvents();
    renderQuote();
    renderTodayForm();
    renderWall();
    syncFormFromSettings();
    applyBackground();
    setupReminder();
  }

  window.GratitudeHub = {
    init,
    onTabActivate,
    getEntryCount,
    getSyncPayload,
    applySyncPayload,
  };
})();
