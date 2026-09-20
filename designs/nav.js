
window.DESIGN_FILES={1: '01-velvet-billboard.html', 2: '02-vip-hero.html', 3: '03-gold-salon.html', 4: '04-rose-night.html', 5: '05-ice-lounge.html', 6: '06-pika-glow.html', 7: '07-triple-vip.html', 8: '08-mahogany-bar.html', 9: '09-champagne-mist.html', 10: '10-spotlight-nectar.html', 11: '11-cascade-luxe.html', 12: '12-mirror-suite.html', 13: '13-framed-collection.html', 14: '14-runway-bottles.html', 15: '15-overlay-panel.html', 16: '16-duo-stage.html', 17: '17-noir-glamour.html', 18: '18-amber-lounge.html', 19: '19-vertical-gallery.html', 20: '20-grand-arrival.html'};
if(new URLSearchParams(location.search).get('shot')==='1'){document.documentElement.classList.add('shot');document.addEventListener('DOMContentLoaded',()=>document.body.classList.add('shot'));}
(()=>{
  const m=(location.pathname.split('/').pop()||'').match(/^(\d{2})-/);
  const n=m?parseInt(m[1],10):1; const total=Object.keys(DESIGN_FILES).length;
  const go=t=>{const name=DESIGN_FILES[t]; if(name) location.href=name;};
  document.addEventListener('keydown',e=>{
    if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();go(n>=total?1:n+1);}
    else if(e.key==='ArrowLeft'){e.preventDefault();go(n<=1?total:n-1);}
    else if(e.key==='Escape'||e.key==='g'||e.key==='G') location.href='../index.html';
  });
})();
