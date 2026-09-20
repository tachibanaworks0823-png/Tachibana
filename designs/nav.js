window.DESIGN_FILES = {
  1: "01-winelist.html",
  2: "02-hero-nir.html",
  3: "03-type-poster.html",
  4: "04-art-deco.html",
  5: "05-spotlight.html",
  6: "06-filmstrip.html",
  7: "07-cascade.html",
  8: "08-gold-plate.html",
  9: "09-luminous.html",
  10: "10-price-hero.html",
  11: "11-mirror.html",
  12: "12-glass-panel.html",
  13: "13-tate-gaki.html",
  14: "14-club-led.html",
  15: "15-silk.html",
  16: "16-brutal.html",
  17: "17-ornate-frame.html",
  18: "18-diptych.html",
  19: "19-ledger.html",
  20: "20-orbit.html",
  21: "21-manifesto.html",
};

(() => {
  const file = location.pathname.split("/").pop() || "";
  const m = file.match(/^(\d{2})-/);
  const n = m ? parseInt(m[1], 10) : 1;

  const go = (target) => {
    const name = window.DESIGN_FILES[target];
    if (name) location.href = name;
  };

  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight" || e.key === " ") {
      e.preventDefault();
      go(n >= 21 ? 1 : n + 1);
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      go(n <= 1 ? 21 : n - 1);
    } else if (e.key === "Escape" || e.key === "g" || e.key === "G") {
      location.href = "../index.html";
    }
  });
})();
