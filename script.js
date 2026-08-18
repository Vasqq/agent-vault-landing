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
  var mobileTabs = document.getElementById("mobile-pane-tabs");
  var asciiField = document.querySelector(".ascii-field");
  if (!heroStage || !heroDots) {
    return;
  }

  // Mirror each policy decision on the vault's locking-bolt ring.
  var vaultTimer = null;
  var DECLINE_MS = 3100; // matches the bolt-decline keyframe duration

  function setVaultState(state) {
    if (!asciiField) {
      return;
    }
    if (vaultTimer) {
      window.clearTimeout(vaultTimer);
      vaultTimer = null;
    }
    asciiField.classList.remove("is-paid", "is-declined");
    if (!state) {
      return;
    }
    // Force a reflow so repeating the same state replays the pulse
    // instead of the class re-add being a no-op.
    void asciiField.offsetWidth;
    asciiField.classList.add("is-" + state);

    // A decline halts the door and flashes red. Once the flash finishes,
    // release it so the vault starts turning again instead of sitting dead
    // until the next scenario. Reduced motion keeps the static red.
    if (state === "declined" && !reducedMotion) {
      vaultTimer = window.setTimeout(function () {
        asciiField.classList.remove("is-declined");
        vaultTimer = null;
      }, DECLINE_MS);
    }
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
      '<header class="terminal-bar"><span>Agent</span></header>' +
      '<div class="terminal-body">' +
      '<p class="terminal-prompt-label">task prompt</p>' +
      '<p class="terminal-prompt" id="agent-prompt"></p>' +
      '<div class="terminal-divider"></div>' +
      '<p class="terminal-prompt-label">request_payment</p>' +
      '<ol class="terminal-rows" id="agent-rows"></ol>' +
      "</div></article>" +
      '<article class="terminal terminal-owner" aria-label="Owner view">' +
      '<header class="terminal-bar"><span>Owner</span></header>' +
      '<div class="terminal-body">' +
      '<p class="terminal-prompt-label">agentvault monitor</p>' +
      '<div class="monitor-block" id="owner-monitor" aria-live="polite"></div>' +
      "</div></article></div>";
  }

  function renderOwnerMonitor(el, scenario) {
    if (!el) {
      return;
    }
    el.innerHTML =
      '<p class="monitor-status"><span class="monitor-decline-dot" aria-hidden="true">●</span> DECLINED</p>' +
      '<p class="monitor-line">attempt_id:     ' + scenario.attemptID + "</p>" +
      '<p class="monitor-line">instruction_id: ' + scenario.instructionID + "</p>" +
      '<p class="monitor-line">envelope: <strong>VERIFIED</strong> signer=0x5000…0510</p>' +
      '<p class="monitor-line monitor-rule">rule fired: ' + scenario.ownerRule + "</p>" +
      '<p class="monitor-line">amount: ' + scenario.amount + "</p>";
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
      setVaultState(row.status === "paid" ? "paid" : "declined");
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
      if (rows.length) {
        setVaultState(rows[rows.length - 1].status === "paid" ? "paid" : "declined");
      }
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
    setVaultState(null);
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

/* Rules section: decrypt transition between the Agent's blind view and the
   Owner's. The whole Owner pane arrives as ciphertext and resolves top to
   bottom, with the text transformation itself carrying the reveal. */
(function () {
  "use strict";

  var cards = document.querySelectorAll(".rule-card");
  if (!cards.length) {
    return;
  }

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  // The incoming pane is visibility:hidden until the fade completes, and a
  // hidden element cannot take focus, so the handoff waits for the swap.
  var SWAP_MS = reduce ? 0 : 320;
  // No positional stagger: a top-to-bottom delay makes the boundary between
  // resolved and unresolved text read as a moving line. Each node gets a small
  // random offset instead, and characters within it resolve in random order.
  var JITTER_MS = 170;
  var RESOLVE_MS = 880;
  var GLYPHS = "0123456789abcdef0123456789ABCDEF#$%&*+=?@^~";

  // Originals are captured once per pane. Without this, re-opening mid-flight
  // would latch ciphertext as the new "plaintext".
  var store = new WeakMap();

  function textNodes(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var out = [];
    var node = walker.nextNode();
    while (node) {
      if (node.nodeValue && node.nodeValue.trim().length) {
        out.push(node);
      }
      node = walker.nextNode();
    }
    return out;
  }

  function cipher(text, thresholds, p) {
    if (p >= 1) {
      return text;
    }
    var out = "";
    for (var i = 0; i < text.length; i += 1) {
      var ch = text.charAt(i);
      // Each character has its own reveal point, so plaintext surfaces all
      // over the line at once. Spacing is preserved so nothing reflows.
      if (ch === " " || ch === "\n" || (p > 0 && thresholds[i] < p)) {
        out += ch;
      } else {
        out += GLYPHS.charAt(Math.floor(Math.random() * GLYPHS.length));
      }
    }
    return out;
  }

  function decrypt(pane) {
    if (reduce || !pane) {
      return;
    }
    var state = store.get(pane);
    if (state) {
      if (state.raf) {
        window.cancelAnimationFrame(state.raf);
      }
      // Restore plaintext before measuring so positions are never taken
      // from a half-scrambled pane.
      state.items.forEach(function (it) {
        it.node.nodeValue = it.final;
      });
    } else {
      state = { items: null, raf: 0 };
      store.set(pane, state);
    }

    state.items = textNodes(pane).map(function (node) {
      var final = node.nodeValue;
      var thresholds = new Array(final.length);
      for (var i = 0; i < final.length; i += 1) {
        thresholds[i] = Math.random();
      }
      return {
        node: node,
        final: final,
        thresholds: thresholds,
        delay: Math.random() * JITTER_MS,
      };
    });

    var items = state.items;
    items.forEach(function (it) {
      it.node.nodeValue = cipher(it.final, it.thresholds, 0);
    });

    var started = null;
    function tick(now) {
      if (started === null) {
        started = now;
      }
      var t = now - started;
      var done = true;
      for (var i = 0; i < items.length; i += 1) {
        var it = items[i];
        var p = (t - it.delay) / RESOLVE_MS;
        if (p < 1) {
          done = false;
        }
        it.node.nodeValue = cipher(it.final, it.thresholds, p);
      }
      if (done) {
        state.raf = 0;
        return;
      }
      state.raf = window.requestAnimationFrame(tick);
    }
    state.raf = window.requestAnimationFrame(tick);
  }

  Array.prototype.forEach.call(cards, function (card) {
    var turns = card.querySelectorAll(".rule-turn");
    var owner = card.querySelector(".rule-face--owner");
    var armed = true;

    function run() {
      if (!armed) {
        return;
      }
      armed = false;
      decrypt(owner);
      window.setTimeout(function () {
        armed = true;
      }, JITTER_MS + RESOLVE_MS);
    }

    // Pointer devices open via CSS :hover; mirror the decrypt here.
    card.addEventListener("mouseenter", run);

    Array.prototype.forEach.call(turns, function (btn) {
      btn.addEventListener("click", function () {
        var open = card.classList.toggle("is-open");

        Array.prototype.forEach.call(turns, function (other) {
          other.setAttribute("aria-expanded", open ? "true" : "false");
        });

        if (open) {
          run();
        }

        var next = card.querySelector(
          (open ? ".rule-face--owner" : ".rule-face--agent") + " .rule-turn"
        );
        if (!next) {
          return;
        }
        window.setTimeout(function () {
          try {
            next.focus({ preventScroll: true });
          } catch (e) {
            next.focus();
          }
        }, SWAP_MS);
      });
    });
  });
})();
