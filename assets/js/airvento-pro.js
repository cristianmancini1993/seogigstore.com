(function () {
  const end = Date.now() + 15 * 60 * 1000;
  function tick() {
    const diff = Math.max(0, end - Date.now());
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    const eh = document.getElementById('cd-h');
    const em = document.getElementById('cd-m');
    const es = document.getElementById('cd-s');
    if (!eh || !em || !es) return;
    eh.textContent = String(h).padStart(2, '0');
    em.textContent = String(m).padStart(2, '0');
    es.textContent = String(s).padStart(2, '0');
    if (diff > 0) setTimeout(tick, 1000);
  }
  tick();
})();

(function () {
  let count = 31;
  const el = document.getElementById('liveCount');
  if (!el) return;
  setInterval(() => {
    count += (Math.random() > 0.5 ? 1 : -1) * Math.ceil(Math.random() * 2);
    count = Math.min(42, Math.max(24, count));
    el.innerHTML = `<strong>${count} persone</strong> stanno guardando questo soffiatore ora`;
  }, 2000);
})();

document.querySelectorAll('.faq-item').forEach((item) => {
  const btn = item.querySelector('.faq-q');
  if (!btn) return;
  btn.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach((i) => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});
