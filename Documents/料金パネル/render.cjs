#!/usr/bin/env node
/**
 * Render each .panel from panels.html to PNG via Chrome headless (puppeteer-core).
 */
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const DIR = __dirname;
const OUT = DIR;
const HTML = path.join(DIR, "panels.html");

async function main() {
  fs.mkdirSync(OUT, { recursive: true });

  let puppeteer;
  try {
    puppeteer = require("puppeteer-core");
  } catch {
    console.log("Installing puppeteer-core...");
    execSync("npm install --no-save --prefix /tmp/rf-render puppeteer-core@23", {
      stdio: "inherit",
    });
    puppeteer = require("/tmp/rf-render/node_modules/puppeteer-core");
  }

  const browser = await puppeteer.launch({
    executablePath: "/usr/local/bin/google-chrome",
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--font-render-hinting=none"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1000, height: 1400, deviceScaleFactor: 2 });
  await page.goto("file://" + HTML, { waitUntil: "networkidle0", timeout: 120000 });
  // Wait for Google Fonts
  await page.evaluateHandle("document.fonts.ready");
  await new Promise((r) => setTimeout(r, 1500));

  const panels = await page.$$(".panel");
  console.log(`Found ${panels.length} panels`);

  const names = [];
  for (let i = 0; i < panels.length; i++) {
    const el = panels[i];
    const name = await el.evaluate((n) => n.dataset.name || `panel_${String(i + 1).padStart(2, "0")}`);
    const file = path.join(OUT, `panel_${name}.png`);
    await el.screenshot({ path: file, type: "png" });
    names.push({ name, file });
    console.log("Saved", path.basename(file));
  }

  await browser.close();

  // Also write a simple gallery HTML that references PNGs
  const gallery = `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CLUB Rain Forest A1料金パネル 20案</title>
<style>
  body{margin:0;padding:24px;background:#fff;font-family:"Noto Sans CJK JP",sans-serif;text-align:center;color:#222}
  h1{font-size:22px;margin:0 0 6px}
  p{color:#666;font-size:13px;line-height:1.7;margin:0 0 28px}
  h2{font-size:15px;color:#2f4a36;margin:28px 0 10px;letter-spacing:.04em}
  img{max-width:100%;height:auto;border:1px solid #e5e5e5;box-shadow:0 4px 16px rgba(0,0,0,.06)}
</style>
</head>
<body>
<h1>CLUB Rain Forest</h1>
<p>レインフォレスト｜A1縦 料金パネル サンプル20案<br>
お一人様 60分 ／ 20:00〜21:00 ¥4,000 ／ 21:00〜22:00 ¥5,000 ／ 22:00〜LAST ¥6,000 ／ 税・サ 30%<br>
高級感・シンプル・白系ベース</p>
${names
  .map(
    (n, i) =>
      `<h2>${String(i + 1).padStart(2, "0")} — ${n.name.replace(/^\d+_/, "").replace(/_/g, " ")}</h2>\n<img src="${path.basename(n.file)}" alt="${n.name}">`
  )
  .join("\n")}
</body>
</html>`;
  fs.writeFileSync(path.join(DIR, "見る.html"), gallery, "utf8");
  console.log("Wrote 見る.html");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
