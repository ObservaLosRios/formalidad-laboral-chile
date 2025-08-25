// Navegación entre secciones por data-section
document.addEventListener('DOMContentLoaded', () => {
	const navLinks = document.querySelectorAll('.nav-link');
	const sections = document.querySelectorAll('.section');

	function showSection(id) {
		sections.forEach(s => s.classList.toggle('active', s.id === id));
		navLinks.forEach(l => l.classList.toggle('active', l.getAttribute('data-section') === id));
		// Al activar una sección, forzar resize de los gráficos visibles con altura específica
		requestAnimationFrame(() => {
			const HEIGHTS = {
				'chart-tasa-informal': 500, 'chart-ocupados-informales': 500,
				'chart-tasa-noagro': 500, 'chart-inf-los-rios-edu': 520, 'chart-for-los-rios-edu': 520
			};
			const visibleCharts = document.querySelectorAll(`#${id} .chart-section > div[id]`);
			visibleCharts.forEach(div => {
				try {
					const h = HEIGHTS[div.id] || 500;
					if (window.Plotly && typeof window.Plotly.relayout === 'function') {
						window.Plotly.relayout(div.id, { height: h });
						window.Plotly.Plots.resize(div.id);
					}
				} catch (e) { /* noop */ }
			});
		});
	}

	navLinks.forEach(link => {
		link.addEventListener('click', () => {
			const target = link.getAttribute('data-section');
			if (target) showSection(target);
		});
	});

	// Modal de configuración básico
	const modal = document.getElementById('configModal');
	const closeBtn = document.querySelector('#configModal .close');
	if (closeBtn) {
		closeBtn.onclick = () => modal && (modal.style.display = 'none');
	}
	window.onclick = (event) => {
		if (event.target === modal) modal.style.display = 'none';
	};

	// Valores iniciales coherentes con la plantilla ya cargada
	const titleInput = document.getElementById('title-input');
	const subtitleInput = document.getElementById('subtitle-input');
	const footerInput = document.getElementById('footer-input');
	if (titleInput) titleInput.value = document.getElementById('main-title')?.textContent || '';
	if (subtitleInput) subtitleInput.value = document.getElementById('subtitle')?.textContent || '';
	if (footerInput) footerInput.value = document.getElementById('footer-text')?.textContent || '';
});

// Abre el modal de configuración
function openModal() {
	const modal = document.getElementById('configModal');
	if (modal) modal.style.display = 'block';
}

// Aplica cambios simples de título/subtítulo/footer desde el modal
function applyConfiguration() {
	const title = document.getElementById('title-input')?.value?.trim();
	const subtitle = document.getElementById('subtitle-input')?.value?.trim();
	const footer = document.getElementById('footer-input')?.value?.trim();

	if (title) document.getElementById('main-title').textContent = title;
	if (subtitle) document.getElementById('subtitle').textContent = subtitle;
	if (footer) document.getElementById('footer-text').textContent = footer;

	const modal = document.getElementById('configModal');
	if (modal) modal.style.display = 'none';
}

// Demo opcional de carga de datos (no afecta los 3 gráficos ya integrados)
function loadExampleData() {
	const status = document.getElementById('status-message');
	if (status) {
		status.className = 'status-message status-info';
		status.textContent = 'Ejemplo cargado. Edita títulos y guarda para ver cambios.';
	}
}

