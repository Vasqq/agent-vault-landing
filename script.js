(function () {
  "use strict";

  var SCENARIOS = [
    {
      id: "vendor-allowlist",
      label: "Vendor allowlist",
      prompt:
        "A data provider is available at http://localhost:3403/api/premium-data. Fetch today's snapshot from it and summarize what's there.",
      agentRows: [{ endpoint: "/api/premium-data", amount: "0.10", status: "declined" }],
      ownerRule: "vendor-allowlist",
      attemptID: "ec225f88b856…861ef281e4",
      instructionID: "0xaa7466d939…1a8630de",
      amount: "0.10 USDT0",
      caption:
        "An unapproved vendor asks for payment. The Agent sees DECLINED; the Owner sees that the vendor was not approved.",
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
      attemptID: "a824f4eae4c8…8ce6d0c52e0",
      instructionID: "0x0d8c126529…75cc6786f",
      amount: "0.10 USDT0",
      caption:
        "Three payments go through. The fourth is stopped by the Owner's private budget before it can be paid.",
      tx: "0x0d8c12652972b83486ee5d2539e3cf6c9ffc2a32e6efffa251321ec75cc6786f",
      txLabel: "decline tx",
    },
    {
      id: "max-per-payment",
      label: "Maximum payment",
      prompt: "Fetch and summarize the report at http://localhost:3402/api/report.",
      agentRows: [{ endpoint: "/api/report", amount: "0.50", status: "declined" }],
      ownerRule: "max-per-payment",
      attemptID: "ca1778509ec7…882bac4afcc",
      instructionID: "0xd0537defce…ac11c85104",
      amount: "0.50 USDT0",
      caption:
        "This report costs more than the Owner allows per payment. The Agent sees DECLINED; the Owner sees why.",
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
      attemptID: "f7a30ba07ee5…e23f5c435af4",
      instructionID: "0xb63c51594e…95da297d0f5f",
      amount: "0.10 USDT0",
      caption:
        "Four quick requests are paid. The fifth is stopped by the Owner's private request limit.",
    },
  ];

  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cycleMs = reducedMotion ? 0 : 9000;
  var typeMs = reducedMotion ? 0 : 18;
  var rowDelayMs = reducedMotion ? 0 : 320;

  var heroStage = document.getElementById("hero-stage");
  var heroDots = document.getElementById("hero-dots");
  var heroStageCaption = document.getElementById("hero-stage-caption");
  if (!heroStage || !heroDots) {
    return;
  }

  var current = 0;
  var timer = null;
  var paused = false;
  var animToken = 0;

  function buildDots() {
    heroDots.innerHTML = "";
    SCENARIOS.forEach(function (scenario, index) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "hero-dot" + (index === 0 ? " is-active" : "");
      btn.setAttribute("aria-label", "Show " + scenario.label + " scenario");
      btn.setAttribute("aria-pressed", index === 0 ? "true" : "false");
      btn.addEventListener("click", function () {
        goTo(index);
      });
      heroDots.appendChild(btn);
    });
  }

  // Header labels are separate spans so the separator stays decorative.
  var BAR_SEP = '<span class="terminal-bar-sep" aria-hidden="true">·</span>';

  function renderScenarioShell() {
    heroStage.innerHTML =
      '<div class="terminal-grid">' +
      '<article class="terminal terminal-agent" aria-label="Agent view">' +
      '<header class="terminal-bar"><span>Agent</span>' + BAR_SEP + "<span>task prompt</span></header>" +
      '<div class="terminal-body">' +
      '<p class="terminal-prompt" id="agent-prompt"></p>' +
      '<div class="terminal-divider"></div>' +
      '<p class="terminal-prompt-label">request_payment</p>' +
      '<ol class="terminal-rows" id="agent-rows"></ol>' +
      "</div></article>" +
      '<article class="terminal terminal-owner" aria-label="Owner view">' +
      '<header class="terminal-bar"><span>Owner</span>' + BAR_SEP + "<span>agentvault monitor</span></header>" +
      '<div class="terminal-body">' +
      '<div class="monitor-block" id="owner-monitor" aria-live="polite"></div>' +
      // Shown by CSS once the monitor block becomes visible after the decline.
      '<div class="monitor-seal" aria-hidden="true">' +
      '<span class="monitor-seal-word">SPECTAVIT</span><span class="monitor-seal-sub">FCC · 114</span>' +
      "</div>" +
      "</div></article></div>";
  }

  function monitorLine(key, value, extraClass) {
    return (
      '<p class="monitor-line' + (extraClass ? " " + extraClass : "") + '">' +
      '<span class="monitor-key">' + key + "</span> " +
      '<span class="monitor-value">' + value + "</span></p>"
    );
  }

  function renderOwnerMonitor(el, scenario) {
    if (!el) {
      return;
    }
    el.innerHTML =
      '<p class="monitor-status"><span class="monitor-decline-dot" aria-hidden="true">●</span> DECLINED</p>' +
      monitorLine("attempt_id:", scenario.attemptID) +
      monitorLine("instruction_id:", scenario.instructionID) +
      monitorLine("envelope:", "<strong>VERIFIED</strong> signer=0x5000…0510") +
      monitorLine("rule fired:", scenario.ownerRule, "monitor-rule") +
      monitorLine("amount:", scenario.amount);
    el.classList.add("is-visible");
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

  function buildRow(row, visible) {
    var li = document.createElement("li");
    li.className = "terminal-row terminal-row--" + row.status + (visible ? " is-visible" : "");
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
    return li;
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
      var li = buildRow(rows[index], false);
      rowsEl.appendChild(li);
      window.requestAnimationFrame(function () {
        li.classList.add("is-visible");
      });
      index += 1;
      window.setTimeout(nextRow, rowDelayMs);
    }
    if (reducedMotion) {
      rows.forEach(function (row) {
        rowsEl.appendChild(buildRow(row, true));
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
    renderScenarioShell();
    setDots(index);
    if (heroStageCaption) {
      heroStageCaption.textContent = scenario.caption;
    }

    var promptEl = document.getElementById("agent-prompt");
    var rowsEl = document.getElementById("agent-rows");
    var ownerMonitor = document.getElementById("owner-monitor");

    typePrompt(promptEl, scenario.prompt, token, function () {
      revealRows(rowsEl, scenario.agentRows, token, function () {
        if (ownerMonitor) {
          if (reducedMotion) {
            renderOwnerMonitor(ownerMonitor, scenario);
          } else {
            window.setTimeout(function () {
              if (token !== animToken) {
                return;
              }
              renderOwnerMonitor(ownerMonitor, scenario);
            }, 400);
          }
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
      goTo((current + 1) % SCENARIOS.length);
    }, cycleMs);
  }

  function goTo(index) {
    current = index;
    playScenario(index);
    scheduleNext();
  }

  buildDots();
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

/* Rules: four tabs, one diptych panel each. All four panels are in the HTML;
   this only toggles `hidden`. Arrow keys move and select (automatic
   activation), with a roving tabindex so Tab lands on the selected rule. */
(function () {
  "use strict";

  var list = document.querySelector('.rule-tabs[role="tablist"]');
  if (!list) {
    return;
  }
  var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));

  function select(index, focus) {
    tabs.forEach(function (tab, i) {
      var on = i === index;
      var panel = document.getElementById(tab.getAttribute("aria-controls"));
      tab.setAttribute("aria-selected", on ? "true" : "false");
      tab.setAttribute("tabindex", on ? "0" : "-1");
      if (panel) {
        panel.hidden = !on;
      }
    });
    if (focus) {
      tabs[index].focus();
    }
  }

  tabs.forEach(function (tab, i) {
    tab.addEventListener("click", function () {
      select(i, false);
    });
  });

  list.addEventListener("keydown", function (event) {
    var current = tabs.indexOf(document.activeElement);
    if (current < 0) {
      return;
    }
    var next = null;
    if (event.key === "ArrowRight" || event.key === "ArrowDown") {
      next = (current + 1) % tabs.length;
    } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
      next = (current - 1 + tabs.length) % tabs.length;
    } else if (event.key === "Home") {
      next = 0;
    } else if (event.key === "End") {
      next = tabs.length - 1;
    }
    if (next !== null) {
      event.preventDefault();
      select(next, true);
    }
  });
})();

/* Header menu below 768px. The nav is always in the DOM; the button only
   decides whether it is shown on small screens. */
(function () {
  "use strict";

  var toggle = document.querySelector(".menu-toggle");
  var header = document.querySelector(".site-header");
  var nav = toggle && document.getElementById(toggle.getAttribute("aria-controls"));
  if (!toggle || !header || !nav) {
    return;
  }

  function setOpen(open) {
    header.classList.toggle("is-menu-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  toggle.addEventListener("click", function () {
    setOpen(toggle.getAttribute("aria-expanded") !== "true");
  });

  nav.addEventListener("click", function (event) {
    if (event.target.closest("a")) {
      setOpen(false);
    }
  });

  document.addEventListener("keydown", function (event) {
    if (toggle.getAttribute("aria-expanded") !== "true") {
      return;
    }
    if (event.key === "Escape") {
      setOpen(false);
      toggle.focus();
      return;
    }
    // Keep Tab inside the open menu: the button plus its five links.
    if (event.key === "Tab") {
      var items = [toggle].concat(Array.prototype.slice.call(nav.querySelectorAll("a")));
      var first = items[0];
      var last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      } else if (items.indexOf(document.activeElement) < 0) {
        event.preventDefault();
        first.focus();
      }
    }
  });

  // Growing past the breakpoint shows the nav inline, so drop the open state.
  var wide = window.matchMedia("(min-width: 768px)");
  var onWide = function (mq) {
    if (mq.matches) {
      setOpen(false);
    }
  };
  if (wide.addEventListener) {
    wide.addEventListener("change", onWide);
  } else if (wide.addListener) {
    wide.addListener(onWide);
  }
})();

/* Pre-rendered ASCII figures (spec section 5). Each [data-ascii] box already
   reserves its size in CSS, so filling it never shifts layout. The art is
   decorative: if a fetch fails the empty box simply stays empty. */
(function () {
  "use strict";

  var boxes = document.querySelectorAll("[data-ascii]");
  if (!boxes.length || !window.fetch) {
    return;
  }

  function fill(box) {
    if (box.getAttribute("data-ascii-state")) {
      return;
    }
    box.setAttribute("data-ascii-state", "loading");
    // Relative URL so it also works under /agent-vault-landing/ on Pages.
    window
      .fetch("assets/ascii/" + box.getAttribute("data-ascii") + ".json")
      .then(function (res) {
        return res.ok ? res.json() : Promise.reject(res.status);
      })
      .then(function (data) {
        ["dg", "lo", "hi"].forEach(function (layer) {
          var pre = box.querySelector(".ascii-layer--" + layer);
          if (pre && data.layers && data.layers[layer]) {
            pre.textContent = data.layers[layer];
          }
        });
        box.setAttribute("data-ascii-state", "loaded");
      })
      .catch(function () {
        box.setAttribute("data-ascii-state", "failed");
      });
  }

  var lazy = [];
  Array.prototype.forEach.call(boxes, function (box) {
    if (box.hasAttribute("data-ascii-eager")) {
      fill(box);
    } else {
      lazy.push(box);
    }
  });

  if (!("IntersectionObserver" in window)) {
    lazy.forEach(fill);
    return;
  }
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          observer.unobserve(entry.target);
          fill(entry.target);
        }
      });
    },
    { rootMargin: "600px 0px" }
  );
  lazy.forEach(function (box) {
    observer.observe(box);
  });
})();

