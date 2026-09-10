/**
 * License auth for ECS / LAN server — persistent token until license expiry.
 */
(function authModule() {
  const TOKEN_KEY = "pep6_auth_token_v1";

  let authRequired = false;
  let loggedIn = false;
  let licenseLabel = "";
  let licenseExpiresAt = "";
  let isAdmin = false;
  let studentLoginEnabled = false;

  const els = {};
  const AUTH_FETCH_MS = 8000;

  function apiUrl(path) {
    if (typeof window.pep6Url === "function") return window.pep6Url(path);
    return path;
  }

  function fetchAuth(url, options = {}) {
    const ctrl = new AbortController();
    const timer = window.setTimeout(() => ctrl.abort(), AUTH_FETCH_MS);
    return fetch(url, { ...options, signal: ctrl.signal }).finally(() => window.clearTimeout(timer));
  }

  function unlockPage() {
    document.body.classList.remove("auth-locked");
    hideGate();
  }

  function getToken() {
    return window.localStorage.getItem(TOKEN_KEY) || "";
  }

  function setToken(token) {
    if (token) window.localStorage.setItem(TOKEN_KEY, token);
    else window.localStorage.removeItem(TOKEN_KEY);
  }

  (function migrateSessionToken() {
    const legacy = window.sessionStorage.getItem(TOKEN_KEY);
    if (legacy && !window.localStorage.getItem(TOKEN_KEY)) {
      window.localStorage.setItem(TOKEN_KEY, legacy);
      window.sessionStorage.removeItem(TOKEN_KEY);
    }
  })();

  function authHeaders(extra = {}) {
    const headers = { ...extra };
    const token = getToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
      headers["X-Auth-Token"] = token;
    }
    return headers;
  }

  function isAuthRequired() {
    return authRequired;
  }

  function isLoggedIn() {
    return !authRequired || loggedIn;
  }

  function isAdminUser() {
    return isAdmin;
  }

  function isStudentLoginEnabled() {
    return studentLoginEnabled;
  }

  function formatLicenseInput(value) {
    const raw = String(value || "").replace(/[^A-Za-z0-9]/g, "").toUpperCase();
    if (!raw) return "";
    const body = raw.startsWith("PEP6") ? raw.slice(4) : raw;
    const chunks = body.slice(0, 12).match(/.{1,4}/g) || [];
    return "PEP6-" + chunks.join("-");
  }

  function applyAdminUi() {
    document.body.classList.toggle("pep6-admin", isAdmin);
    const hostBox = document.getElementById("hostAdminBox");
    if (hostBox) {
      hostBox.classList.toggle("hidden", !isAdmin);
    }
    if (typeof window.onPep6AdminChange === "function") {
      window.onPep6AdminChange(isAdmin);
    }
  }

  function applyAuthUserBar() {
    const bar = document.getElementById("authUserBar");
    if (!bar) return;
    bar.classList.toggle("hidden", !(authRequired && loggedIn));
  }

  function applyStudentLoginUi() {
    const showStudent = studentLoginEnabled && !isAdmin;
    if (els.studentBlock) {
      els.studentBlock.classList.toggle("hidden", !showStudent);
    }
    if (els.gateIntro) {
      els.gateIntro.textContent = showStudent
        ? "请输入管理员密码，或使用老师发放的 PEP6 授权码登录。"
        : "请输入管理员密码登录。学生授权码入口由管理员开放后显示。";
    }
  }

  function showGate(message) {
    if (!els.gate) return;
    els.gate.classList.remove("hidden");
    document.body.classList.add("auth-locked");
    applyStudentLoginUi();
    if (els.feedback && message) {
      els.feedback.textContent = message;
      els.feedback.dataset.tone = "warn";
    }
  }

  function hideGate() {
    if (!els.gate) return;
    els.gate.classList.add("hidden");
    document.body.classList.remove("auth-locked");
  }

  function updateStatusBar() {
    if (!els.statusBar) return;
    if (!authRequired) {
      els.statusBar.classList.add("hidden");
      return;
    }
    els.statusBar.classList.remove("hidden");
    if (loggedIn) {
      if (isAdmin) {
        els.statusBar.textContent = "管理员已登录 · 永久有效";
        els.statusBar.dataset.tone = "ok";
        return;
      }
      const exp = licenseExpiresAt ? ` · 有效期至 ${licenseExpiresAt}` : "";
      els.statusBar.textContent = `已登录：${licenseLabel || "学习许可"}${exp}`;
      els.statusBar.dataset.tone = "ok";
    } else if (studentLoginEnabled) {
      els.statusBar.textContent = "需要授权码登录后才能同步学习数据";
      els.statusBar.dataset.tone = "warn";
    } else {
      els.statusBar.classList.add("hidden");
    }
  }

  async function refreshStatus() {
    try {
      const res = await fetchAuth(apiUrl("/api/auth/status"), {
        cache: "no-store",
        headers: authHeaders(),
      });
      if (!res.ok) {
        unlockPage();
        return false;
      }
      const data = await res.json();
      authRequired = Boolean(data.authRequired);
      loggedIn = Boolean(data.loggedIn);
      isAdmin = Boolean(data.permanent) || data.role === "admin";
      studentLoginEnabled = Boolean(data.studentLoginEnabled);
      licenseLabel = data.licenseLabel || "";
      licenseExpiresAt = data.expiresAt || "";
      if (!loggedIn && getToken()) setToken("");
      applyAdminUi();
      applyAuthUserBar();
      applyStudentLoginUi();
      if (authRequired && !loggedIn) showGate();
      else hideGate();
      updateStatusBar();
      return loggedIn || !authRequired;
    } catch {
      authRequired = false;
      loggedIn = false;
      isAdmin = false;
      unlockPage();
      applyAdminUi();
      updateStatusBar();
      return true;
    }
  }

  async function loginWithAdminPassword(password) {
    const pwd = String(password || "");
    if (!pwd) throw new Error("请输入管理员密码");
    const res = await fetchAuth(apiUrl("/api/auth/login"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: pwd }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "登录失败");
    setToken(data.token || "");
    loggedIn = true;
    isAdmin = data.role === "admin";
    licenseLabel = data.licenseLabel || "";
    licenseExpiresAt = data.licenseExpiresAt || data.expiresAt || "";
    authRequired = true;
    applyAdminUi();
    applyAuthUserBar();
    applyStudentLoginUi();
    hideGate();
    updateStatusBar();
    return data;
  }

  async function login(code) {
    if (!studentLoginEnabled) {
      throw new Error("学生授权码登录未开放，请联系管理员");
    }
    const license = formatLicenseInput(code);
    if (!license || license.length < 10) {
      throw new Error("请输入完整授权码（格式 PEP6-XXXX-XXXX-XXXX）");
    }
    const res = await fetchAuth(apiUrl("/api/auth/login"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ license }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "登录失败");
    setToken(data.token || "");
    loggedIn = true;
    isAdmin = false;
    licenseLabel = data.licenseLabel || "";
    licenseExpiresAt = data.licenseExpiresAt || data.expiresAt || "";
    authRequired = true;
    applyAdminUi();
    applyAuthUserBar();
    applyStudentLoginUi();
    hideGate();
    updateStatusBar();
    return data;
  }

  function logout() {
    setToken("");
    loggedIn = false;
    isAdmin = false;
    applyAdminUi();
    applyAuthUserBar();
    applyStudentLoginUi();
    if (authRequired) showGate("已退出，请重新登录。");
    updateStatusBar();
  }

  async function ensureAuth() {
    const ok = await refreshStatus();
    if (!ok) {
      showGate();
      return false;
    }
    return true;
  }

  function bindUi() {
    els.gate = document.getElementById("authGate");
    els.password = document.getElementById("authPasswordInput");
    els.input = document.getElementById("authLicenseInput");
    els.submit = document.getElementById("authLoginBtn");
    els.logout = document.getElementById("authLogoutBtn");
    els.feedback = document.getElementById("authFeedback");
    els.statusBar = document.getElementById("authStatusBar");
    els.studentBlock = document.getElementById("authStudentLoginBlock");
    els.gateIntro = document.getElementById("authGateIntro");

    if (els.input) {
      els.input.addEventListener("input", () => {
        const pos = els.input.selectionStart;
        els.input.value = formatLicenseInput(els.input.value);
        try {
          els.input.setSelectionRange(pos, pos);
        } catch { /* ignore */ }
      });
      els.input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") els.submit?.click();
      });
    }
    if (els.password) {
      els.password.addEventListener("keydown", (e) => {
        if (e.key === "Enter") els.submit?.click();
      });
    }
    if (els.submit) {
      els.submit.addEventListener("click", async () => {
        els.submit.disabled = true;
        try {
          const license = (els.input?.value || "").trim();
          const adminPwd = (els.password?.value || "").trim();
          if (license && studentLoginEnabled) {
            await login(license);
          } else if (adminPwd) {
            await loginWithAdminPassword(adminPwd);
          } else if (license && !studentLoginEnabled) {
            throw new Error("学生授权码登录未开放，请联系管理员");
          } else {
            throw new Error("请输入管理员密码");
          }
          if (els.feedback) {
            els.feedback.textContent = "登录成功，可以开始学习与同步。";
            els.feedback.dataset.tone = "ok";
          }
          if (typeof window.onPep6AuthLogin === "function") window.onPep6AuthLogin();
        } catch (err) {
          if (els.feedback) {
            els.feedback.textContent = err.message || "登录失败";
            els.feedback.dataset.tone = "error";
          }
        } finally {
          els.submit.disabled = false;
        }
      });
    }
    if (els.logout) {
      els.logout.addEventListener("click", () => logout());
    }
  }

  async function init() {
    bindUi();
    try {
      await refreshStatus();
    } catch {
      unlockPage();
    }
  }

  window.Pep6Auth = {
    init,
    getToken,
    authHeaders,
    login,
    loginWithAdminPassword,
    logout,
    ensureAuth,
    refreshStatus,
    isAuthRequired,
    isLoggedIn,
    isAdmin: isAdminUser,
    isStudentLoginEnabled,
    formatLicenseInput,
  };
})();
