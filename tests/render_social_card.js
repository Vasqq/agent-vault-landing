#!/usr/bin/env node
/** Render assets/images/social-card.html to social-card.png (1200x630). */
const { chromium } = require("playwright");
const path = require("path");

const root = path.join(__dirname, "..");
const html = "file://" + path.join(root, "assets/images/social-card.html");
const out = path.join(root, "assets/images/social-card.png");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.goto(html, { waitUntil: "networkidle" });
  await page.locator(".card").screenshot({ path: out, type: "png" });
  await browser.close();
  console.log("wrote", out);
})();
