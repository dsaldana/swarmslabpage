# SwarmsLab website

The SwarmsLab website, migrated from WordPress to the [Cohen Lab website template](https://github.com/bchcohenlab/lab-website-template). Built with Astro and Tailwind CSS; outputs static HTML for GitHub Pages. No WordPress, database, or server is required.

## Run locally

Use Node.js 22.23.4 or newer (Node 24 recommended).

```sh
npm ci
npm run dev
```

Open **http://localhost:4321/swarmslabpage/**. The project path is intentional: it exercises the same links and assets used on GitHub Pages.

```sh
npm run check       # Astro and TypeScript diagnostics
npm run build       # Production website in dist/
npm run check:site  # Check built pages, local links, media, profiles, and publication counts
npm run check:scholar # Verify Scholar coverage and preservation of original records
npm run preview    # Serve the production build locally
```

## Deploy to GitHub Pages

The included workflow deploys `main` in `dsaldana/swarmslabpage`.

1. Push these files to the repository's `main` branch.
2. Open **Settings → Pages → Build and deployment → Source**, and select **GitHub Actions**.
3. In **Actions → Deploy to GitHub Pages**, choose **Run workflow** if the initial push ran before Pages was enabled.
4. Wait for the build and deployment jobs to succeed. The project URL is **https://dsaldana.github.io/swarmslabpage/**.

Each subsequent push to `main` rebuilds and deploys the website. The workflow reads the actual origin and base path from GitHub Pages, so it also supports a custom domain without source edits. Local creation of this project does not itself publish the website.

## Move swarmslab.com when ready

First validate the GitHub Pages version. Keep the existing WordPress hosting until the new version and its media are confirmed.

1. Verify your domain with GitHub if requested, then set **Settings → Pages → Custom domain** to `swarmslab.com`.
2. Configure the domain's DNS using [GitHub's current custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site). Preserve unrelated records, including email records.
3. Re-run the deploy workflow. It automatically builds with `https://swarmslab.com` and an empty base path. Enable **Enforce HTTPS** once GitHub provisions the certificate.

A `CNAME` file is not required for this Actions-based deployment. No DNS settings or live WordPress content were changed during this migration.

To validate a custom-domain build locally:

```sh
SITE_URL=https://swarmslab.com BASE_PATH=/ npm run build
BASE_PATH=/ npm run check:site
```

Run `npm run build` again afterward to return to the default GitHub project configuration.

## Edit content

| Content | Location |
| --- | --- |
| Lab identity, navigation, contact | `src/data/site.ts` |
| People and alumni | `src/content/people/*.md` |
| Publications, abstracts, BibTeX, paper/video links | `src/content/publications/*.md` |
| Research project descriptions | `src/data/projects.json` |
| Our Robots: names, years, descriptions, and associated paper IDs | `src/data/robots.json` |
| News | `src/data/news.json` |
| Video collection | `src/data/videos.json` |
| Workshop gallery | `src/content/gallery/*.md` |
| Club information | `src/pages/club.astro` |
| Homepage | `src/pages/index.astro` |
| Colors, fonts, shared styles | `src/styles/global.css` |
| Original WordPress URL redirects | `src/data/redirects.json` |

Follow an existing Markdown record when adding a person or publication. `npm run check` verifies frontmatter against `src/content.config.ts`. Research tags must match the vocabulary in that schema and `src/lib/content.ts`.

The Our Robots page sorts entries by their starting year. Each robot's `imagePaper` selects an existing publication image, and `papers` lists its associated publication IDs. Paper URLs and the first available YouTube resource are read from those publication records, so updates stay consistent across the site.

Put new images in `src/assets/` for Astro optimization, or in `public/` for files served directly. Imported photographs and PDFs retain their original `wp-content/uploads/...` paths to help preserve old media links. The website uses locally stored images and fonts; videos remain hosted on YouTube.

Publication records use `image` (a relative local path), `imageAlt` (a description of the image), and `imageSource` (the original source URL). Thumbnails appear wherever publications are listed, including research pages and member profiles. Astro generates responsive WebP versions; the layout preserves the entire image. Image provenance is recorded in `migration/publication-images.json`: 55 verified thumbnails, with two 2012 papers intentionally without images at the lab owner's request. These exceptions are recorded in the manifest's `withoutImages` list.

Use `withBase()` from `src/lib/paths.ts` for internal navigation and public-file URLs. This keeps links working at both `/swarmslabpage/` and `/`.

## Google Scholar publications

The publication list now includes all 57 entries from [David Saldaña’s Scholar profile](https://scholar.google.com/citations?user=VU1s_Z8AAAAJ), checked November 8, 2026. One duplicate chapter is consolidated, and the original website-only paper is retained: **57 publication records in total, including 19 additions**. Thesis, workshop, and technical-report entries are explicitly labeled.

See [migration/scholar/REPORT.md](migration/scholar/REPORT.md) for every addition, source mapping, duplicate decisions, and metadata corrections. Normal edits remain in Markdown. The Scholar importer uses the archived, reviewed snapshot; it is not a live synchronization job.

## Migration record

See [migration/REPORT.md](migration/REPORT.md) for source provenance, imported counts, old URL mappings, and content limitations. The original public WordPress JSON and HTML are retained under `migration/source/` for comparison. They are not copied into the deployed `dist/` site.

The initial importer and asset downloader are retained for reproducibility. **Do not rerun the importer over edited content**: it resets the content collections and regenerates the initial import. Normal maintenance is done by editing Markdown and JSON.

The optional upstream ORCID and citation scripts remain available; no automatic citation-refresh workflow is enabled, and no citation counts or author identifiers have been invented.

## Attribution

Based on the Cohen Lab template at commit `877ee317337e5b077414e59c45070b346f5dfa30`, used under the included MIT license. The template's original documentation is preserved under `docs/TEMPLATE-*.md`. This migration retains the template's content collections, profile system, gallery lightbox, typography, Tailwind styling, and static-site architecture, customized for SwarmsLab. Astro was updated to a patched release during the migration.
