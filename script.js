(function () {
  "use strict";

  var EXPLORER_TX = "https://coston2-explorer.flare.network/tx/";
  var EXPLORER_ADDR = "https://coston2-explorer.flare.network/address/";

  var SCENARIOS = [
    {
      id: "vendor-allowlist",
      label: "Vendor allowlist",
      prompt:
        "A data provider is available at http://localhost:3403/api/premium-data. Fetch today's snapshot from it and summarize what's there.",
      agentRows: [{ endpoint: "/api/premium-data", amount: "0.10", status: "declined" }],
      ownerRule: "vendor-allowlist",
    },
    {
      id: "budget-window",
      label: "Rolling budget window",
      prompt:
        "Check the data feed at http://localhost:3402/api/premium-data. Make four fetch attempts to this exact URL, one after another, then tell me what changed between the successful snapshots.",
      agentRows: [
        { endpoint: "/api/premium-data", amount: "0.10", status: "paid" },
        { endpoint: "/api/premium-data", amount: "0.10", status: "paid" },
        { endpoint: "/api/premium-data", amount: "0.10", status: "paid" },
        { endpoint: "/api/premium-data", amount: "0.10", status: "declined" },
      ],
      ownerRule: "budget-window",
      tx: "0x0d8c12652972b83486ee5d2539e3cf6c9ffc2a32e6efffa251321ec75cc6786f",
      txLabel: "decline tx",
    },
    {
      id: "max-per-payment",
      label: "Maximum payment",
      prompt: "Fetch and summarize the report at http://localhost:3402/api/report.",
      agentRows: [{ endpoint: "/api/report", amount: "0.50", status: "declined" }],
      ownerRule: "max-per-payment",
    },
    {
      id: "rate-limit",
      label: "Rate limit",
      prompt:
        "Pull the data feed at http://localhost:3402/api/premium-data. Make five fetch attempts to this exact URL in immediate succession, with no pause between them.",
      agentRows: [
        { endpoint: "/api/premium-data", amount: "0.10", status: "paid" },
        { endpoint: "/api/premium-data", amount: "0.10", status: "paid" },
        { endpoint: "/api/premium-data", amount: "0.10", status: "paid" },
        { endpoint: "/api/premium-data", amount: "0.10", status: "paid" },
        { endpoint: "/api/premium-data", amount: "0.10", status: "declined" },
      ],
      ownerRule: "rate-limit",
    },
  ];

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cycleMs = reducedMotion ? 0 : 9000;
  var typeMs = reducedMotion ? 0 : 18;
  var rowDelayMs = reducedMotion ? 0 : 320;

  var heroStage = document.getElementById("hero-stage");
  var heroDots = document.getElementById("hero-dots");
  var mobileTabs = document.getElementById("mobile-pane-tabs");
  if (!heroStage || !heroDots) {
    return;
  }

  var current = 0;
  var timer = null;
  var paused = false;
  var animToken = 0;

  function shortHash(hash) {
    return hash.slice(0, 8) + "…" + hash.slice(-6);
  }

  function buildDots() {
    heroDots.innerHTML = "";
    SCENARIOS.forEach(function (scenario, index) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "hero-dot" + (index === 0 ? " is-active" : "");
      btn.setAttribute("aria-label", "Show " + scenario.label + " scenario");
      btn.setAttribute("aria-pressed", index === 0 ? "true" : "false");
      btn.addEventListener("click", function () {
        goTo(index, true);
      });
      heroDots.appendChild(btn);
    });
  }

  function buildMobileTabs() {
    if (!mobileTabs) {
      return;
    }
    mobileTabs.innerHTML = "";
    ["Agent view", "Owner view"].forEach(function (label, index) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "pane-tab" + (index === 0 ? " is-active" : "");
      btn.textContent = label;
      btn.setAttribute("aria-pressed", index === 0 ? "true" : "false");
      btn.addEventListener("click", function () {
        mobileTabs.querySelectorAll(".pane-tab").forEach(function (el, i) {
          el.classList.toggle("is-active", i === index);
          el.setAttribute("aria-pressed", i === index ? "true" : "false");
        });
        heroStage.classList.toggle("show-owner", index === 1);
      });
      mobileTabs.appendChild(btn);
    });
  }

  function renderScenarioShell(scenario) {
    heroStage.innerHTML =
      '<div class="terminal-grid">' +
      '<article class="terminal terminal-agent" aria-label="Agent view">' +
      '<header class="terminal-bar"><span>agent · task</span></header>' +
      '<div class="terminal-body">' +
      '<p class="terminal-prompt-label">task prompt</p>' +
      '<p class="terminal-prompt" id="agent-prompt"></p>' +
      '<div class="terminal-divider"></div>' +
      '<p class="terminal-prompt-label">request_payment</p>' +
      '<ol class="terminal-rows" id="agent-rows"></ol>' +
      '<p class="terminal-agent-note" id="agent-note" hidden>Agent sees no rule name, budget, or counter.</p>' +
      "</div></article>" +
      '<article class="terminal terminal-owner" aria-label="Owner view">' +
      '<header class="terminal-bar"><span>owner · monitor</span></header>' +
      '<div class="terminal-body">' +
      '<p class="terminal-prompt-label">ActionResult · verified</p>' +
      '<dl class="owner-meta">' +
      "<dt>machine</dt><dd>0x5000…0510 · PRODUCTION</dd>" +
      "<dt>signature</dt><dd>native FCC envelope ✓</dd>" +
      "</dl>" +
      '<div class="terminal-divider"></div>' +
      '<p class="terminal-prompt-label">owner-monitor decrypt</p>' +
      '<p class="owner-reveal" id="owner-reveal" aria-live="polite"></p>' +
      '<p class="owner-tx"><a id="owner-tx-link" href="#" rel="noopener noreferrer"></a></p>' +
      "</div></article></div>";
  }

  function setDots(index) {
    heroDots.querySelectorAll(".hero-dot").forEach(function (dot, i) {
      dot.classList.toggle("is-active", i === index);
      dot.setAttribute("aria-pressed", i === index ? "true" : "false");
    });
  }

  function typePrompt(el, text, token, done) {
    if (!el) {
      done();
      return;
    }
    el.textContent = "";
    if (reducedMotion || typeMs === 0) {
      el.textContent = text;
      done();
      return;
    }
    var i = 0;
    function step() {
      if (token !== animToken) {
        return;
      }
      el.textContent = text.slice(0, i);
      i += 1;
      if (i <= text.length) {
        window.setTimeout(step, typeMs);
      } else {
        done();
      }
    }
    step();
  }

  function revealRows(rowsEl, rows, token, done) {
    if (!rowsEl) {
      done();
      return;
    }
    rowsEl.innerHTML = "";
    var index = 0;
    function nextRow() {
      if (token !== animToken) {
        return;
      }
      if (index >= rows.length) {
        done();
        return;
      }
      var row = rows[index];
      var li = document.createElement("li");
      li.className = "terminal-row terminal-row--" + row.status;
      li.innerHTML =
        '<span class="terminal-row-endpoint">' +
        row.endpoint +
        "</span>" +
        '<span class="terminal-row-amount">' +
        row.amount +
        "</span>" +
        '<span class="terminal-row-status">' +
        (row.status === "paid" ? "PAID" : "DECLINED") +
        "</span>";
      rowsEl.appendChild(li);
      window.requestAnimationFrame(function () {
        li.classList.add("is-visible");
      });
      index += 1;
      window.setTimeout(nextRow, rowDelayMs);
    }
    if (reducedMotion) {
      rows.forEach(function (row) {
        var li = document.createElement("li");
        li.className = "terminal-row terminal-row--" + row.status + " is-visible";
        li.innerHTML =
          '<span class="terminal-row-endpoint">' +
          row.endpoint +
          "</span>" +
          '<span class="terminal-row-amount">' +
          row.amount +
          "</span>" +
          '<span class="terminal-row-status">' +
          (row.status === "paid" ? "PAID" : "DECLINED") +
          "</span>";
        rowsEl.appendChild(li);
      });
      done();
      return;
    }
    nextRow();
  }

  function playScenario(index) {
    animToken += 1;
    var token = animToken;
    var scenario = SCENARIOS[index];
    renderScenarioShell(scenario);
    setDots(index);

    var promptEl = document.getElementById("agent-prompt");
    var rowsEl = document.getElementById("agent-rows");
    var noteEl = document.getElementById("agent-note");
    var revealEl = document.getElementById("owner-reveal");
    var txLink = document.getElementById("owner-tx-link");

    if (revealEl) {
      revealEl.textContent = "";
      revealEl.classList.remove("is-revealed");
    }
    if (txLink) {
      txLink.textContent = "";
      txLink.removeAttribute("href");
    }

    typePrompt(promptEl, scenario.prompt, token, function () {
      revealRows(rowsEl, scenario.agentRows, token, function () {
        if (noteEl) {
          noteEl.hidden = false;
        }
        if (revealEl) {
          if (reducedMotion) {
            revealEl.textContent = 'failedRuleIds=["' + scenario.ownerRule + '"]';
            revealEl.classList.add("is-revealed");
          } else {
            window.setTimeout(function () {
              if (token !== animToken) {
                return;
              }
              revealEl.textContent = 'failedRuleIds=["' + scenario.ownerRule + '"]';
              revealEl.classList.add("is-revealed");
            }, 400);
          }
        }
        if (txLink && scenario.tx) {
          txLink.href = EXPLORER_TX + scenario.tx;
          txLink.textContent = scenario.txLabel + " · " + shortHash(scenario.tx);
        }
      });
    });
  }

  function scheduleNext() {
    if (timer) {
      window.clearTimeout(timer);
    }
    if (reducedMotion || cycleMs === 0 || paused) {
      return;
    }
    timer = window.setTimeout(function () {
      goTo((current + 1) % SCENARIOS.length, false);
    }, cycleMs);
  }

  function goTo(index, userInitiated) {
    current = index;
    playScenario(index);
    if (userInitiated) {
      scheduleNext();
    } else {
      scheduleNext();
    }
  }

  buildDots();
  buildMobileTabs();
  playScenario(0);
  scheduleNext();

  heroStage.addEventListener("mouseenter", function () {
    paused = true;
    if (timer) {
      window.clearTimeout(timer);
    }
  });

  heroStage.addEventListener("mouseleave", function () {
    paused = false;
    scheduleNext();
  });

  heroStage.addEventListener("focusin", function () {
    paused = true;
    if (timer) {
      window.clearTimeout(timer);
    }
  });

  heroStage.addEventListener("focusout", function () {
    paused = false;
    scheduleNext();
  });

  var sections = document.querySelectorAll(".section[data-reveal]");
  if (!reducedMotion && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-revealed");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    sections.forEach(function (section) {
      observer.observe(section);
    });
  } else {
    sections.forEach(function (section) {
      section.classList.add("is-revealed");
    });
  }
})();
