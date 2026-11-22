// Copies the web game (../../memory) into www/ for the apps, leaving out web-only and store files.
const fs = require("fs"), path = require("path");
const SRC = path.join(__dirname, "..", "..", "memory"), OUT = path.join(__dirname, "www");
const SKIP = new Set(["store", "sw.js", "make_sw.py", "make_assets.py", "README.md", "manifest.webmanifest", "lines.json"]);
fs.rmSync(OUT, { recursive: true, force: true });
(function copy(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const f of fs.readdirSync(src)) {
    if (SKIP.has(f) || f.startsWith(".") || f.startsWith("_")) continue;
    const s = path.join(src, f), d = path.join(dst, f);
    fs.statSync(s).isDirectory() ? copy(s, d) : fs.copyFileSync(s, d);
  }
})(SRC, OUT);
console.log("www ready:", fs.readdirSync(OUT).join(", "));
