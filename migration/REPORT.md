# WordPress migration report

This report documents the initial WordPress migration. The subsequent [Google Scholar expansion](scholar/REPORT.md) increases the publication list to 57 records.

Migration date: **November 8, 2026**. Source: **https://swarmslab.com/**.
Destination: the `swarmslabpage` repository, using the [Cohen Lab website template](https://github.com/bchcohenlab/lab-website-template).

## Imported content

| Content | Result |
| --- | --- |
| People | 26 profiles: 1 PI, 4 current PhD students, 21 alumni/former members |
| Publications | 38 records: all 36 teachPress records plus the two 2025 papers linked from the homepage |
| Research | Three original project descriptions plus related blimp and environmental-monitoring publications |
| News | Eight homepage news items and the original media links |
| Videos | 25 distinct YouTube videos from the homepage, video page, and publication resources |
| Gallery | All 17 photographs/captions from the 2022 Robot Versatility Workshop gallery |
| Club | Description, activities, competitions, application form, GitHub, and four contact roles |
| Contact | Original lab email and Mountaintop street address; no invented telephone number |
| Local media | 95 downloaded images/attachments including the original wordmark |
| Original URL aliases | 10 static redirects |
| Output | 47 HTML pages, including profiles, aliases, and a 404 page |

The source WordPress posts endpoint returned an empty list. News lived on the homepage. WordPress also exposed many unused theme demonstration pages (prices, shopping, sample services, testimonials, etc.); they were excluded. Their slugs are recorded in `inventory.json`.

## Provenance

- `source/pages.json`: original public WordPress REST response, including rendered builder HTML and teachPress citations.
- `source/home.html`: original public homepage HTML.
- `source/posts.json`: public posts inventory (empty).
- `source/publications.bib`: original teachPress BibTeX blocks, unmodified.
- `inventory.json`: initial extraction counts and page scope (before the two additional 2025 papers and the logo).
- `assets.json`: original asset URL → local public path mapping, including the logo.
- `alumni-positions.md`: November 8, 2026 current-position audit of all 21 alumni, including sources, four profile updates, and unresolved entries.
- `publication-videos.json`: verified paper-to-YouTube associations and their sources. The publication lists display 26 YouTube links, including 16 added after the original import. Old gallery captions were not used to assign videos because several captions were mismatched.
- `asset-report.json`: download results for the initial 94 assets; the logo was downloaded separately.
- `scripts/import-wordpress.py`: one-time extraction script. Do not rerun on edited content.
- `scripts/download-assets.py`: repeatable asset downloader; skips existing downloads.

The two 2025 entries were linked on the WordPress homepage. Their exact titles, author lists, and ICRA acceptance were checked against the linked primary records: [Spinning Blimp](https://arxiv.org/abs/2503.04112) and [MochiSwarm](https://arxiv.org/abs/2503.03077). They link to those preprints; no conference DOI was guessed.

## Publication images

The publication list now displays a representative image beside each citation when a verified source is available. The 31 images attached to WordPress publication records retain their exact paper associations. Five older author-hosted images fill the remaining original publication-list records; the two homepage-linked papers also have images. Other thumbnails come from the corresponding papers, author manuscript figure files, or author/lab project and video pages.

See `publication-images.json` for each local asset, source URL, alt text, and extraction details. At the lab owner's request on November 8, 2026, two 2012 papers intentionally remain without images: **Improved algorithm for perimeter tracking in robotic sensor networks** and **A multi-agent model to control robotic sensor networks**. Image coverage is complete for the requested scope: 55 thumbnails and two approved exceptions.

Images are stored locally and optimized into responsive WebP files during the Astro build. The shared publication component uses an uncropped thumbnail beside the text on desktop and above it on phones. This applies to the publications page, homepage, research pages, and member profiles. The static-output check validates thumbnail presence and alt text, with only the two requested exceptions exempted.

## Editorial and technical decisions

- Kept the original Lehigh/SwarmsLab wordmark, using brown and gold with the template's serif/sans typography.
- Preserved the team page's current/alumni classifications. The separate Diego and Gustavo profile pages still described them as PhD students, while the team page listed their faculty destinations. Their new profiles use the newer roster information; older source biographies remain in the archived snapshot.
- Preserved names and publication author order. Author-to-profile links match surname plus first initial, including accented surnames and D’Antonio's apostrophe variants.
- Some alumni cards placed roles in body text instead of subtitles; those roles were carried into the new cards.
- Replaced Sebastian Ramirez's stock robot illustration with initials rather than treating it as a portrait.
- Added robotics topic tags from titles and source keywords. These are editorial organization, not new claims about publication metadata.
- Preserved source year, venue, abstracts, and resource links where available. Removed repeated DOI URL prefixes and used an arXiv link for the source's malformed `arXiv:2308.00259` DOI field. Filled blank/`nokey` BibTeX citation keys with unique slugs; original BibTeX remains in the source archive.
- Some original records have no DOI, external paper URL, or abstract. These omissions were preserved; this is a migration of the public website, not a complete bibliographic update through 2026.
- The WordPress teaching page contained an unrendered shortcode. The new Teaching page uses the courses explicitly listed on the club page.
- Migrated media remain at their downloaded `wp-content/uploads/...` paths. The hero, portraits, and gallery also receive optimized WebP variants. Fonts are bundled locally.
- Kept YouTube-hosted videos as lazy-loaded privacy-enhanced embeds with direct viewing links. External paper, press, form, and video links retain their external dependencies; not every third-party destination was audited.
- Removed sample people, publications, photographs, clinical copy, and unused clinical illustration. Kept the upstream MIT license and original template documentation.
- Upgraded Astro to a patched release and applied compatible dependency fixes. The final dependency audit reported **0 vulnerabilities**.
- Added base-aware URLs throughout. GitHub Actions reads the actual Pages origin/path; local defaults target `https://dsaldana.github.io/swarmslabpage/`. The custom-domain configuration builds with `https://swarmslab.com/`.

## Preserved WordPress routes

| Old URL path | New destination |
| --- | --- |
| `/team/` | `/people/` |
| `/projects/` | `/research/` |
| `/location/` | `/contact/` |
| `/david-saldana/` | `/people/david-saldana/` |
| `/diego-salazardantonio/` | `/people/diego-s-d-antonio/` |
| `/gustavo-cardona/` | `/people/gustavo-a-cardona/` |
| `/conference-publications/` | `/publications/?type=conference` |
| `/journals/` | `/publications/?type=journal` |
| `/mediavw2022/` | `/lab-life/` |
| `/home-02/` | `/` |

These are static HTML redirects compatible with GitHub Pages, with canonical destinations and fallback links. The main `/publications/`, `/videos/`, and `/club/` paths are retained. WordPress-specific tag IDs and pagination query strings are replaced by the new filters.

## Verification

- `npm run check`: 0 errors, warnings, or hints from Astro diagnostics.
- `npm run build`: successful production build.
- `npm run check:site`: all 47 HTML pages, 1,211 internal links/asset references, 38 publication records, 26 person profiles, 10 aliases, and all 95 mirrored media files validated.
- Built and ran those output checks both at `/swarmslabpage/` and at `/` with the custom domain.
- Inspected the homepage at desktop and mobile (390px) sizes in Firefox, plus the team page and gallery.
- Browser-tested mobile navigation expansion, publication search (1 result for “MochiSwarm”), the no-results state, filter reset (38 records restored), a legacy redirect, and the photo lightbox.

No live deployment, repository push, WordPress changes, or DNS changes were performed. See the root README for local preview and GitHub Pages deployment instructions.
