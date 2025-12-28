// Tech Anime Background Effects
document.addEventListener('DOMContentLoaded', function() {
    createVisibleParticles();
    createTechGrid();
    addGlowEffects();
});

// Create visible cyan particles
function createVisibleParticles() {
    const container = document.querySelector('.particles-container');
    
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            width: ${Math.random() * 6 + 2}px;
            height: ${Math.random() * 6 + 2}px;
            left: ${Math.random() * 100}%;
            animation-delay: ${Math.random() * 6}s;
            animation-duration: ${Math.random() * 4 + 4}s;
        `;
        container.appendChild(particle);
    }
}

// Create tech grid overlay
function createTechGrid() {
    const grid = document.createElement('div');
    grid.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: -1;
        animation: gridMove 20s linear infinite;
    `;
    document.body.appendChild(grid);
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
    `;
    document.head.appendChild(style);
}

// Add glow effects to cards
function addGlowEffects() {
    const cards = document.querySelectorAll('.project-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 0 30px rgba(0, 255, 255, 0.5), 0 20px 40px rgba(0, 0, 0, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.1)';
        });
    });
}