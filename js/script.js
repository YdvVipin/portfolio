// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Matrix rain effect
function createMatrixRain() {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  canvas.style.position = 'fixed';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  canvas.style.pointerEvents = 'none';
  canvas.style.zIndex = '-1';
  canvas.style.opacity = '0.1';
  document.body.appendChild(canvas);

  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
  const charArray = chars.split('');
  const fontSize = 14;
  const columns = canvas.width / fontSize;
  const drops = [];

  for (let i = 0; i < columns; i++) {
    drops[i] = 1;
  }

  function draw() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#00ff00';
    ctx.font = fontSize + 'px monospace';
    
    for (let i = 0; i < drops.length; i++) {
      const text = charArray[Math.floor(Math.random() * charArray.length)];
      ctx.fillText(text, i * fontSize, drops[i] * fontSize);
      
      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }
  }

  setInterval(draw, 50);
}

// Particle system
function createParticles() {
  const particleContainer = document.createElement('div');
  particleContainer.style.position = 'fixed';
  particleContainer.style.top = '0';
  particleContainer.style.left = '0';
  particleContainer.style.width = '100%';
  particleContainer.style.height = '100%';
  particleContainer.style.pointerEvents = 'none';
  particleContainer.style.zIndex = '-1';
  document.body.appendChild(particleContainer);

  for (let i = 0; i < 50; i++) {
    const particle = document.createElement('div');
    particle.style.position = 'absolute';
    particle.style.width = '2px';
    particle.style.height = '2px';
    particle.style.background = '#ffffff';
    particle.style.borderRadius = '50%';
    particle.style.opacity = Math.random();
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animation = `float ${3 + Math.random() * 4}s ease-in-out infinite`;
    particleContainer.appendChild(particle);
  }
}

// Add floating animation
const style = document.createElement('style');
style.textContent = `
  @keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-10px) rotate(120deg); }
    66% { transform: translateY(5px) rotate(240deg); }
  }
`;
document.head.appendChild(style);

// Interactive test runner functionality
document.addEventListener('DOMContentLoaded', () => {
  // Create matrix effect
  createMatrixRain();
  createParticles();
  
  // Add typing effect to hero text
  const heroText = document.querySelector('.hero h2');
  if (heroText) {
    const text = heroText.textContent;
    heroText.textContent = '';
    let i = 0;
    const typeWriter = () => {
      if (i < text.length) {
        heroText.textContent += text.charAt(i);
        i++;
        setTimeout(typeWriter, 100);
      }
    };
    setTimeout(typeWriter, 1000);
  }
  
  // Test runner functionality
  const runBtn = document.getElementById('runTestsBtn');
  const statusDiv = document.getElementById('testStatus');
  const statusMsg = document.getElementById('statusMessage');
  const reportLink = document.getElementById('reportLink');
  
  if (!runBtn) return;
  
  runBtn.addEventListener('click', async () => {
    runBtn.disabled = true;
    runBtn.innerHTML = '⚡ <span style="animation: pulse 1s infinite;">INITIALIZING...</span>';
    statusDiv.style.display = 'block';
    statusMsg.innerHTML = '🚀 <span style="color: #00ff00;">BOOTING TEST MATRIX...</span>';
    reportLink.style.display = 'none';
    
    // Simulate test phases
    const phases = [
      '🔧 Configuring test environment...',
      '📡 Connecting to test servers...',
      '🤖 Deploying test bots...',
      '⚡ Running automation suite...',
      '📊 Analyzing results...'
    ];
    
    for (let i = 0; i < phases.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 800));
      statusMsg.innerHTML = `<span style="color: #00ff00; text-shadow: 0 0 10px #00ff00;">${phases[i]}</span>`;
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    statusMsg.innerHTML = '✅ <span style="color: #00ff00; font-weight: bold; text-shadow: 0 0 15px #00ff00;">TESTS COMPLETED! REDIRECTING TO MATRIX...</span>';
    reportLink.href = 'https://github.com/YdvVipin/portfolio/actions';
    reportLink.innerHTML = '🎯 <span style="animation: glow 1s infinite;">ACCESS RESULTS</span>';
    reportLink.style.display = 'inline-block';
    
    setTimeout(() => {
      window.open('https://github.com/YdvVipin/portfolio/actions', '_blank');
    }, 2000);
    
    setTimeout(() => {
      runBtn.disabled = false;
      runBtn.innerHTML = '▶ RUN TESTS NOW';
    }, 5000);
  });
  
  // Add hover effects to project cards
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-10px) scale(1.02)';
      card.style.boxShadow = '0 20px 40px rgba(102, 126, 234, 0.3)';
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0) scale(1)';
      card.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';
    });
  });
});