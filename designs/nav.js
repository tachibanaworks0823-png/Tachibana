
if (new URLSearchParams(location.search).get("shot") === "1") {
  document.documentElement.classList.add("shot");
  document.addEventListener("DOMContentLoaded", () => document.body.classList.add("shot"));
}
window.DESIGN_FILES = {
  1: "01-billboard.html",
  2: "02-scoreboard.html",
  3: "03-hero-punch.html",
  4: "04-price-wall.html",
  5: "05-split-blast.html",
  6: "06-neon-club.html",
  7: "07-band.html",
  8: "08-center-stage.html",
};
(() => {
  const file = location.pathname.split("/").pop() || "";
  const m = file.match(/^(\d{2})-/);
  const n = m ? parseInt(m[1], 10) : 1;
  const total = Object.keys(window.DESIGN_FILES).length;
  const go = (t) => { const name = window.DESIGN_FILES[t]; if (name) location.href = name; };
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" || e.key === " ") { e.preventDefault(); go(n >= total ? 1 : n + 1); }
    else if (e.key === "ArrowLeft") { e.preventDefault(); go(n <= 1 ? total : n - 1); }
    else if (e.key === "Escape" || e.key === "g" || e.key === "G") location.href = "../index.html";
  });
})();
