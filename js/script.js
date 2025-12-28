// Tech Anime Background Effects
document.addEventListener('DOMContentLoaded', function() {
    createParticles();
    createFloatingIcons();
    addScrollAnimations();
});

// Create animated particles
function createParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particles';
    particleContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    `;
    document.body.appendChild(particleContainer);

    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.style.cssText = `
            position: absolute;
            width: ${Math.random() * 4 + 1}px;
            height: ${Math.random() * 4 + 1}px;
            background: rgba(255, 255, 255, ${Math.random() * 0.5 + 0.2});
            border-radius: 50%;
            animation: float-particle ${Math.random() * 10 + 5}s linear infinite;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        particleContainer.appendChild(particle);
    }

    // Add particle animation CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float-particle {
            0% { transform: translateY(0px) translateX(0px) rotate(0deg); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-100vh) translateX(${Math.random() * 200 - 100}px) rotate(360deg); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// Create floating tech icons
function createFloatingIcons() {
    const icons = ['⚡', '🔧', '🚀', '💻', '🤖', '📊', '🔬', '⚙️'];
    const iconContainer = document.createElement('div');
    iconContainer.className = 'floating-icons';
    iconContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    `;
    document.body.appendChild(iconContainer);

    icons.forEach((icon, index) => {
        const floatingIcon = document.createElement('div');
        floatingIcon.textContent = icon;
        floatingIcon.style.cssText = `
            position: absolute;
            font-size: ${Math.random() * 20 + 15}px;
            opacity: 0.1;
            animation: float-icon ${Math.random() * 15 + 10}s ease-in-out infinite;
            left: ${Math.random() * 90}%;
            top: ${Math.random() * 90}%;
            animation-delay: ${index * 2}s;
        `;
        iconContainer.appendChild(floatingIcon);
    });

    // Add icon animation CSS
    const iconStyle = document.createElement('style');
    iconStyle.textContent = `
        @keyframes float-icon {
            0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.1; }
            25% { transform: translateY(-30px) rotate(90deg); opacity: 0.3; }
            50% { transform: translateY(-60px) rotate(180deg); opacity: 0.1; }
            75% { transform: translateY(-30px) rotate(270deg); opacity: 0.3; }
        }
    `;
    document.head.appendChild(iconStyle);
}

// Add scroll animations
function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
            }
        });
    }, observerOptions);

    // Observe project cards
    document.querySelectorAll('.project-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        observer.observe(card);
    });

    // Add fadeInUp animation
    const animationStyle = document.createElement('style');
    animationStyle.textContent = `
        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(animationStyle);
}

// Add glitch effect to title on hover
document.addEventListener('DOMContentLoaded', function() {
    const title = document.querySelector('nav h1');
    if (title) {
        title.addEventListener('mouseenter', function() {
            this.style.animation = 'glitch 0.5s ease-in-out';
        });
        
        title.addEventListener('animationend', function() {
            this.style.animation = '';
        });
    }

    // Add glitch animation CSS
    const glitchStyle = document.createElement('style');
    glitchStyle.textContent = `
        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
    `;
    document.head.appendChild(glitchStyle);
});