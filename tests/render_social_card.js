#!/usr/bin/env node
/** Render assets/images/social-card.html to social-card.png (1200x630). */
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const html = "file://" + path.join(root, "assets/images/social-card.html");
const out = path.join(root, "assets/images/social-card.png");
// file:// pages cannot fetch() the JSON, so the art is read here and injected.
const art = JSON.parse(fs.readFileSync(path.join(root, "assets/ascii/temple-hero.json"), "utf8"));

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.goto(html, { waitUntil: "networkidle" });
  await page.evaluate((layers) => {
    for (const name of ["dg", "lo", "hi"]) {
      document.querySelector(`[data-ascii="temple-hero"] .${name}`).textContent = layers[name] || "";
    }
  }, art.layers);
  await page.evaluate(() => document.fonts.ready);
  await page.locator(".card").screenshot({ path: out, type: "png" });
  await browser.close();
  console.log("wrote", out);
})();
