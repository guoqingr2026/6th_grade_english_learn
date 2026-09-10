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

  const els = {};

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

  function formatLicenseInput(value) {
    const raw = String(value || "").replace(/[^A-Za-z0-9]/g, "").toUpperCase();
    if (!raw) return "";
    const body = raw.startsWith("PEP6") ? raw.slice(4) : raw;
    const chunks = body.slice(0, 12).match(/.{1,4}/g) || [];
    return "PEP6-" + chunks.join("-");
  }

  function showGate(message) {
    if (!els.gate) return;
    els.gate.classList.remove("hidden");
    document.body.classList.add("auth-locked");
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
      const exp = isAdmin
        ? " · 永久有效"
        : licenseExpiresAt
          ? ` · 有效期至 ${licenseExpiresAt}`
          : "";
      els.statusBar.textContent = `已授权：${licenseLabel || "学习许可"}${exp}`;
      els.statusBar.dataset.tone = "ok";
    } else {
      els.statusBar.textContent = "需要授权码登录后才能同步学习数据";
      els.statusBar.dataset.tone = "warn";
    }
  }

  async function refreshStatus() {
    try {
      const res = await fetch(pep6Url("/api/auth/status"), {
        cache: "no-store",
        headers: authHeaders(),
      });
      if (!res.ok) return false;
      const data = await res.json();
      authRequired = Boolean(data.authRequired);
      loggedIn = Boolean(data.loggedIn);
      isAdmin = Boolean(data.permanent) || data.role === "admin";
      licenseLabel = data.licenseLabel || "";
      licenseExpiresAt = data.expiresAt || "";
      if (!loggedIn && getToken()) setToken("");
      if (authRequired && !loggedIn) showGate();
      else hideGate();
      updateStatusBar();
      return loggedIn || !authRequired;
    } catch {
      authRequired = false;
      loggedIn = false;
      hideGate();
      updateStatusBar();
      return true;
    }
  }

  async function loginWithAdminPassword(password) {
    const pwd = String(password || "");
    if (!pwd) throw new Error("请输入管理员密码");
    const res = await fetch(pep6Url("/api/auth/login"), {
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
    hideGate();
    updateStatusBar();
    return data;
  }

  async function login(code) {
    const license = formatLicenseInput(code);
    if (!license || license.length < 10) {
      throw new Error("请输入完整授权码（格式 PEP6-XXXX-XXXX-XXXX）");
    }
    const res = await fetch(pep6Url("/api/auth/login"), {
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
    hideGate();
    updateStatusBar();
    return data;
  }

  function logout() {
    setToken("");
    loggedIn = false;
    isAdmin = false;
    if (authRequired) showGate("已退出，请重新输入授权码。");
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

    if (els.input) {
      els.input.addEventListener("input", () => {
        const pos = els.input.selectionStart;
        els.input.value = formatLicenseInput(els.input.value);
      });
      els.input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") els.submit?.click();
      });
    }
    if (els.submit) {
      els.submit.addEventListener("click", async () => {
        els.submit.disabled = true;
        try {
          const license = (els.input?.value || "").trim();
          const adminPwd = (els.password?.value || "").trim();
          if (license) {
            await login(license);
          } else if (adminPwd) {
            await loginWithAdminPassword(adminPwd);
          } else {
            throw new Error("请输入学生授权码或管理员密码");
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
    await refreshStatus();
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
    formatLicenseInput,
  };
})();
