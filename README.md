# Telugu Bhakti

A static Telugu devotional lyrics library with searchable song listings, full song pages, copy/print tools and deity/category collections.

## Planned live URL

https://akhilalladi-code.github.io/telugu-bhakti/

## Development

- Read `AGENTS.md` before making changes.
- Search index: `data/songs.json`.
- Run `node --check assets/site.js` and `python scripts/check_site.py` before submitting changes.
- Pull requests to `main` run quality checks. Production deployment runs only after checks pass on `main`.

## Structure

- `/` — Home and devotional collections
- `/kasturi-ranga-ranga-lyrics/` — Featured song guide
- `/krishna/`, `/rama/`, `/shiva/`, `/devi/`, `/vinayaka/` — Deity collections
- `/bhajans/`, `/stotras/`, `/deities/` — Content hubs
- `/about/`, `/contact/`, `/privacy/`, `/terms/`, `/faq/` — Site information
- `/404.html` — Not-found page

## SEO foundation

Semantic HTML, Telugu language metadata, page titles and descriptions, canonical URLs, Open Graph metadata, structured data, XML sitemap, robots.txt and contextual internal links.

## Editorial standards

Do not publish unverified lyrics or reproduce copyrighted song text without permission. Verify the exact recording, source, author/rights status and regional text variants before adding full lyrics. Prefer original explanations and meaning notes where full reproduction is not authorized.

## Deployment

The GitHub Actions workflow deploys this static site on pushes to `main`. In repository **Settings → Pages**, set **Build and deployment → Source** to **GitHub Actions** if Pages is not already configured.