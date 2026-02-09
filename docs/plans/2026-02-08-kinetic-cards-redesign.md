# Portfolio Redesign: Kinetic Cards

Complete visual overhaul of the portfolio with an interactive, playful, light-themed multi-page design.

## Design Direction

Interactive and playful on a clean, light canvas. Every element responds to user interaction. 3D card tilts on hover, animated gradient blobs, scroll-triggered entrances, and smooth filter transitions. No heavy JS libraries — CSS-first with vanilla JS.

## Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| Background | `#FAFAFA` | Page background |
| Surface | `#FFFFFF` | Cards, inputs |
| Text primary | `#1A1A2E` | Headings, body |
| Text secondary | `#94A3B8` | Muted text, labels |
| Accent | `#6366F1` | CTAs, active states, highlights |
| Accent secondary | `#EC4899` | Tags, small details |
| Border | `#E2E8F0` | Card borders, dividers |

## Typography

- **Headings:** Space Grotesk (Google Fonts), 700/800 weight
- **Body:** Inter (Google Fonts), 400/500 weight
- **Monospace:** JetBrains Mono (for code/tech references)

## Site Architecture

Four pages, all sharing a common nav and footer:

1. **Home** (`index.html`) — Hero + featured projects + quick stats
2. **Projects** (`pages/projects.html`) — Full project gallery with filters
3. **About** (`pages/about.html`) — Timeline, skills, education
4. **Contact** (`pages/contact.html`) — Contact form + socials

### Navigation

- Sticky top bar with frosted-glass backdrop blur on white
- Logo/name left, page links right
- Active page indicator: animated sliding underline
- Shrinks from 80px to 64px on scroll
- Mobile: hamburger menu opening full-screen overlay with staggered link animations

### Footer

- Shared across all pages
- Social links (LinkedIn, GitHub, Email, Phone, Location)
- Brief tagline
- "Back to top" smooth scroll button

## Page Designs

### Home Page

**Hero (full viewport):**
- Left: Bold headline ("I Build Intelligent QA Systems"), 72-96px Space Grotesk. Key phrase in accent color. 1-2 line subtitle. Two pill CTA buttons ("View Projects", "Get In Touch") with hover lift animations.
- Right: Animated gradient blob — soft organic shape cycling through blob morphs via CSS `border-radius` animation in accent color palette.

**Featured Projects (below hero):**
- Grid of 4-6 kinetic cards showing top projects
- 3D tilt effect on hover (CSS `perspective` + `transform: rotateX/Y` driven by mouse position via JS)
- Each card: project name, one-liner, 2-3 tech tags, link to detail page

**Quick Stats Bar:**
- Horizontal row of 3-4 animated counters
- Stats: repos, years experience, projects built, lines of code
- Count-up animation triggered on scroll into view
- White cards with accent-colored numbers

### Projects Page

**Top area:**
- Page title "The Work" with GitHub live stats subtitle (repo count)
- Filter bar: pill-shaped toggle buttons for categories (All, AI Platforms, QA Frameworks, Data & Intelligence, AI/ML)
- Filter transitions: cards animate out/in with scale + fade

**Project grid:**
- Responsive CSS Grid with `auto-fill`
- Shows all 11 local project showcases + GitHub API repos
- GitHub repos distinguished with GitHub icon badge + language bar
- Each card: name, description, tech tags, "View Details" arrow
- 3D tilt hover effect
- FLIP-style animation on filter change

**Links:**
- 11 showcase cards link to existing `projects/*/index.html` detail pages
- GitHub repo cards link to GitHub

### About Page

**Intro section:**
- Personal intro paragraph (name, Toronto, positioning statement)
- Subtle animated gradient accent beside text

**Career Timeline:**
- Vertical timeline on left edge with connected dots
- Entries: Bright Order Inc. (current, pulsing indicator), Sofbang LLC, OPPO Mobiles, Mobilecomm Technologies
- Each entry: company, role, dates, 2-3 bullets
- Scroll-triggered fade + slide-from-left entrance

**Skills Grid:**
- 8 category cards with 3D tilt effect
- Categories: Languages, Frameworks, Testing, AI/ML, DevOps, Databases, Tools, Cloud
- Each card lists technologies

**Education & Achievements:**
- Two side-by-side cards
- Education: PGD Computer Programming (Seneca College), B.Tech IT (IIMT College)
- Achievements/certifications

### Contact Page

- Heading: "Let's Build Something"
- Functional contact form (Name, Email, Message) via Formspree
- Accent color focus states on inputs
- Social icons row below form with hover animations
- Subtle animated gradient accent in background corner

## Interaction System

All interactions are CSS-first with minimal vanilla JS:

1. **3D card tilt** — Mouse-driven `perspective` + `rotateX/Y` transforms. ~30 lines of JS.
2. **Gradient blobs** — CSS `@keyframes` animating `border-radius` percentages. Pure CSS.
3. **Scroll entrances** — IntersectionObserver + CSS transitions (fade + translateY). ~15 lines of JS.
4. **Counter animations** — requestAnimationFrame count-up on intersection. ~20 lines of JS.
5. **Filter transitions** — CSS transitions on opacity/transform + JS class toggling. ~30 lines of JS.
6. **Hover lifts** — Pure CSS `transform: translateY(-4px)` + `box-shadow` increase.
7. **Nav scroll shrink** — Scroll listener + CSS transition on height. ~10 lines of JS.

Total custom JS: ~200 lines for interactions + GitHub API fetching.

## Technical Constraints

- Pure HTML/CSS/JS — no build tools, no frameworks
- Google Fonts loaded via `<link>`
- GitHub API for live repo data (same as current)
- Formspree for contact form submission
- Existing 11 project detail pages under `projects/` remain unchanged
- Mobile responsive (breakpoints: 768px, 1024px)
- All animations respect `prefers-reduced-motion`

## File Structure

```
Portfolio/
  index.html              # Home page
  pages/
    projects.html          # Projects page
    about.html             # About page
    contact.html           # Contact page
  css/
    style.css              # All styles
  js/
    script.js              # All JS (interactions + GitHub API)
  projects/                # Existing detail pages (unchanged)
    ai-enabled-qa/
    playwright-bdd-framework/
    ...
```
