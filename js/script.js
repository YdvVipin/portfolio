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

// Interactive test runner functionality
document.addEventListener('DOMContentLoaded', () => {
  const runBtn = document.getElementById('runTestsBtn');
  const statusDiv = document.getElementById('testStatus');
  const statusMsg = document.getElementById('statusMessage');
  const reportLink = document.getElementById('reportLink');
  
  if (!runBtn) return; // Only runs on project pages
  
  runBtn.addEventListener('click', async () => {
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Tests running...';
    statusDiv.style.display = 'block';
    statusMsg.textContent = 'Starting tests... (this may take 2-3 minutes)';
    reportLink.style.display = 'none';
    
    try {
      // Simulate test run - replace with actual GitHub Actions API call
      setTimeout(() => {
        statusMsg.textContent = '✅ Tests completed! Redirecting to results...';
        reportLink.href = 'https://github.com/YdvVipin/portfolio/actions';
        reportLink.textContent = '📊 View Test Results';
        reportLink.style.display = 'inline-block';
        
        setTimeout(() => {
          window.open('https://github.com/YdvVipin/portfolio/actions', '_blank');
        }, 2000);
      }, 3000);
      
    } catch (error) {
      statusMsg.textContent = '❌ Failed to trigger tests. Check console.';
      console.error(error);
    } finally {
      setTimeout(() => {
        runBtn.disabled = false;
        runBtn.textContent = '▶ Run Tests Now';
      }, 5000);
    }
  });
});