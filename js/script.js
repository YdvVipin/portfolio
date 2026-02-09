const GITHUB_USERNAME = 'YdvVipin';
const GITHUB_API = 'https://api.github.com';

document.addEventListener('DOMContentLoaded', function() {
    setupScrollAnimations();
    setupParallax();
    setupSmoothScroll();
    loadGitHubData();
});

// ─── GitHub API ──────────────────────────────────────

async function loadGitHubData() {
    try {
        const [profile, repos] = await Promise.all([
            fetchJSON(`${GITHUB_API}/users/${GITHUB_USERNAME}`),
            fetchJSON(`${GITHUB_API}/users/${GITHUB_USERNAME}/repos?per_page=100&sort=updated`)
        ]);

        renderProfileStats(profile);
        renderRepos(repos);

        // Fetch languages for each repo in parallel
        const langPromises = repos.map(repo =>
            fetchJSON(repo.languages_url).then(langs => ({ name: repo.name, langs }))
        );
        const langResults = await Promise.all(langPromises);
        const langMap = {};
        langResults.forEach(r => { langMap[r.name] = r.langs; });
        updateRepoLanguages(langMap);

    } catch (err) {
        console.error('GitHub API error:', err);
        showAPIError();
    }
}

async function fetchJSON(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

function renderProfileStats(profile) {
    const container = document.getElementById('github-stats');
    if (!container) return;

    container.innerHTML = `
        <div class="gh-stat">
            <span class="gh-stat-value">${profile.public_repos}</span>
            <span class="gh-stat-label">Repositories</span>
        </div>
        <div class="gh-stat">
            <span class="gh-stat-value">${profile.followers}</span>
            <span class="gh-stat-label">Followers</span>
        </div>
        <div class="gh-stat">
            <span class="gh-stat-value">${profile.following}</span>
            <span class="gh-stat-label">Following</span>
        </div>
    `;
    container.classList.add('loaded');
}

function renderRepos(repos) {
    const grid = document.getElementById('repo-grid');
    if (!grid) return;

    // Remove loading skeleton
    grid.innerHTML = '';

    const filtered = repos.filter(r => !r.fork);

    if (filtered.length === 0) {
        grid.innerHTML = '<p class="gh-empty">No public repositories found.</p>';
        return;
    }

    filtered.forEach((repo, i) => {
        const card = document.createElement('a');
        card.href = repo.html_url;
        card.target = '_blank';
        card.rel = 'noopener noreferrer';
        card.className = 'repo-card fade-target';
        card.style.animationDelay = `${i * 0.08}s`;

        const updated = new Date(repo.updated_at);
        const timeAgo = getTimeAgo(updated);

        card.innerHTML = `
            <div class="repo-card-header">
                <svg class="repo-icon" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
                    <path d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/>
                </svg>
                <h3 class="repo-name">${repo.name}</h3>
            </div>
            <p class="repo-desc">${repo.description || 'No description provided'}</p>
            <div class="repo-meta">
                <div class="repo-lang" data-repo="${repo.name}">
                    ${repo.language ? `<span class="lang-dot" style="background:${getLangColor(repo.language)}"></span><span>${repo.language}</span>` : ''}
                </div>
                <div class="repo-stats">
                    ${repo.stargazers_count > 0 ? `
                        <span class="repo-stat">
                            <svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>
                            ${repo.stargazers_count}
                        </span>
                    ` : ''}
                    ${repo.forks_count > 0 ? `
                        <span class="repo-stat">
                            <svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 0-1.5 0v.878a.25.25 0 0 1-.25.25h-1.5V2.25a.75.75 0 0 0-1.5 0v4.25h-1.5a.25.25 0 0 1-.25-.25v-.878a2.25 2.25 0 1 0-1.5 0ZM7.25 1.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM5 12.75v.878a2.25 2.25 0 1 0 1.5 0v-.878a.25.25 0 0 1 .25-.25h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 0-1.5 0v.878a.25.25 0 0 1-.25.25h-4.5a.75.75 0 0 0-.75.75Z"/></svg>
                            ${repo.forks_count}
                        </span>
                    ` : ''}
                    <span class="repo-stat repo-size">
                        ${formatSize(repo.size)}
                    </span>
                </div>
            </div>
            <div class="repo-footer">
                <span class="repo-updated">Updated ${timeAgo}</span>
            </div>
        `;

        grid.appendChild(card);
    });

    // Re-observe new fade targets
    setupScrollAnimations();
}

function updateRepoLanguages(langMap) {
    Object.entries(langMap).forEach(([repoName, langs]) => {
        const el = document.querySelector(`.repo-lang[data-repo="${repoName}"]`);
        if (!el || !langs || Object.keys(langs).length === 0) return;

        const total = Object.values(langs).reduce((a, b) => a + b, 0);
        const entries = Object.entries(langs).slice(0, 4);

        // Build language bar
        const barHTML = `<div class="lang-bar">${entries.map(([lang, bytes]) => {
            const pct = ((bytes / total) * 100).toFixed(1);
            return `<div class="lang-bar-segment" style="width:${pct}%;background:${getLangColor(lang)}" title="${lang} ${pct}%"></div>`;
        }).join('')}</div>`;

        const labelsHTML = entries.map(([lang, bytes]) => {
            const pct = ((bytes / total) * 100).toFixed(1);
            return `<span class="lang-label"><span class="lang-dot" style="background:${getLangColor(lang)}"></span>${lang} <span class="lang-pct">${pct}%</span></span>`;
        }).join('');

        el.innerHTML = barHTML + `<div class="lang-labels">${labelsHTML}</div>`;
    });
}

function showAPIError() {
    const grid = document.getElementById('repo-grid');
    if (grid) {
        grid.innerHTML = '<p class="gh-error">Unable to load repositories. GitHub API rate limit may be exceeded.</p>';
    }
}

// ─── Helpers ──────────────────────────────────────

function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    const intervals = [
        { label: 'year', seconds: 31536000 },
        { label: 'month', seconds: 2592000 },
        { label: 'week', seconds: 604800 },
        { label: 'day', seconds: 86400 },
        { label: 'hour', seconds: 3600 },
    ];
    for (const interval of intervals) {
        const count = Math.floor(seconds / interval.seconds);
        if (count >= 1) return `${count} ${interval.label}${count > 1 ? 's' : ''} ago`;
    }
    return 'just now';
}

function formatSize(kb) {
    if (kb >= 1024) return `${(kb / 1024).toFixed(1)} MB`;
    return `${kb} KB`;
}

const LANG_COLORS = {
    JavaScript: '#f1e05a', TypeScript: '#3178c6', Python: '#3572A5',
    HTML: '#e34c26', CSS: '#563d7c', Java: '#b07219', 'C#': '#178600',
    Ruby: '#701516', Go: '#00ADD8', Rust: '#dea584', PHP: '#4F5D95',
    Swift: '#F05138', Kotlin: '#A97BFF', Shell: '#89e051', Dart: '#00B4AB',
    'Jupyter Notebook': '#DA5B0B', Vue: '#41b883', Dockerfile: '#384d54',
    SCSS: '#c6538c', Makefile: '#427819',
};

function getLangColor(lang) {
    return LANG_COLORS[lang] || '#8b949e';
}

// ─── UI Setup ──────────────────────────────────────

function setupScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.fade-target:not(.visible)').forEach(el => {
        observer.observe(el);
    });
}

function setupParallax() {
    const patternBg = document.querySelector('.pattern-bg');
    if (!patternBg) return;

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        patternBg.style.transform = `translateY(${scrolled * 0.3}px)`;
    }, { passive: true });
}

function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
}