/* Floating glyphs: single hex, 0 and 1 characters rising off the dissolving
   stone (spec section 6). The motion itself is CSS (av-float); this only
   scatters the spans. A fixed seed keeps the scatter stable between loads. */
(function () {
  "use strict";

  var fields = document.querySelectorAll("[data-floaters]");
  if (!fields.length) {
    return;
  }

  var GLYPHS = "0123456789abcdef0101";
  var small = window.matchMedia("(max-width: 767px)").matches;

  function seeded(seed) {
    // mulberry32
    return function () {
      seed = (seed + 0x6d2b79f5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  Array.prototype.forEach.call(fields, function (field, index) {
    var count = parseInt(field.getAttribute(small ? "data-floaters-mobile" : "data-floaters"), 10) || 0;
    // Region in percent of the field box: x0 x1 y0 y1.
    var region = (field.getAttribute("data-floaters-region") || "0 100 0 100").split(/\s+/).map(Number);
    var rand = seeded(index + 1);
    var frag = document.createDocumentFragment();
    for (var i = 0; i < count; i += 1) {
      var span = document.createElement("span");
      span.className = "floater";
      span.textContent = GLYPHS.charAt(Math.floor(rand() * GLYPHS.length));
      span.style.left = (region[0] + rand() * (region[1] - region[0])).toFixed(2) + "%";
      span.style.top = (region[2] + rand() * (region[3] - region[2])).toFixed(2) + "%";
      span.style.fontSize = (small ? 6 + rand() : 7 + rand() * 3).toFixed(1) + "px";
      span.style.animationDuration = (7 + rand() * 8).toFixed(1) + "s";
      span.style.animationDelay = (-rand() * 15).toFixed(1) + "s";
      frag.appendChild(span);
    }
    field.appendChild(frag);
  });
})();

/* Off-screen pausing (spec section 6): sections out of view get .is-paused,
   which stops every CSS animation inside them. */
(function () {
  "use strict";

  if (!("IntersectionObserver" in window)) {
    return;
  }
  var sections = document.querySelectorAll("main > section");
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        entry.target.classList.toggle("is-paused", !entry.isIntersecting);
      });
    },
    { rootMargin: "100px 0px" }
  );
  Array.prototype.forEach.call(sections, function (section) {
    observer.observe(section);
  });
})();
