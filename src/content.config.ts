import { defineCollection, reference } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "zod";

/*
  Content collections for the lab site (Astro 6 Content Layer API).

  Content lives in src/content/<collection>/*.md so a CMS (Sveltia/Decap) can
  layer on later with no schema change.
  Safety defaults fail closed: figures default to rightsConfirmed:false and are
  filtered out of every figure query, so a half-filled record can never leak.
*/

// People — bio lives in the markdown body (use render()).
const people = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/people" }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      status: z.enum(["current", "alumni"]),
      group: z.enum([
        "Faculty",
        "Researchers",
        "Staff",
        "Students",
        "Affiliates",
        "Alumni",
      ]),
      role: z.string(),
      title: z.string().optional(),
      headshot: image().optional(),
      links: z
        .object({
          email: z.email().optional(),
          twitter: z.url().optional(),
          scholar: z.url().optional(),
          orcid: z.url().optional(),
          linkedin: z.url().optional(),
          website: z.url().optional(),
        })
        .default({}),
      order: z.number().default(0),
      featured: z.boolean().default(false),
    }),
});

// Publications — frontmatter only (any markdown body is optional notes).
const publications = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/publications" }),
  schema: ({ image }) => z.object({
    title: z.string(),
    image: image().optional(),
    imageAlt: z.string().optional(),
    imageSource: z.url().optional(),
    authors: z.array(z.string()),
    year: z.number(),
    journal: z.string().optional(),
    doi: z.string().optional(),
    pages: z.string().optional(),
    volume: z.string().optional(),
    issue: z.string().optional(),
    pmid: z.string().optional(),
    pmcid: z.string().optional(),
    url: z.url().optional(),
    scholarUrl: z.url().optional(),
    scholarIds: z.array(z.string()).default([]),
    scholarChecked: z.string().optional(),
    metadataSources: z.array(z.url()).default([]),
    publicationNote: z.string().optional(),
    citations: z.number().optional(),
    isMenteePaper: z.boolean().default(false),
    menteeFirstAuthor: z.boolean().default(false),
    // The lab PI is first or last (senior) author.
    piFirstOrSenior: z.boolean().default(false),
    featured: z.boolean().default(false),
    openAccess: z.boolean().default(false),
    publicationType: z.enum(["journal", "conference", "chapter", "thesis", "workshop", "report", "other"]).default("other"),
    resources: z.array(z.object({ label: z.string(), url: z.string() })).default([]),
    abstract: z.string().default(""),
    bibtex: z.string().default(""),
    areas: z.array(z.enum(["modular-robots", "aerial-manipulation", "resilient-swarms", "environmental-monitoring", "robotic-blimps", "robot-learning", "review", "letter"])).default([]),
  }),
});

// Figures — gated by rightsConfirmed (hard gate, defaults closed).
const figures = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/figures", }),
  schema: ({ image }) =>
    z.object({
      image: image(),
      paper: reference("publications"),
      caption: z.string(),
      citation: z.string(),
      doi: z.string().optional(),
      pmid: z.string().optional(),
      journal: z.string().optional(),
      license: z.enum([
        "CC-BY",
        "CC-BY-SA",
        "CC0",
        "publisher-permission",
        "unknown",
      ]),
      licenseUrl: z.url().optional(),
      // Hard gate: only true figures are ever rendered.
      rightsConfirmed: z.boolean().default(false),
      order: z.number().default(0),
    }),
});

// Gallery — lab-life photos.
const gallery = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/gallery" }),
  schema: ({ image }) =>
    z.object({
      image: image(),
      caption: z.string(),
      date: z.coerce.date(),
      people: z.array(z.string()).optional(),
      featured: z.boolean().default(false),
    }),
});

export const collections = { people, publications, figures, gallery };
