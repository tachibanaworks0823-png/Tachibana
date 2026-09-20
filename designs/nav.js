
window.DESIGN_FILES = {1: '01-base.html', 2: '02-pika-front.html', 3: '03-wide-menu.html', 4: '04-bottle-dominate.html', 5: '05-brut-stack.html', 6: '06-glass-panel.html', 7: '07-gold-rule.html', 8: '08-leader-dots.html', 9: '09-ice-lead.html', 10: '10-rose-lead.html', 11: '11-deep-noir.html', 12: '12-warm-amber.html', 13: '13-cool-night.html', 14: '14-crop-impact.html', 15: '15-show-labels.html', 16: '16-framed-panel.html', 17: '17-glow-hot.html', 18: '18-soft-fade.html', 19: '19-five-ghost.html', 20: '20-bar-floor.html'};
if (new URLSearchParams(location.search).get('shot') === '1') {
  document.documentElement.classList.add('shot');
  document.addEventListener('DOMContentLoaded', () => document.body.classList.add('shot'));
}
(() => {
  const m = (location.pathname.split('/').pop() || '').match(/^(\d{2})-/);
  const n = m ? parseInt(m[1], 10) : 1;
  const total = Object.keys(DESIGN_FILES).length;
  const go = (t) => { const name = DESIGN_FILES[t]; if (name) location.href = name; };
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(n >= total ? 1 : n + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); go(n <= 1 ? total : n - 1); }
    else if (e.key === 'Escape' || e.key === 'g' || e.key === 'G') location.href = '../index.html';
  });
})();
