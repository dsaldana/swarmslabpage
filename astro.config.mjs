import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// GitHub Actions supplies the actual Pages origin/base, including custom domains.
// Defaults also make the local build work at this repository's project URL.
export default defineConfig({
  site: process.env.SITE_URL || 'https://dsaldana.github.io',
  base: process.env.BASE_PATH ?? '/swarmslabpage',
  trailingSlash: 'always',
  vite: { plugins: [tailwindcss()] },
  integrations: [sitemap()],
});
