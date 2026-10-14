/* Controles da janela de detalhes do Streamlit. Executado no documento principal via st.html. */
(() => {
  if (window.__pontoApoioModalControlsLoaded) return;
  window.__pontoApoioModalControlsLoaded = true;

  const visible = el => !!el && el.getClientRects().length > 0;
  function findDialog() {
    const candidates = [...document.querySelectorAll('[data-testid="stDialog"], [role="dialog"], div[aria-modal="true"]')];
    return candidates.find(visible) || null;
  }

  function setupDialog() {
    const dialog = findDialog();
    if (!dialog) return;
    if (dialog.dataset.pontoControlsReady === '1') return;

    let header = dialog.querySelector('[data-testid="stDialogHeader"]') || dialog.querySelector('header') || dialog.querySelector('div > div > div > h1')?.parentElement?.parentElement;
    
    if (!header) {
      const titleEl = dialog.querySelector('h1, h2, h3');
      if (titleEl) {
        header = titleEl.closest('div');
      }
    }
    if (!header) return;

    dialog.dataset.pontoControlsReady = '1';
    dialog.classList.add('ponto-modal-window');
    header.classList.add('ponto-modal-header');

    if (header.querySelector('.ponto-window-controls')) return;

    const controls = document.createElement('div');
    controls.className = 'ponto-window-controls';
    controls.innerHTML = `
      <button type="button" class="ponto-win-btn" data-action="min" title="Minimizar" aria-label="Minimizar">−</button>
      <button type="button" class="ponto-win-btn" data-action="max" title="Maximizar" aria-label="Maximizar">□</button>
      <button type="button" class="ponto-win-btn ponto-win-close" data-action="close" title="Fechar" aria-label="Fechar">×</button>
    `;

    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';
    header.appendChild(controls);

    controls.addEventListener('click', event => {
      const btn = event.target.closest('button[data-action]');
      if (!btn) return;
      event.preventDefault();
      event.stopPropagation();
      const action = btn.dataset.action;

      if (action === 'min') {
        dialog.classList.toggle('ponto-minimized');
        btn.textContent = dialog.classList.contains('ponto-minimized') ? '▢' : '−';
      } else if (action === 'max') {
        dialog.classList.toggle('ponto-maximized');
        dialog.classList.remove('ponto-minimized');
        const minBtn = controls.querySelector('[data-action="min"]');
        if (minBtn) minBtn.textContent = '−';
        btn.textContent = dialog.classList.contains('ponto-maximized') ? '❐' : '□';
      } else if (action === 'close') {
        const nativeClose = dialog.querySelector('button[aria-label="Close"], button[aria-label="Fechar"], [data-testid="stDialogCloseButton"] button');
        if (nativeClose) {
          nativeClose.click();
        } else {
          const allBtns = [...dialog.querySelectorAll('button')];
          const closeBtn = allBtns.find(b => /^(×|x|fechar|close)$/i.test(b.textContent.trim() || b.getAttribute('aria-label') || ''));
          if (closeBtn) closeBtn.click();
        }
      }
    });

    let dragging = false, startX = 0, startY = 0, originX = 0, originY = 0;
    header.addEventListener('pointerdown', event => {
      if (event.target.closest('button, input, a, .ponto-window-controls') || dialog.classList.contains('ponto-maximized')) return;
      const rect = dialog.getBoundingClientRect();
      dragging = true;
      startX = event.clientX;
      startY = event.clientY;
      originX = rect.left;
      originY = rect.top;
      try { header.setPointerCapture(event.pointerId); } catch(e) {}
      dialog.classList.add('ponto-dragging');
      event.preventDefault();
    });

    header.addEventListener('pointermove', event => {
      if (!dragging) return;
      const maxLeft = Math.max(0, window.innerWidth - dialog.offsetWidth);
      const maxTop = Math.max(0, window.innerHeight - 50);
      const newLeft = Math.min(maxLeft, Math.max(0, originX + event.clientX - startX));
      const newTop = Math.min(maxTop, Math.max(0, originY + event.clientY - startY));
      dialog.style.setProperty('left', `${newLeft}px`, 'important');
      dialog.style.setProperty('top', `${newTop}px`, 'important');
      dialog.style.setProperty('transform', 'none', 'important');
      dialog.style.setProperty('margin', '0', 'important');
    });

    const stopDrag = e => {
      if (!dragging) return;
      dragging = false;
      dialog.classList.remove('ponto-dragging');
      try { header.releasePointerCapture(e.pointerId); } catch(err) {}
    };
    header.addEventListener('pointerup', stopDrag);
    header.addEventListener('pointercancel', stopDrag);
  }

  const init = () => {
    setupDialog();
    const observer = new MutationObserver(() => setupDialog());
    observer.observe(document.body, { childList: true, subtree: true });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();