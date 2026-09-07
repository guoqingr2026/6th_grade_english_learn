/**
 * 冲满分一体化：每日复习 · Part 通关 · 考前模拟
 */
(function masteryModule() {
  const MASTERY_KEY = "english_grade6_mastery_v1";
  const NOTES_KEY = "study_hub_notes_v1";
  const PART_CHAIN = ["unit-start", "unit-next", "part-a", "part-b", "part-c", "reading"];
  const UNLOCK_THRESHOLD = 0.8;

  let quizPool = [];

  function loadProgress() {
    try {
      return JSON.parse(localStorage.getItem(MASTERY_KEY) || "{}");
    } catch {
      return {};
    }
  }

  function saveProgress(data) {
    localStorage.setItem(MASTERY_KEY, JSON.stringify(data));
    if (typeof touchDataUpdatedAt === "function") touchDataUpdatedAt();
  }

  function partId(unit, part) {
    return `u${unit}-${part}`;
  }

  function isPartUnlocked(unit, part) {
    if (part === "part-a") return true;
    const idx = PART_CHAIN.indexOf(part);
    if (idx <= 0) return true;
    const prev = PART_CHAIN[idx - 1];
    const prog = loadProgress();
    return !!prog[partId(unit, prev)]?.passed;
  }

  function markPartPassed(unit, part, score, total) {
    const prog = loadProgress();
    prog[partId(unit, part)] = {
      passed: score / total >= UNLOCK_THRESHOLD,
      score,
      total,
      at: new Date().toISOString(),
    };
    saveProgress(prog);
    return prog[partId(unit, part)].passed;
  }

  function getStudyNotes() {
    try {
      return JSON.parse(localStorage.getItem(NOTES_KEY) || "{}");
    } catch {
      return {};
    }
  }

  function setStudyNotes(notes) {
    localStorage.setItem(NOTES_KEY, JSON.stringify(notes || {}));
    if (typeof touchDataUpdatedAt === "function") touchDataUpdatedAt();
  }

  function getMasteryExport() {
    return { progress: loadProgress(), updatedAt: new Date().toISOString() };
  }

  function applyMasteryImport(data) {
    if (data?.progress) saveProgress(data.progress);
  }

  window.MasteryHub = {
    loadProgress,
    saveProgress,
    isPartUnlocked,
    markPartPassed,
    getStudyNotes,
    setStudyNotes,
    getMasteryExport,
    applyMasteryImport,
    PART_CHAIN,
  };

  window.StudyHubExport = {
    getNotes: getStudyNotes,
    setNotes: setStudyNotes,
  };

  async function loadQuizzes() {
    if (quizPool.length) return quizPool;
    const res = await fetch("data/question-banks/quiz-bank.json");
    const data = await res.json();
    quizPool = Array.isArray(data.questions) ? data.questions : [];
    return quizPool;
  }

  function getWrongBookItems() {
    try {
      const raw = localStorage.getItem("english_grade6_wrong_items_v1");
      return raw ? JSON.parse(raw) : [];
    } catch {
      return [];
    }
  }

  function currentPartSuggestion() {
    const prog = loadProgress();
    for (let u = 1; u <= 6; u += 1) {
      for (const part of PART_CHAIN) {
        if (!prog[partId(u, part)]?.passed) {
          return { unit: u, part, label: `Unit ${u} · ${part}` };
        }
      }
    }
    return { unit: 6, part: "reading", label: "全部 Part 已通关，建议考前模拟" };
  }

  function renderDailyReview() {
    const box = document.getElementById("masteryDailyContent");
    if (!box) return;
    const wrong = getWrongBookItems();
    const suggest = currentPartSuggestion();
    const lines = wrong.slice(0, 8).map((w) => `<li>${w.module || "错题"}：${w.prompt || w.title || w.id}</li>`);
    box.innerHTML = `
      <p><strong>今日建议（约 20 分钟）：</strong></p>
      <ol>
        <li>打开「课文中英文讲读」→ ${suggest.label}（5 分钟）</li>
        <li>「知识点精讲」同 Part（5 分钟）</li>
        <li>错题本复习 ${wrong.length} 条（5 分钟）</li>
        <li>Part 通关测验（5 分钟）</li>
      </ol>
      <p><strong>错题快览：</strong></p>
      <ul>${lines.length ? lines.join("") : "<li>暂无错题，继续保持！</li>"}</ul>`;
  }

  function filterQuizzesByPart(unit, part) {
    const partLetter = part === "reading" ? null : part.replace("part-", "").toUpperCase();
    return quizPool.filter((q) => {
      if (Number(q.unit) !== unit) return false;
      if (!partLetter) return true;
      return String(q.part || "A").toUpperCase() === partLetter;
    });
  }

  function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  async function runPartQuiz() {
    await loadQuizzes();
    const u = Number(document.getElementById("masteryUnitSelect")?.value || 1);
    const part = document.getElementById("masteryPartSelect")?.value || "part-a";
    if (!isPartUnlocked(u, part)) {
      window.alert(`请先通关上一 Part（需 ≥${UNLOCK_THRESHOLD * 100}% 正确率）。`);
      return;
    }
    let pool = filterQuizzesByPart(u, part);
    if (pool.length < 3) pool = quizPool.filter((q) => Number(q.unit) === u);
    if (pool.length < 3) pool = quizPool;
    const set = shuffle(pool).slice(0, Math.min(10, pool.length));
    let correct = 0;
    set.forEach((q, i) => {
      const opts = (q.options || []).map((o, j) => `${j + 1}. ${o}`).join("\n");
      const ans = window.prompt(`[${i + 1}/${set.length}] ${q.prompt}\n\n${opts}\n\n输入正确选项全文：`);
      if (ans && ans.trim() === q.answer) correct += 1;
    });
    const passed = markPartPassed(u, part, correct, set.length);
    const msg = `得分 ${correct}/${set.length}（${Math.round((correct / set.length) * 100)}%）\n${passed ? "恭喜通关！已解锁下一 Part。" : "未达 80%，请复习后重试。"}`;
    window.alert(msg);
    renderDailyReview();
  }

  async function runMockExam() {
    await loadQuizzes();
    const set = shuffle(quizPool).slice(0, Math.min(20, quizPool.length));
    const start = Date.now();
    let correct = 0;
    const details = [];
    set.forEach((q, i) => {
      const opts = (q.options || []).map((o, j) => `${j + 1}. ${o}`).join("\n");
      const ans = window.prompt(`【模拟 ${i + 1}/${set.length}】Unit ${q.unit} ${q.prompt}\n\n${opts}\n\n输入答案：`);
      const ok = ans && ans.trim() === q.answer;
      if (ok) correct += 1;
      details.push({ unit: q.unit, prompt: q.prompt, ok, answer: q.answer });
    });
    const mins = ((Date.now() - start) / 60000).toFixed(1);
    const pct = Math.round((correct / set.length) * 100);
    const nick = JSON.parse(localStorage.getItem("english_grade6_profile_v1") || "{}").nickname || "同学";
    const html = `<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8"/><title>模拟考成绩</title>
<style>body{font-family:Arial,sans-serif;padding:24px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:8px}</style></head>
<body><h1>六年级英语模拟考成绩单</h1><p>姓名：${nick} · 用时 ${mins} 分钟 · 得分 ${correct}/${set.length}（${pct}%）</p>
<table><tr><th>单元</th><th>题目</th><th>结果</th><th>答案</th></tr>
${details.map((d) => `<tr><td>U${d.unit}</td><td>${d.prompt}</td><td>${d.ok ? "✓" : "✗"}</td><td>${d.answer}</td></tr>`).join("")}
</table></body></html>`;
    const blob = new Blob([html], { type: "text/html;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `mock-exam-${new Date().toISOString().slice(0, 10)}.html`;
    a.click();
    URL.revokeObjectURL(a.href);
    window.alert(`模拟考结束：${correct}/${set.length}（${pct}%），成绩单已下载。`);
  }

  function bindMastery() {
    document.getElementById("masteryDailyBtn")?.addEventListener("click", () => {
      renderDailyReview();
      document.getElementById("masteryPanel")?.classList.remove("hidden");
    });
    document.getElementById("masteryPartQuizBtn")?.addEventListener("click", runPartQuiz);
    document.getElementById("masteryMockExamBtn")?.addEventListener("click", runMockExam);
    document.getElementById("masteryCloseBtn")?.addEventListener("click", () => {
      document.getElementById("masteryPanel")?.classList.add("hidden");
    });
    renderDailyReview();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindMastery);
  } else {
    bindMastery();
  }
})();
