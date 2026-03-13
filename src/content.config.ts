import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ 
    pattern: '**/[^_]*.{md,mdx}', 
    base: "./src/content/blog",
    generateId: ({ entry }) => entry.replace(/\.[^/.]+$/, "")
  }),
  schema: z.object({
    title: z.string(),
    pubDate: z.string(),
    description: z.string().optional(),
    tags: z.array(z.string()).optional(),
  })
});

const page = defineCollection({
  loader: glob({ 
    pattern: '**/[^_]*.{md,mdx}', 
    base: "./src/content/page",
    generateId: ({ entry }) => entry.replace(/\.[^/.]+$/, "")
  }),
  schema: z.object({
    title: z.string(),
    pubDate: z.string().optional(),
    description: z.string().optional(),
    tags: z.array(z.string()).optional(),
  })
});

const labArts = defineCollection({
  loader: glob({ 
    pattern: '**/[^_]*.{md,mdx}', 
    base: "./src/content/lab-arts",
    generateId: ({ entry }) => entry.replace(/\.[^/.]+$/, "")
  }),
  schema: z.object({
    title: z.string(),
    image: z.string(),
    pubDate: z.string().optional(),
    description: z.string().optional(),
  })
});

export const collections = {
  'blog': blog,
  'page': page,
  'lab-arts': labArts,
};
