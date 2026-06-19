import fs from 'node:fs';
import path from 'node:path';

type Doc = {
  slug: string;
  title: string;
  language: string;
  category?: string;
  category_slug?: string;
  category_label?: string;
  sub_category?: string;
  sub_category_slug?: string;
  sub_category_label?: string;
  subcategory?: string;
  summary?: string;
  version?: string;
  published_on?: string;
  author?: string;
  seo_title?: string;
  seo_description?: string;
  canonical_url?: string;
  og_image?: string;
  noindex?: number | boolean;
  tags?: string[];
  body_md?: string;
  body_html?: string;
};

type AllDocsPayload = { docs: Doc[]; [k: string]: any };

const BASE =
  (typeof import.meta !== 'undefined' &&
    (import.meta as any).env &&
    (import.meta as any).env.PUBLIC_DOCS_API) ||
  process.env.DOCS_API_BASE ||
  'http://127.0.0.1:8000';

const LOCAL_API_HOSTS = new Set(['127.0.0.1', 'localhost']);
const SITE_NAME_HEADER = resolveBenchSiteName();

function normalizeUrl(path: string) {
  return `${BASE.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
}

function resolveBenchSiteName(): string | undefined {
  const explicitCandidates = [
    process.env.IFITWALA_DOC_SITE_NAME,
    process.env.FRAPPE_SITE,
    process.env.SITE_NAME,
  ];
  for (const candidate of explicitCandidates) {
    if (typeof candidate === 'string' && candidate.trim()) {
      return candidate.trim();
    }
  }

  let currentDir = process.cwd();
  for (let depth = 0; depth < 6; depth += 1) {
    const sitesDir = path.join(currentDir, 'sites');
    const commonConfig = path.join(sitesDir, 'common_site_config.json');
    if (fs.existsSync(commonConfig)) {
      try {
        const parsed = JSON.parse(fs.readFileSync(commonConfig, 'utf8'));
        if (typeof parsed?.default_site === 'string' && parsed.default_site.trim()) {
          return parsed.default_site.trim();
        }
      } catch {
        // Ignore malformed local config and continue searching.
      }
    }

    const currentSiteFile = path.join(sitesDir, 'currentsite.txt');
    if (fs.existsSync(currentSiteFile)) {
      try {
        const siteName = fs.readFileSync(currentSiteFile, 'utf8').trim();
        if (siteName) {
          return siteName;
        }
      } catch {
        // Ignore unreadable fallback files and continue searching.
      }
    }

    const parentDir = path.dirname(currentDir);
    if (parentDir === currentDir) {
      break;
    }
    currentDir = parentDir;
  }

  return undefined;
}

function maybeAttachSiteHeader(targetUrl: string, headers: Record<string, string>) {
  if (!SITE_NAME_HEADER) {
    return;
  }

  try {
    const hostname = new URL(targetUrl).hostname.toLowerCase();
    if (LOCAL_API_HOSTS.has(hostname)) {
      headers['X-Frappe-Site-Name'] = SITE_NAME_HEADER;
    }
  } catch {
    // Ignore invalid URLs and fall back to plain headers.
  }
}

function withCacheBust(url: string, token?: string) {
  const sep = url.includes('?') ? '&' : '?';
  const value = token || Date.now().toString(36);
  return `${url}${sep}__bust=${value}`;
}

async function fetchJSON(url: string, attempt = 1): Promise<any> {
  const headers: Record<string, string> = {
    'User-Agent': 'ifitwala-docs/astro-build',
    'Accept': 'application/json',
    'Cache-Control': 'no-cache, no-store',
    'Pragma': 'no-cache',
  };
  const targetUrl = withCacheBust(url, `${Date.now()}_${attempt}`);
  maybeAttachSiteHeader(targetUrl, headers);

  let res: Response;
  try {
    res = await fetch(targetUrl, { headers });
  } catch (error) {
    if (attempt < 3) {
      return fetchJSON(url, attempt + 1);
    }
    throw error;
  }

  if (res.status === 304 && attempt < 3) {
    return fetchJSON(url, attempt + 1);
  }

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`${targetUrl} -> ${res.status} ${res.statusText}
${text}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`Invalid JSON from ${targetUrl}`);
  }
}

