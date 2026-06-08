// ── Progress bar
const progressBar = document.getElementById('progress-bar');
// ── Back to top
const backToTop = document.getElementById('back-to-top');
// ── Header
const header = document.getElementById('header');
// ── Nav links
const navLinks = document.querySelectorAll('.nav-link[data-section]');
const sections = document.querySelectorAll('section[id]');

function onScroll() {
  const scrollY  = window.scrollY;
  const maxScroll = document.documentElement.scrollHeight - window.innerHeight;

  // progress bar
  if (progressBar) progressBar.style.width = (scrollY / maxScroll * 100) + '%';

  // header shadow
  header.classList.toggle('scrolled', scrollY > 20);

  // back to top visibility
  if (backToTop) backToTop.classList.toggle('visible', scrollY > 500);

  // active nav link (scroll spy)
  let current = '';
  sections.forEach(sec => {
    if (scrollY >= sec.offsetTop - 90) current = sec.id;
  });
  navLinks.forEach(link => {
    link.classList.toggle('active', link.dataset.section === current);
  });
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// Back to top click
if (backToTop) {
  backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// Mobile menu toggle
const menuToggle = document.getElementById('menu-toggle');
const mainNav    = document.getElementById('main-nav');
if (menuToggle && mainNav) {
  menuToggle.addEventListener('click', () => mainNav.classList.toggle('open'));
  navLinks.forEach(link => link.addEventListener('click', () => mainNav.classList.remove('open')));
}

// Scroll-reveal via IntersectionObserver
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.08 });

const revealSelectors = [
  '.info-card', '.eixo-card', '.team-card', '.senti-card',
  '.prod-item', '.connect-item', '.theme-item', '.project-item',
  '.line-item', '.cta-contact-item', '.cta-event-card',
  '.hero-stat', '.meth-step'
];
document.querySelectorAll(revealSelectors.join(',')).forEach((el, i) => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(20px)';
  el.style.transition = `opacity .5s ease ${(i % 6) * 60}ms, transform .5s ease ${(i % 6) * 60}ms`;
  observer.observe(el);
});
