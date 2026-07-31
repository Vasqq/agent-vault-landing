(function () {
  "use strict";

  var rows = document.querySelectorAll("#receipt-rows .row");
  var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function revealRows() {
    rows.forEach(function (row, index) {
      var delay = reducedMotion ? 0 : Number(row.getAttribute("data-delay") || index) * 280;
      window.setTimeout(function () {
        row.classList.add("is-visible");
      }, delay);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", revealRows);
  } else {
    revealRows();
  }
})();
