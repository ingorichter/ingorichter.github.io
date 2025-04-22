// screenshot.js
const puppeteer = require("puppeteer");
const fs = require("fs");
const path = require("path");

const BASE_URL = "http://localhost:1313";
const isBaseline = process.argv.includes("--baseline");
const OUTPUT_DIR = path.join("screenshots", isBaseline ? "baseline" : "current");
const visited = new Set();

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

async function waitForImagesToLoad(page) {
  await page.evaluate(() => {
    return Promise.all(
      Array.from(document.images)
        .filter((img) => !img.complete)
        .map(
          (img) =>
            new Promise((resolve) => {
              img.onload = img.onerror = resolve;
            })
        )
    );
  });
}

async function crawlAndScreenshot(page, url) {
  if (visited.has(url) || url.includes("/index.xml")) return;
  visited.add(url);

  const response = await page.goto(url, { waitUntil: "networkidle2" });
  if (!response || !response.ok()) return;

  const filename =
    url
      .replace(BASE_URL, "")
      .replace(/\/$/, "")
      .replace(/[^\w-]/g, "_") || "home";

  const filepath = path.join(OUTPUT_DIR, `${filename}.png`);
  console.log(`📸 ${url} → ${filepath}`);

  await page.evaluate(async () => {
    await new Promise(resolve => {
      let totalHeight = 0;
      const distance = 100;
      const timer = setInterval(() => {
        window.scrollBy(0, distance);
        totalHeight += distance;
        if (totalHeight >= document.body.scrollHeight) {
          clearInterval(timer);
          resolve();
        }
      }, 100);
    });
  });

  await page.screenshot({ path: filepath, fullPage: true });

  const links = await page.$$eval('a[href^="/"]', (as) =>
    as.map((a) => a.getAttribute("href")).filter(Boolean)
  );

  for (const link of links) {
    const nextUrl = new URL(link, BASE_URL).href;
    await crawlAndScreenshot(page, nextUrl);
  }
}

(async () => {
  ensureDir(OUTPUT_DIR);

  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  await crawlAndScreenshot(page, BASE_URL);

  await browser.close();
})();