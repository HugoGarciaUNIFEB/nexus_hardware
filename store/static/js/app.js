document.addEventListener('DOMContentLoaded', () => {
  // Atalho de Teclado Global: Ctrl + K ou Cmd + K foca na busca
  const searchInput = document.querySelector('#global-search-input');
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }
  });

  // Galeria de Imagens Dinâmica no Detalhe do Produto
  const mainProductImg = document.querySelector('#main-product-img');
  const galleryThumbnails = document.querySelectorAll('.gallery-thumb');

  galleryThumbnails.forEach(thumb => {
    thumb.addEventListener('click', () => {
      const targetSrc = thumb.getAttribute('data-full-src') || thumb.getAttribute('src');
      if (mainProductImg && targetSrc) {
        mainProductImg.style.opacity = '0.4';
        setTimeout(() => {
          mainProductImg.src = targetSrc;
          mainProductImg.style.opacity = '1';
        }, 150);

        galleryThumbnails.forEach(t => t.classList.remove('border-primary', 'hud-glow-subtle'));
        thumb.classList.add('border-primary', 'hud-glow-subtle');
      }
    });
  });

  // Auto-dismiss para alertas e mensagens após 5 segundos
  const toastMessages = document.querySelectorAll('.toast-message');
  toastMessages.forEach(toast => {
    setTimeout(() => {
      toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      setTimeout(() => toast.remove(), 400);
    }, 5000);
  });

  // Toggle do menu mobile (caso exista)
  const mobileMenuBtn = document.querySelector('#mobile-menu-btn');
  const mobileNav = document.querySelector('#mobile-nav');
  if (mobileMenuBtn && mobileNav) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileNav.classList.toggle('hidden');
    });
  }
});
