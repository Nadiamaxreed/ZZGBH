/* Share the same decode-before-switch behavior across all eight websites. */
(() => {
  const root = document.querySelector('.hm-carousel, .banner');
  if (!root) return;
  const company = root.classList.contains('hm-carousel');
  const slides = [...root.querySelectorAll(company ? '.hm-slide' : '.banner-slide')];
  const buttons = [...root.querySelectorAll(company ? '.hm-dots button' : '[data-slide]')];
  const activeClass = company ? 'is-active' : 'active';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let active = 0, ticket = 0, timer, idleTimer, hovered = false, focused = false;
  const failed = new Set();
  const allowed = () => !document.hidden && !hovered && !focused && !reduced.matches;
  const stop = () => { clearTimeout(timer); clearTimeout(idleTimer); };
  const prepare = async (index) => {
    const slide = slides[index], img = slide.querySelector('img');
    slide.querySelectorAll('source[data-srcset]').forEach(source => {
      source.srcset = source.dataset.srcset; source.removeAttribute('data-srcset');
    });
    img.loading = 'eager';
    if (img.dataset.srcset) { img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); }
    if (img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
    if (img.decode) await img.decode();
    else if (!img.complete) await new Promise((resolve, reject) => {
      img.addEventListener('load', resolve, {once:true});
      img.addEventListener('error', reject, {once:true});
    });
    if (!img.naturalWidth) throw Error('Image unavailable');
  };
  const next = () => {
    for (let n = 1; n < slides.length; n++) {
      const i = (active + n) % slides.length;
      if (!failed.has(i)) return i;
    }
    return active;
  };
  const warm = () => {
    clearTimeout(idleTimer);
    if (!allowed() || navigator.connection?.saveData) return;
    idleTimer = setTimeout(() => {
      const i = next();
      if (i !== active && allowed()) prepare(i).catch(() => failed.add(i));
    }, 1200);
  };
  const show = async index => {
    const request = ++ticket;
    root.setAttribute('aria-busy', 'true');
    try {
      await prepare(index);
      if (request !== ticket) return;
      slides.forEach((slide, i) => {
        slide.classList.toggle(activeClass, i === index);
        slide.setAttribute('aria-hidden', String(i !== index));
      });
      buttons.forEach((button, i) => {
        button.classList.toggle('is-active', i === index);
        button.setAttribute('aria-pressed', String(i === index));
      });
      active = index; failed.delete(index); warm();
    } catch { failed.add(index); }
    finally { if (request === ticket) root.removeAttribute('aria-busy'); }
  };
  const schedule = () => {
    clearTimeout(timer);
    if (allowed() && slides.length > 1) timer = setTimeout(async () => {
      await show(next()); schedule();
    }, company ? 6000 : 5000);
  };
  buttons.forEach((button, i) => button.addEventListener('click', async () => {
    stop(); await show(i); schedule();
  }));
  root.addEventListener('mouseenter', () => { hovered = true; stop(); });
  root.addEventListener('mouseleave', () => { hovered = false; warm(); schedule(); });
  root.addEventListener('focusin', () => { focused = true; stop(); });
  root.addEventListener('focusout', () => { focused = false; warm(); schedule(); });
  document.addEventListener('visibilitychange', () => { stop(); if (allowed()) { warm(); schedule(); } });
  reduced.addEventListener('change', () => { stop(); warm(); schedule(); });
  prepare(0).then(() => { warm(); schedule(); }).catch(() => failed.add(0));
})();
