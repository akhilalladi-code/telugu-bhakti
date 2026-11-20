# Telugu Bhakti — Development Rules

## Product
A Telugu devotional lyrics library. Prioritise complete, readable song lyrics and song discovery. Do not turn song pages into meaning-first articles.

## Design system
- Preserve the warm parchment, forest-green and saffron visual identity.
- Use Anek Telugu for the website UI and Ramabhadra for Telugu song lyrics.
- Keep layouts responsive, keyboard-accessible and readable on mobile.
- Reuse the shared stylesheet and site JavaScript.

## Content integrity
- Never invent lyrics, authorship, sources, recording details or copyright status.
- Only publish full lyrics supplied by the project owner or cleared for publication.
- Preserve user-supplied wording unless asked to proofread.
- Do not add source notes or rights disclaimers to the Kasturi page unless explicitly requested.
- A song must not appear in the search index unless its page exists and its content has been reviewed.

## Technical constraints
- Static HTML/CSS/vanilla JavaScript; GitHub Pages hosting.
- No backend, paid API, Webflow CMS, Replit or unnecessary dependencies.
- Use relative asset paths so project pages work under the GitHub Pages subpath.
- Keep sitemap and robots.txt aligned with published pages.
- Do not add secrets or credentials to the repository.

## Verification
Before proposing a merge:
1. Run `python scripts/check_site.py`.
2. Run `node --check assets/site.js`.
3. Inspect the complete diff.
4. Verify all internal links, metadata and search results.
5. Never claim live behaviour has been tested unless it was tested in a browser.
