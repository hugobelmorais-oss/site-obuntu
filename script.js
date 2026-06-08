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

// ══════════════════════════════════════════════════════
//  GOOGLE DRIVE — Produções
//  Para ativar: cole o URL do seu Apps Script em DRIVE_API_URL
//  (veja DRIVE_SETUP.md para instruções)
// ══════════════════════════════════════════════════════
const DRIVE_API_URL = ''; // ← cole o URL do Apps Script aqui

const MIME_LABELS = {
  'application/pdf':                                                         { label: 'PDF',           icon: '📄', type: 'pdf'   },
  'application/vnd.google-apps.document':                                    { label: 'Doc',           icon: '📝', type: 'doc'   },
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': { label: 'Word',          icon: '📝', type: 'doc'   },
  'application/vnd.google-apps.spreadsheet':                                 { label: 'Planilha',      icon: '📊', type: 'sheet' },
  'application/vnd.google-apps.presentation':                                { label: 'Apresentação',  icon: '📊', type: 'slide' },
  'application/vnd.openxmlformats-officedocument.presentationml.presentation':{ label:'Apresentação',  icon: '📊', type: 'slide' },
  'image/jpeg': { label: 'Imagem', icon: '🖼️', type: 'image' },
  'image/png':  { label: 'Imagem', icon: '🖼️', type: 'image' },
  'image/svg+xml': { label: 'Imagem', icon: '🖼️', type: 'image' },
};

function driveFileInfo(mimeType) {
  return MIME_LABELS[mimeType] || { label: 'Arquivo', icon: '📎', type: 'other' };
}

function driveCard(file) {
  const info = driveFileInfo(file.mimeType);
  const date = file.createdTime
    ? new Date(file.createdTime).toLocaleDateString('pt-BR', { year:'numeric', month:'short' })
    : '';
  const displayName = file.name.replace(/\.(pdf|docx?|pptx?|xlsx?)$/i, '').replace(/[_;]/g, ' ').trim();
  return `
    <a href="${file.url}" target="_blank" rel="noopener"
       class="drive-card" data-filetype="${info.type}" title="${file.name}">
      <span class="drive-card-icon">${info.icon}</span>
      <span class="drive-card-info">
        <span class="drive-card-badge">${info.label}</span>
        <span class="drive-card-name">${displayName}</span>
        ${date ? `<span class="drive-card-date">${date}</span>` : ''}
      </span>
      <span class="drive-card-arrow">›</span>
    </a>`;
}

async function loadDriveFiles() {
  const grid    = document.getElementById('drive-grid');
  const status  = document.getElementById('drive-status');
  const filters = document.getElementById('drive-filters');
  const notConf = document.getElementById('drive-not-configured');

  if (!DRIVE_API_URL) {
    if (grid)    grid.innerHTML = '';
    if (status)  status.remove();
    if (filters) filters.style.display = 'none';
    if (notConf) notConf.style.display = 'block';
    return;
  }

  try {
    const res   = await fetch(DRIVE_API_URL);
    const data  = await res.json();
    const files = data.files || [];

    if (status) {
      status.textContent = `${files.length} arquivo${files.length !== 1 ? 's' : ''}`;
      status.className = 'drive-badge ok';
    }
    if (filters) filters.style.display = 'flex';
    if (grid)   grid.innerHTML = files.map(driveCard).join('');

    // Filter buttons
    document.querySelectorAll('.drive-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.drive-filter').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const type = btn.dataset.type;
        document.querySelectorAll('.drive-card').forEach(card => {
          card.style.display = (type === 'all' || card.dataset.filetype === type) ? '' : 'none';
        });
      });
    });
  } catch (err) {
    if (status) { status.textContent = 'Erro ao carregar'; status.className = 'drive-badge error'; }
    if (grid)   grid.innerHTML = '<p class="drive-error">Não foi possível carregar os arquivos. Tente novamente mais tarde.</p>';
    console.error('Drive API error:', err);
  }
}

loadDriveFiles();

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
