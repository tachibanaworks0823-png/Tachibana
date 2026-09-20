(() => {
  const SLIDE_DURATION_MS = 9000;
  const IDLE_HIDE_MS = 2500;

  const slides = Array.from(document.querySelectorAll(".slide"));
  const progressBar = document.getElementById("progressBar");
  const dotsRoot = document.getElementById("dots");
  const body = document.body;

  let index = 0;
  let timerId = null;
  let startedAt = 0;
  let remaining = SLIDE_DURATION_MS;
  let paused = false;
  let rafId = null;
  let idleTimer = null;

  function buildDots() {
    dotsRoot.innerHTML = "";
    slides.forEach((_, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.setAttribute("aria-label", `スライド ${i + 1}`);
      if (i === index) btn.classList.add("is-active");
      btn.addEventListener("click", () => goTo(i));
      dotsRoot.appendChild(btn);
    });
  }

  function syncDots() {
    Array.from(dotsRoot.children).forEach((dot, i) => {
      dot.classList.toggle("is-active", i === index);
    });
  }

  function showSlide(nextIndex) {
    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === nextIndex);
    });
    index = nextIndex;
    syncDots();
  }

  function clearTimer() {
    if (timerId) {
      clearTimeout(timerId);
      timerId = null;
    }
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
  }

  function updateProgress() {
    if (paused) return;
    const elapsed = performance.now() - startedAt;
    const ratio = Math.min(1, elapsed / remaining);
    progressBar.style.width = `${ratio * 100}%`;
    if (ratio < 1) {
      rafId = requestAnimationFrame(updateProgress);
    }
  }

  function scheduleNext(ms = SLIDE_DURATION_MS) {
    clearTimer();
    remaining = ms;
    startedAt = performance.now();
    progressBar.style.width = "0%";
    rafId = requestAnimationFrame(updateProgress);
    timerId = setTimeout(() => {
      goTo((index + 1) % slides.length);
    }, ms);
  }

  function goTo(nextIndex) {
    showSlide(nextIndex);
    scheduleNext(SLIDE_DURATION_MS);
  }

  function pause() {
    if (paused) return;
    paused = true;
    const elapsed = performance.now() - startedAt;
    remaining = Math.max(300, remaining - elapsed);
    clearTimer();
  }

  function resume() {
    if (!paused) return;
    paused = false;
    scheduleNext(remaining);
  }

  function markInteractive() {
    body.classList.add("is-interactive");
    clearTimeout(idleTimer);
    idleTimer = setTimeout(() => {
      body.classList.remove("is-interactive");
    }, IDLE_HIDE_MS);
  }

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen?.();
    } else {
      document.exitFullscreen?.();
    }
  }

  document.addEventListener("keydown", (event) => {
    markInteractive();
    if (event.code === "Space") {
      event.preventDefault();
      if (paused) resume();
      else pause();
      return;
    }
    if (event.code === "ArrowRight") {
      goTo((index + 1) % slides.length);
      return;
    }
    if (event.code === "ArrowLeft") {
      goTo((index - 1 + slides.length) % slides.length);
      return;
    }
    if (event.code === "KeyF") {
      toggleFullscreen();
    }
  });

  ["mousemove", "pointerdown", "touchstart"].forEach((type) => {
    document.addEventListener(type, markInteractive, { passive: true });
  });

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pause();
    else resume();
  });

  buildDots();
  showSlide(0);
  if (slides.length > 1) {
    scheduleNext(SLIDE_DURATION_MS);
  } else {
    progressBar.style.width = "100%";
  }
})();