function unwrap<T = any>(data: any): T {
  return data && typeof data === 'object' && 'message' in data ? data.message : data;
}

function normalizeLanguageValue(input: unknown): string | null {
  if (typeof input !== 'string') {
    return null;
  }
  const trimmed = input.trim();
  if (!trimmed) {
    return null;
  }
  return trimmed;
}

export async function getAllDocs(lang?: string): Promise<AllDocsPayload> {
  const qp = lang ? `?language=${encodeURIComponent(lang)}` : '';
  const raw = await fetchJSON(
    normalizeUrl(`/api/method/ifitwala_doc.api.docs.fetch_all${qp}`)
  );
  return unwrap<AllDocsPayload>(raw);
}

export async function getOneDoc(language: string, slug: string): Promise<Doc> {
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.fetch_one?language=${encodeURIComponent(
      language
    )}&slug=${encodeURIComponent(slug)}`
  );
  const raw = await fetchJSON(url);
  return unwrap<Doc>(raw);
}

export async function getCategories(language = 'en') {
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.get_categories?language=${encodeURIComponent(language)}`
  );
  const raw = await fetchJSON(url);
  return unwrap(raw) || [];
}

export async function getCategory(slug: string) {
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.get_category?slug=${encodeURIComponent(slug)}`
  );
  const raw = await fetchJSON(url);
  return unwrap(raw) || null;
}

export async function getDocsInCategory(language: string, category_slug: string) {
  const q = new URLSearchParams({ language, category_slug });
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.get_docs_in_category?${q.toString()}`
  );
  const raw = await fetchJSON(url);
  return unwrap(raw) || [];
}

export type SearchFilters = {
  language?: string;
  category?: string;
  subcategory?: string;
  tags?: string[];
  q?: string;
  published_after?: string;
  published_before?: string;
  author?: string;
};

export type SearchResult = Doc & { snippets?: string[] };

export type SearchResponse = {
  items: SearchResult[];
  facets?: Record<string, any>;
};

export async function searchDocs(filters: SearchFilters = {}): Promise<SearchResponse> {
  const params = new URLSearchParams();
  if (filters.language) params.set('language', filters.language);
  if (filters.category) params.set('category', filters.category);
  if (filters.subcategory) params.set('subcategory', filters.subcategory);
  if (filters.q) params.set('q', filters.q);
  if (filters.author) params.set('author', filters.author);
  if (filters.published_after) params.set('published_after', filters.published_after);
  if (filters.published_before) params.set('published_before', filters.published_before);
  if (Array.isArray(filters.tags)) {
    for (const tag of filters.tags) {
      if (typeof tag === 'string' && tag.trim()) {
        params.append('tags', tag.trim());
      }
    }
  }

  const suffix = params.toString() ? `?${params.toString()}` : '';
  const raw = await fetchJSON(normalizeUrl(`/api/method/ifitwala_doc.api.docs.search${suffix}`));
  const payload = unwrap<SearchResponse>(raw);
  if (!payload || typeof payload !== 'object') {
    return { items: [], facets: {} };
  }
  payload.items = Array.isArray(payload.items) ? payload.items : [];
  payload.facets = payload.facets && typeof payload.facets === 'object' ? payload.facets : {};
  return payload;
}

export async function getAvailableLanguages(): Promise<string[]> {
  try {
    const payload = await getAllDocs();
    const rawBucket = new Map<string, string>();
    const add = (value: unknown) => {
      const normalized = normalizeLanguageValue(value);
      if (!normalized) {
        return;
      }
      const key = normalized.toLowerCase();
      if (!rawBucket.has(key)) {
        rawBucket.set(key, normalized);
      }
    };

    const docs = Array.isArray(payload?.docs) ? payload.docs : [];
    for (const doc of docs) {
      add(doc?.language);
    }

    const fromPayload = (payload as any)?.languages;
    if (Array.isArray(fromPayload)) {
      for (const value of fromPayload) {
        add(value);
      }
    }

    const languages = Array.from(rawBucket.values()).sort((a, b) =>
      a.localeCompare(b)
    );
    return languages.length ? languages : ['en'];
  } catch (error) {
    return ['en'];
  }
}
