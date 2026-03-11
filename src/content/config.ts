import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.string(),
    description: z.string().optional(),
    tags: z.array(z.string()).optional(),
  })
});

const pageCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    pubDate: z.string().optional(),
    description: z.string().optional(),
    tags: z.array(z.string()).optional(),
  })
});

const labArtsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    image: z.string(),
    pubDate: z.string().optional(),
    description: z.string().optional(),
  })
});

export const collections = {
  'blog': blogCollection,
  'page': pageCollection,
  'lab-arts': labArtsCollection,
};
