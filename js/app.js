document.addEventListener('DOMContentLoaded', () => {
  const WHATSAPP_PHONE = '593992217314';
  const JSON_PATH = './productos.json';

  let allProducts = [];
  let currentCategory = 'todos';
  let searchQuery = '';
  let sortMode = 'price-asc';

  const productGrid = document.getElementById('productGrid');
  const catalogStatus = document.getElementById('catalogStatus');
  const searchInput = document.getElementById('searchInput');
  const clearSearch = document.getElementById('clearSearch');
  const categoryTabs = document.getElementById('categoryTabs');
  const sortSelect = document.getElementById('sortSelect');
  const currentYearSpan = document.getElementById('currentYear');

  if (currentYearSpan) {
    currentYearSpan.textContent = new Date().getFullYear();
  }

  async function loadProducts() {
    try {
      const res = await fetch(`${JSON_PATH}?t=${Date.now()}`);
      if (!res.ok) throw new Error('No se pudo acceder a productos.json');
      allProducts = await res.json();
      if (!allProducts || allProducts.length === 0) {
        throw new Error('No hay productos en el JSON');
      }
      renderCatalog();
    } catch (err) {
      console.error('Error cargando productos:', err);
      if (catalogStatus) {
        catalogStatus.innerHTML = '<p style="color: #ef4444;">❌ Error cargando productos. ' + err.message + '</p>';
        catalogStatus.style.display = 'block';
      }
      productGrid.innerHTML = '';
    }
  }

  function renderCatalog() {
    let filtered = allProducts.filter(item => {
      const catMatch = currentCategory === 'todos' || (item.categoria && item.categoria.toLowerCase() === currentCategory.toLowerCase());
      const query = searchQuery.toLowerCase().trim();
      const textMatch = !query || 
        (item.nombre && item.nombre.toLowerCase().includes(query)) || 
        (item.caracteristicas && item.caracteristicas.some(c => c && c.toLowerCase().includes(query)));
      return catMatch && textMatch;
    });

    if (sortMode === 'price-asc') {
      filtered.sort((a, b) => (Number(a.precio) || 0) - (Number(b.precio) || 0));
    } else if (sortMode === 'price-desc') {
      filtered.sort((a, b) => (Number(b.precio) || 0) - (Number(a.precio) || 0));
    } else if (sortMode === 'name-asc') {
      filtered.sort((a, b) => (a.nombre || '').localeCompare(b.nombre || ''));
    }

    if (filtered.length === 0) {
      catalogStatus.style.display = 'block';
      catalogStatus.innerHTML = '<p>No se encontraron productos coincidentes.</p>';
      productGrid.innerHTML = '';
      return;
    }

    catalogStatus.style.display = 'none';
    productGrid.innerHTML = filtered.map(p => createCard(p)).join('');

    // Reinitialize lucide icons
    if (window.lucide) {
      lucide.createIcons();
    }
  }

  function createCard(p) {
    const defaultSvg = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="150" height="150" viewBox="0 0 24 24" fill="none" stroke="%2394a3b8" stroke-width="1.5"><rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M12 8v8M8 12h8"/></svg>';
    let img = p.imagen || defaultSvg;
    if (img && img.startsWith('imagenes/')) {
      img = './' + img;
    }

    const precio = Number(p.precio) ? `$${Number(p.precio).toFixed(2)}` : 'Consultar';
    const specs = (p.caracteristicas || []).slice(0, 4);
    const specsHtml = specs.map(s => `<li><span class="spec-bullet"></span><span>${escapeHtml(s)}</span></li>`).join('');

    const msg = encodeURIComponent(`Hola AGNEXUSUIO, deseo cotizar el siguiente equipo:\n\n*${p.nombre}*\nPrecio Final: ${precio}\n\n¿Tienen disponibilidad para entrega?`);
    const waUrl = `https://wa.me/${WHATSAPP_PHONE}?text=${msg}`;

    return `
      <article class="product-card">
        <div class="product-image-container">
          <img src="${escapeHtml(img)}" alt="${escapeHtml(p.nombre)}" loading="lazy" onerror="this.src='${defaultSvg}'">
        </div>
        <div class="product-body">
          <span class="product-category-tag">${escapeHtml(p.categoria || 'Tecnología')}</span>
          <h2 class="product-title" title="${escapeHtml(p.nombre)}">${escapeHtml(p.nombre)}</h2>
          <ul class="product-specs">${specsHtml}</ul>
          <div class="product-footer">
            <div class="product-price-box">
              <span class="price-label">Precio Final</span>
              <span class="product-price">${precio}</span>
            </div>
            <a href="${waUrl}" target="_blank" class="btn-quote" aria-label="Cotizar por WhatsApp">
              <i data-lucide="message-circle"></i>
              <span>Cotizar</span>
            </a>
          </div>
        </div>
      </article>
    `;
  }

  function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  searchInput.addEventListener('input', (e) => {
    searchQuery = e.target.value;
    clearSearch.style.display = searchQuery ? 'block' : 'none';
    renderCatalog();
  });

  clearSearch.addEventListener('click', () => {
    searchInput.value = '';
    searchQuery = '';
    clearSearch.style.display = 'none';
    searchInput.focus();
    renderCatalog();
  });

  categoryTabs.addEventListener('click', (e) => {
    const btn = e.target.closest('.tab-btn');
    if (btn) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentCategory = btn.getAttribute('data-category');
      renderCatalog();
    }
  });

  sortSelect.addEventListener('change', (e) => {
    sortMode = e.target.value;
    renderCatalog();
  });

  loadProducts();
});
