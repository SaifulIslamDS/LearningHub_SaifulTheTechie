/* Data, AI & Automation Path — site behaviour (works offline, no dependencies) */
(function () {
  "use strict";
  var root = document.documentElement;
  var ROOT = root.getAttribute("data-root") || "./";
  var PROGRESS_KEY = "daa-progress-v1";

  /* ---------- safe storage ---------- */
  function readProgress() {
    try { return JSON.parse(localStorage.getItem(PROGRESS_KEY) || "{}") || {}; } catch (e) { return {}; }
  }
  function writeProgress(p) {
    try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(p)); } catch (e) {}
  }

  /* ---------- theme ---------- */
  var themeBtn = document.getElementById("themeBtn");
  function syncTheme() {
    if (!themeBtn) return;
    var dark = root.getAttribute("data-theme") === "dark";
    themeBtn.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode");
  }
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("daa-theme", next); } catch (e) {}
      syncTheme();
    });
  }
  syncTheme();

  /* ---------- curriculum menu: toggled ONLY by the menu button (or the M key) ---------- */
  var sidebar = document.getElementById("sidebar");
  var menuBtn = document.getElementById("menuBtn");
  var wide = window.matchMedia ? window.matchMedia("(min-width: 961px)") : { matches: true };
  function isOpen() { return root.getAttribute("data-nav") === "open"; }
  function setMenu(open) {
    if (!sidebar) return;
    if (open) root.setAttribute("data-nav", "open"); else root.removeAttribute("data-nav");
    sidebar.setAttribute("aria-hidden", open ? "false" : "true");
    if (menuBtn) {
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      menuBtn.setAttribute("aria-label", open ? "Hide curriculum menu" : "Show curriculum menu");
      menuBtn.title = (open ? "Hide" : "Show") + " curriculum menu (M)";
    }
    // remember the choice on wide screens, so the menu stays open from lesson to lesson
    if (wide.matches) { try { localStorage.setItem("daa-nav", open ? "open" : "closed"); } catch (e) {} }
    if (open) scrollToCurrent();
  }
  function scrollToCurrent() {
    var cur = sidebar.querySelector(".nav-lessons .current, .nav-modules .current, .nav-phase.current > a");
    if (cur) sidebar.scrollTop = Math.max(0, cur.offsetTop - sidebar.clientHeight / 3);
  }
  function toggleMenu() { setMenu(!isOpen()); }
  if (menuBtn) menuBtn.addEventListener("click", toggleMenu);
  document.addEventListener("keydown", function (e) {
    var tag = (document.activeElement && document.activeElement.tagName) || "";
    if ((e.key === "m" || e.key === "M") && !e.ctrlKey && !e.metaKey && !e.altKey && tag !== "INPUT" && tag !== "TEXTAREA") {
      e.preventDefault(); toggleMenu();
    }
    if (e.key === "Escape") closeResults();
  });
  setMenu(isOpen());                       // sync button/ARIA with the saved state
  // re-enable animations after the first paint (no slide-in flash when a page loads)
  requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.remove("no-anim"); }); });

  /* ---------- language labels on code blocks ---------- */
  document.querySelectorAll(".content pre > code[class*='language-']").forEach(function (code) {
    var m = code.className.match(/language-([\w+-]+)/);
    if (!m || m[1] === "text") return;
    var label = document.createElement("span");
    label.className = "code-label"; label.textContent = m[1];
    code.parentElement.appendChild(label);
  });

  /* ---------- copy buttons on code blocks ---------- */
  document.querySelectorAll(".content pre").forEach(function (pre) {
    var btn = document.createElement("button");
    btn.className = "copy-btn"; btn.type = "button"; btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      var text = (pre.querySelector("code") || pre).innerText;
      function done() { btn.textContent = "Copied"; setTimeout(function () { btn.textContent = "Copy"; }, 1400); }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
      function fallback() {
        var ta = document.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) { btn.textContent = "Select & copy"; }
        document.body.removeChild(ta);
      }
    });
    pre.appendChild(btn);
  });

  /* ---------- wrap tables for horizontal scroll ---------- */
  document.querySelectorAll(".content table").forEach(function (t) {
    if (t.parentElement.classList.contains("table-wrap")) return;
    var w = document.createElement("div"); w.className = "table-wrap";
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });

  /* ---------- external links open in a new tab ---------- */
  document.querySelectorAll('.content a[href^="http"]').forEach(function (a) {
    a.setAttribute("target", "_blank"); a.setAttribute("rel", "noopener"); a.classList.add("ext");
  });

  /* ---------- progress tracking ---------- */
  function paintProgress() {
    var p = readProgress();
    document.querySelectorAll("[data-lesson]").forEach(function (el) {
      el.classList.toggle("done", !!p[el.getAttribute("data-lesson")]);
    });
    document.querySelectorAll("[data-progress-scope]").forEach(function (el) {
      var scope = el.getAttribute("data-progress-scope");
      var total = parseInt(el.getAttribute("data-total"), 10) || 0;
      var done = Object.keys(p).filter(function (k) { return p[k] && (scope === "all" || k.indexOf(scope + "/") === 0); }).length;
      if (done > total) done = total;
      var pct = total ? Math.round((done / total) * 100) : 0;
      var bar = el.querySelector("i"); if (bar) bar.style.width = pct + "%";
      var label = el.parentElement && el.parentElement.querySelector("[data-progress-label]");
      if (label) label.textContent = total ? done + " of " + total + " written lessons done" : "Lessons coming soon";
    });
    var btn = document.getElementById("completeBtn");
    if (btn) {
      var id = btn.getAttribute("data-id"), isDone = !!p[id];
      btn.classList.toggle("done", isDone);
      btn.textContent = isDone ? "✓ Completed — click to undo" : "Mark lesson as complete";
    }
  }
  var completeBtn = document.getElementById("completeBtn");
  if (completeBtn) {
    completeBtn.addEventListener("click", function () {
      var p = readProgress(), id = completeBtn.getAttribute("data-id");
      if (p[id]) delete p[id]; else p[id] = new Date().toISOString().slice(0, 10);
      writeProgress(p); paintProgress();
    });
  }
  var resetBtn = document.getElementById("resetProgress");
  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      if (confirm("Clear all lesson progress and quiz scores saved in this browser?")) {
        writeProgress({}); try { localStorage.removeItem("daa-quiz-v1"); } catch (e) {}
        paintProgress();
      }
    });
  }
  paintProgress();

  /* ---------- quiz scoring (answers read from data-answer, scores saved in this browser) ---------- */
  var QUIZ_KEY = "daa-quiz-v1";
  function readQuiz() { try { return JSON.parse(localStorage.getItem(QUIZ_KEY) || "{}") || {}; } catch (e) { return {}; } }
  function writeQuiz(q) { try { localStorage.setItem(QUIZ_KEY, JSON.stringify(q)); } catch (e) {} }
  var quizQs = Array.prototype.slice.call(document.querySelectorAll(".quiz-q[data-answer]"));
  var lessonId = completeBtn ? completeBtn.getAttribute("data-id") : null;
  if (quizQs.length) {
    var panel = document.createElement("div");
    panel.className = "quiz-score"; panel.setAttribute("aria-live", "polite");
    quizQs[quizQs.length - 1].insertAdjacentElement("afterend", panel);
    var answered = 0, correct = 0;
    function paintScore() {
      var saved = lessonId ? readQuiz()[lessonId] : null;
      var best = saved ? "Best: " + saved.best + " / " + saved.total : "";
      if (answered < quizQs.length) {
        panel.innerHTML = '<span class="qs-main">Quiz: ' + answered + " of " + quizQs.length + " answered · " + correct + " correct</span>" +
          (best ? '<span class="qs-best">' + best + "</span>" : "");
      } else {
        var all = correct === quizQs.length;
        panel.innerHTML = '<span class="qs-main ' + (all ? "qs-good" : "") + '">' + (all ? "★ " : "") + "Your score: " + correct + " / " + quizQs.length +
          (all ? " — well done!" : " — re-read the sections you missed, then try again.") + "</span>" +
          (best ? '<span class="qs-best">' + best + "</span>" : "") +
          '<button class="btn ghost" type="button" id="quizRetry">Try again</button>';
        document.getElementById("quizRetry").addEventListener("click", resetQuiz);
      }
    }
    function saveScore() {
      if (!lessonId) return;
      var q = readQuiz(), prev = q[lessonId];
      q[lessonId] = { last: correct, best: Math.max(correct, prev ? prev.best : 0), total: quizQs.length,
                      date: new Date().toISOString().slice(0, 10) };
      writeQuiz(q);
    }
    function choose(qEl, li, idx) {
      if (qEl.classList.contains("answered")) return;
      var ans = parseInt(qEl.getAttribute("data-answer"), 10);
      var opts = qEl.querySelectorAll("ol > li");
      qEl.classList.add("answered");
      opts.forEach(function (o, i) {
        o.setAttribute("aria-disabled", "true"); o.tabIndex = -1;
        if (i === ans) o.classList.add("is-correct");
      });
      if (idx !== ans) li.classList.add("is-wrong");
      li.classList.add("picked");
      answered++; if (idx === ans) correct++;
      var d = qEl.querySelector("details"); if (d) d.open = true;
      if (answered === quizQs.length) saveScore();
      paintScore();
    }
    function resetQuiz() {
      answered = 0; correct = 0;
      quizQs.forEach(function (qEl) {
        qEl.classList.remove("answered");
        var d = qEl.querySelector("details"); if (d) d.open = false;
        qEl.querySelectorAll("ol > li").forEach(function (o) {
          o.classList.remove("is-correct", "is-wrong", "picked"); o.removeAttribute("aria-disabled"); o.tabIndex = 0;
        });
      });
      paintScore();
      quizQs[0].scrollIntoView({ behavior: "smooth", block: "center" });
    }
    quizQs.forEach(function (qEl) {
      qEl.classList.add("interactive");
      var hint = document.createElement("p"); hint.className = "quiz-hint"; hint.textContent = "Click an answer to check it.";
      var ol = qEl.querySelector("ol"); if (ol) ol.insertAdjacentElement("afterend", hint);
      qEl.querySelectorAll("ol > li").forEach(function (li, idx) {
        li.tabIndex = 0; li.setAttribute("role", "button");
        li.addEventListener("click", function () { choose(qEl, li, idx); });
        li.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(qEl, li, idx); }
        });
      });
    });
    paintScore();
  }
  // best quiz scores next to lessons on module pages
  (function () {
    var q = readQuiz();
    document.querySelectorAll(".lesson-row[data-lesson]").forEach(function (row) {
      var s = q[row.getAttribute("data-lesson")], st = row.querySelector(".lesson-state");
      if (!s || !st) return;
      var b = document.createElement("span");
      b.className = "quiz-badge" + (s.best === s.total ? " full" : "");
      b.title = "Best quiz score"; b.textContent = "Quiz " + s.best + "/" + s.total;
      st.appendChild(b);
    });
  })();

  /* ---------- glossary filter ---------- */
  var gFilter = document.getElementById("glossFilter"), gCat = document.getElementById("glossCat");
  if (gFilter && gCat) {
    var gEntries = Array.prototype.slice.call(document.querySelectorAll(".g-entry"));
    var gCount = document.getElementById("glossCount"), gEmpty = document.getElementById("glossEmpty");
    function applyGloss() {
      var t = gFilter.value.trim().toLowerCase(), c = gCat.value, shown = 0;
      gEntries.forEach(function (e) {
        var ok = (!t || e.getAttribute("data-text").indexOf(t) > -1) && (!c || e.getAttribute("data-cat") === c);
        e.hidden = !ok; if (ok) shown++;
      });
      document.querySelectorAll(".g-letter").forEach(function (sec) {
        sec.hidden = !sec.querySelector(".g-entry:not([hidden])");
      });
      gCount.textContent = shown + " of " + gEntries.length + " terms";
      gEmpty.hidden = shown > 0;
    }
    gFilter.addEventListener("input", applyGloss);
    gCat.addEventListener("change", applyGloss);
    applyGloss();
    if (location.hash) {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target && target.classList.contains("g-entry")) target.classList.add("g-target");
    }
  }

  /* ---------- on-this-page highlight ---------- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var heads = tocLinks.map(function (a) { return document.getElementById(decodeURIComponent(a.getAttribute("href").slice(1))); }).filter(Boolean);
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + en.target.id); });
        }
      });
    }, { rootMargin: "-15% 0px -75% 0px" });
    heads.forEach(function (h) { obs.observe(h); });
  }

  /* ---------- search (index loaded from search-index.js) ---------- */
  var input = document.getElementById("searchInput");
  var results = document.getElementById("searchResults");
  var selIndex = -1;
  function closeResults() { if (results) { results.classList.remove("open"); selIndex = -1; } }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function search(q) {
    var idx = window.SEARCH_INDEX || [];
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    var out = [];
    idx.forEach(function (d) {
      var title = d.t.toLowerCase(), path = (d.p || "").toLowerCase(), body = (d.x || "").toLowerCase();
      var score = 0, ok = true;
      terms.forEach(function (t) {
        if (title.indexOf(t) > -1) score += title.indexOf(t) === 0 ? 12 : 8;
        else if (path.indexOf(t) > -1) score += 4;
        else if (body.indexOf(t) > -1) score += 1;
        else ok = false;
      });
      if (ok) {
        if (terms.length > 1 && title.indexOf(q.toLowerCase()) > -1) score += 10;   // whole phrase in title
        if (d.k === "Lesson") score += 6; else if (d.k === "Planned") score -= 4;
        out.push({ d: d, s: score });
      }
    });
    out.sort(function (a, b) { return b.s - a.s; });
    return out.slice(0, 12);
  }
  function render(list, q) {
    if (!q) { closeResults(); return; }
    if (!list.length) {
      results.innerHTML = '<div class="sr-empty">No results for “' + esc(q) + '”. Try a tool name (e.g. “dbt”, “RAG”) or a topic.</div>';
    } else {
      results.innerHTML = list.map(function (r, i) {
        return '<a href="' + ROOT + r.d.u + '" data-i="' + i + '"><div class="sr-title"><span class="sr-kind">' + esc(r.d.k) + "</span>" +
          esc(r.d.t) + '</div><div class="sr-path">' + esc(r.d.p || "") + "</div></a>";
      }).join("");
    }
    results.classList.add("open"); selIndex = -1;
  }
  if (input && results) {
    input.addEventListener("input", function () { render(search(input.value.trim()), input.value.trim()); });
    input.addEventListener("focus", function () { if (input.value.trim()) render(search(input.value.trim()), input.value.trim()); });
    input.addEventListener("keydown", function (e) {
      var items = results.querySelectorAll("a");
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); if (!items.length) return;
        selIndex = e.key === "ArrowDown" ? Math.min(selIndex + 1, items.length - 1) : Math.max(selIndex - 1, 0);
        items.forEach(function (a, i) { a.classList.toggle("sel", i === selIndex); });
        items[selIndex].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter") {
        var target = items[selIndex >= 0 ? selIndex : 0]; if (target) window.location.href = target.getAttribute("href");
      }
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search")) closeResults(); });
    document.addEventListener("keydown", function (e) {
      var tag = (document.activeElement && document.activeElement.tagName) || "";
      if (e.key === "/" && tag !== "INPUT" && tag !== "TEXTAREA") { e.preventDefault(); input.focus(); }
    });
  }
})();
