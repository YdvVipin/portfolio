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

// Subtle particle system
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

  for (let i = 0; i < 20; i++) {
    const particle = document.createElement('div');
    particle.style.position = 'absolute';
    particle.style.width = '1px';
    particle.style.height = '1px';
    particle.style.background = '#ffffff';
    particle.style.borderRadius = '50%';
    particle.style.opacity = '0.1';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animation = `float ${4 + Math.random() * 2}s ease-in-out infinite`;
    particleContainer.appendChild(particle);
  }
}

// Add floating animation
const style = document.createElement('style');
style.textContent = `
  @keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
  }
`;
document.head.appendChild(style);

// Interactive test runner functionality
document.addEventListener('DOMContentLoaded', () => {
  // Create subtle particles
  createParticles();
  
  // Test runner functionality
  const runBtn = document.getElementById('runTestsBtn');
  const statusDiv = document.getElementById('testStatus');
  const statusMsg = document.getElementById('statusMessage');
  const reportLink = document.getElementById('reportLink');
  
  if (!runBtn) return;
  
  runBtn.addEventListener('click', async () => {
    runBtn.disabled = true;
    runBtn.innerHTML = '⚡ Running Tests...';
    statusDiv.style.display = 'block';
    statusMsg.innerHTML = '🚀 <span style="color: #3498db;">Initializing test suite...</span>';
    reportLink.style.display = 'none';
    
    // Simulate test phases
    const phases = [
      '🔧 Setting up test environment...',
      '📡 Connecting to servers...',
      '🤖 Running automation suite...',
      '📊 Analyzing results...'
    ];
    
    for (let i = 0; i < phases.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      statusMsg.innerHTML = `<span style="color: #3498db;">${phases[i]}</span>`;
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    statusMsg.innerHTML = '✅ <span style="color: #27ae60; font-weight: bold;">Tests completed successfully!</span>';
    reportLink.href = 'https://github.com/YdvVipin/portfolio/actions';
    reportLink.innerHTML = '📊 View Results';
    reportLink.style.display = 'inline-block';
    
    setTimeout(() => {
      window.open('https://github.com/YdvVipin/portfolio/actions', '_blank');
    }, 2000);
    
    setTimeout(() => {
      runBtn.disabled = false;
      runBtn.innerHTML = '▶ Run Tests Now';
    }, 5000);
  });
});