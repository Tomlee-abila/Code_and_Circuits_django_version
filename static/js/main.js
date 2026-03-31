/**
 * Code & Circuits — Main JavaScript
 */

'use strict';

// ── LUCIDE ICONS (re-init after dynamic content) ─────────────
function initIcons() {
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
}

// ── STAR RATING INTERACTION ───────────────────────────────────
function initStarRating() {
  const starGroups = document.querySelectorAll('.star-rating-input');
  starGroups.forEach(group => {
    const labels = group.querySelectorAll('.star-label');
    labels.forEach((label, idx) => {
      label.addEventListener('mouseenter', () => {
        labels.forEach((l, i) => {
          l.querySelector('.star-icon').style.color =
            i >= labels.length - 1 - idx ? 'var(--primary)' : 'var(--on-surface-dim)';
        });
      });
      label.addEventListener('mouseleave', () => {
        const checked = group.querySelector('.star-radio:checked');
        labels.forEach((l, i) => {
          if (checked) {
            const val = parseInt(checked.value);
            l.querySelector('.star-icon').style.color =
              i >= labels.length - val ? 'var(--primary)' : 'var(--on-surface-dim)';
          } else {
            l.querySelector('.star-icon').style.color = 'var(--on-surface-dim)';
          }
        });
      });
    });
  });
}

// ── PROGRESS BAR ANIMATION ────────────────────────────────────
function animateProgressBars() {
  const bars = document.querySelectorAll('.progress-bar, .learn-progress-fill');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        const target = bar.style.width;
        bar.style.width = '0%';
        requestAnimationFrame(() => {
          setTimeout(() => { bar.style.width = target; }, 50);
        });
        observer.unobserve(bar);
      }
    });
  }, { threshold: 0.2 });
  bars.forEach(bar => observer.observe(bar));
}

// ── COURSE FILTER (mobile toggle) ────────────────────────────
function initFilterToggle() {
  const toggleBtn = document.getElementById('filterToggleBtn');
  const sidebar = document.querySelector('.filters-sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      toggleBtn.setAttribute('aria-expanded', sidebar.classList.contains('open'));
    });
  }
}

// ── SCROLL-TO-TOP ─────────────────────────────────────────────
function initScrollTop() {
  const btn = document.createElement('button');
  btn.className = 'scroll-top-btn';
  btn.setAttribute('aria-label', 'Scroll to top');
  btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m18 15-6-6-6 6"/></svg>';
  document.body.appendChild(btn);

  const style = document.createElement('style');
  style.textContent = `
    .scroll-top-btn {
      position: fixed; bottom: 1.5rem; right: 1.5rem;
      width: 40px; height: 40px;
      background: var(--primary); color: var(--on-primary);
      border-radius: var(--radius-md);
      display: flex; align-items: center; justify-content: center;
      opacity: 0; pointer-events: none;
      transition: opacity .3s, transform .3s;
      z-index: 50;
      box-shadow: 0 4px 16px rgba(255,228,131,.3);
    }
    .scroll-top-btn.visible { opacity: 1; pointer-events: all; }
    .scroll-top-btn:hover { transform: translateY(-2px); }
  `;
  document.head.appendChild(style);

  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ── QUIZ CHOICE INTERACTIVITY ─────────────────────────────────
function initQuizChoices() {
  const choices = document.querySelectorAll('.quiz-choice');
  choices.forEach(choice => {
    const radio = choice.querySelector('.quiz-radio');
    if (!radio) return;
    choice.addEventListener('click', () => {
      // Deselect siblings
      const group = document.querySelectorAll(`.quiz-radio[name="${radio.name}"]`);
      group.forEach(r => {
        r.closest('.quiz-choice')?.classList.remove('selected');
      });
      radio.checked = true;
      choice.classList.add('selected');
    });
  });
}

// ── NOTIFICATION DISMISS ──────────────────────────────────────
function initNotifDismiss() {
  document.querySelectorAll('.notif-close').forEach(btn => {
    if (btn.tagName === 'BUTTON') {
      btn.addEventListener('click', () => {
        btn.closest('.notif-item')?.remove();
      });
    }
  });
}

// ── FORM VALIDATION FEEDBACK ──────────────────────────────────
function initFormFeedback() {
  const forms = document.querySelectorAll('form');
  forms.forEach(form => {
    form.addEventListener('submit', () => {
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.style.opacity = '.7';
        const originalText = btn.innerHTML;
        btn.innerHTML = btn.innerHTML.replace(/<i[^>]*><\/i>\s*/, '') + ' Processing…';
        // Re-enable after 5s fallback
        setTimeout(() => {
          btn.disabled = false;
          btn.style.opacity = '';
          btn.innerHTML = originalText;
        }, 5000);
      }
    });
  });
}

// ── TOOLTIP SYSTEM ────────────────────────────────────────────
function initTooltips() {
  document.querySelectorAll('[data-tooltip]').forEach(el => {
    el.addEventListener('mouseenter', () => {
      const tip = document.createElement('div');
      tip.className = 'cc-tooltip';
      tip.textContent = el.dataset.tooltip;
      const style = `
        position: absolute; background: var(--surface-highest);
        color: var(--on-surface); padding: .35rem .65rem;
        border-radius: var(--radius-sm); font-size: .75rem;
        pointer-events: none; z-index: 1000;
        border: 1px solid var(--outline-subtle);
        white-space: nowrap;
      `;
      tip.style.cssText = style;
      document.body.appendChild(tip);

      const rect = el.getBoundingClientRect();
      tip.style.left = rect.left + window.scrollX + (rect.width / 2) - (tip.offsetWidth / 2) + 'px';
      tip.style.top  = rect.top + window.scrollY - tip.offsetHeight - 8 + 'px';

      el._ccTooltip = tip;
    });
    el.addEventListener('mouseleave', () => {
      el._ccTooltip?.remove();
    });
  });
}

// ── LESSON PROGRESS AUTO-SAVE ─────────────────────────────────
function initVideoProgress() {
  // Track video progress via postMessage from YouTube iframes
  // (Placeholder — full implementation requires YouTube IFrame API)
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'VIDEO_COMPLETE') {
      const markBtn = document.querySelector('button[name="mark_complete"]');
      if (markBtn) {
        markBtn.classList.add('btn-primary');
        markBtn.style.animation = 'pulse-glow 1s ease-in-out 3';
      }
    }
  });
}

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initIcons();
  initStarRating();
  animateProgressBars();
  initFilterToggle();
  initScrollTop();
  initQuizChoices();
  initNotifDismiss();
  initFormFeedback();
  initTooltips();
  initVideoProgress();
});
