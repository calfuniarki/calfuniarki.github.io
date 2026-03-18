/* ============================================================
   Calfuniarki — main.js
   Scroll reveal, mobile menu, header shrink, ambient particles
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* --- Enable reveal animations (fallback: everything visible without JS) --- */
  document.body.classList.add('js-ready');

  /* --- Mobile menu --- */
  const toggle  = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  const overlay  = document.querySelector('.nav-overlay');

  if (toggle) {
    const close = () => {
      toggle.classList.remove('open');
      navLinks.classList.remove('open');
      if (overlay) overlay.classList.remove('open');
    };
    toggle.addEventListener('click', () => {
      const open = toggle.classList.toggle('open');
      navLinks.classList.toggle('open', open);
      if (overlay) overlay.classList.toggle('open', open);
    });
    if (overlay) overlay.addEventListener('click', close);
    navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', close));
  }

  /* --- Header shrink on scroll --- */
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 60);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* --- Scroll reveal --- */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(el => io.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('visible'));
  }

  /* --- Ambient particles --- */
  const canvas = document.getElementById('particles');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let w, h, particles;
    const COUNT = 40;

    function resize() {
      w = canvas.width  = window.innerWidth;
      h = canvas.height = window.innerHeight;
    }

    function init() {
      resize();
      particles = Array.from({ length: COUNT }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.5 + .5,
        dx: (Math.random() - .5) * .15,
        dy: (Math.random() - .5) * .15,
        o: Math.random() * .4 + .1,
      }));
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      particles.forEach(p => {
        p.x += p.dx;
        p.y += p.dy;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(200,164,92,${p.o})`;
        ctx.fill();
      });
      requestAnimationFrame(draw);
    }

    window.addEventListener('resize', resize, { passive: true });
    init();
    draw();
  }
});
