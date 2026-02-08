document.addEventListener('DOMContentLoaded', function() {
    createParticles();
    createGridOverlay();
    setupScrollAnimations();
    setupNavHighlight();
    setupMobileMenu();
    setupProjectFilters();
});

function createParticles() {
    const container = document.querySelector('.particles-container');
    if (!container) return;

    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            width: ${Math.random() * 4 + 2}px;
            height: ${Math.random() * 4 + 2}px;
            left: ${Math.random() * 100}%;
            animation-delay: ${Math.random() * 8}s;
            animation-duration: ${Math.random() * 6 + 6}s;
        `;
        container.appendChild(particle);
    }
}

function createGridOverlay() {
    const grid = document.createElement('div');
    grid.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 60px 60px;
        pointer-events: none;
        z-index: -1;
    `;
    document.body.appendChild(grid);
}

function setupScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 60);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.project-card, .skill-category, .contact-card, .timeline-item, .edu-card, .achievement-card, .highlight-item, .info-card').forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
}

function setupNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('nav a[href^="#"]');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const top = section.offsetTop - 120;
            if (window.scrollY >= top) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.style.color = '';
            if (link.getAttribute('href') === '#' + current) {
                link.style.color = '#e4e4ef';
            }
        });
    });
}

function setupMobileMenu() {
    const btn = document.querySelector('.mobile-menu-btn');
    const menu = document.querySelector('nav ul');
    if (!btn || !menu) return;

    btn.addEventListener('click', () => {
        menu.classList.toggle('open');
    });

    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('open');
        });
    });
}

function setupProjectFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.project-card[data-category]');
    if (!filterBtns.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;

            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            cards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.classList.remove('hidden');
                    card.style.display = '';
                } else {
                    card.classList.add('hidden');
                }
            });
        });
    });
}
