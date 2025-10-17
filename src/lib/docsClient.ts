type Doc = {
  slug: string;
  title: string;
  language: string;
  category?: string;
  sub_category?: string;
  summary?: string;
  version?: string;
  published_on?: string;
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

function normalizeUrl(path: string) {
  return `${BASE.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
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
  };
  // On retries we force upstream caches to refresh.
  const targetUrl = attempt === 1 ? url : withCacheBust(url, `${Date.now()}_${attempt}`);
  if (attempt > 1) {
    headers['Cache-Control'] = 'no-cache, no-store';
    headers['Pragma'] = 'no-cache';
  }

  let res: Response;
  try {
    res = await fetch(targetUrl, { headers });
  } catch (error) {
    if (attempt < 3) {
      console.warn(`[docsClient] ${targetUrl} fetch failed (${error}). Retrying without cache.`);
      return fetchJSON(url, attempt + 1);
    }
    console.error(`[docsClient] ${targetUrl} fetch failed after ${attempt} attempts.`, error);
    throw error;
  }

  // Some reverse proxies may answer 304 when ETag matches; retry once bypassing cache.
  if (res.status === 304 && attempt < 3) {
    console.warn(`[docsClient] ${targetUrl} -> 304 Not Modified. Retrying without cache.`);
    return fetchJSON(url, attempt + 1);
  }

  const text = await res.text();
  if (!res.ok) {
    console.error(`[docsClient] ${targetUrl} -> ${res.status} ${res.statusText}\n${text}`);
    throw new Error(`${targetUrl} -> ${res.status}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    console.error(`[docsClient] Non-JSON at ${targetUrl}:\n${text}`);
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
  const payload = unwrap<AllDocsPayload>(raw);
  const docs = Array.isArray(payload?.docs) ? payload.docs : [];
  console.log(`[docsClient] getAllDocs(${lang || 'all'}) -> ${docs.length}`);
  return payload;
}

export async function getOneDoc(language: string, slug: string): Promise<Doc> {
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.fetch_one?language=${encodeURIComponent(
      language
    )}&slug=${encodeURIComponent(slug)}`
  );
  const raw = await fetchJSON(url);
  const doc = unwrap<Doc>(raw);
  console.log(`[docsClient] getOneDoc(${language}, ${slug}) -> ${doc ? 'hit' : 'miss'}`);
  return doc;
}


export async function getCategories(language = 'en') {
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.get_categories?language=${encodeURIComponent(language)}`
  );
  const raw = await fetchJSON(url);
  const categories = unwrap(raw) || [];
  console.log(`[docsClient] getCategories(${language}) -> ${Array.isArray(categories) ? categories.length : 0}`);
  return categories;
}

export async function getCategory(slug: string) {
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.get_category?slug=${encodeURIComponent(slug)}`
  );
  const raw = await fetchJSON(url);
  const category = unwrap(raw) || null;
  console.log(`[docsClient] getCategory(${slug}) -> ${category ? 'hit' : 'miss'}`);
  return category;
}

export async function getDocsInCategory(language: string, category_slug: string) {
  const q = new URLSearchParams({ language, category_slug });
  const url = normalizeUrl(
    `/api/method/ifitwala_doc.api.docs.get_docs_in_category?${q.toString()}`
  );
  const raw = await fetchJSON(url);
  const docs = unwrap(raw) || [];
  console.log(`[docsClient] getDocsInCategory(${language}, ${category_slug}) -> ${Array.isArray(docs) ? docs.length : 0}`);
  return docs;
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
    console.log(`[docsClient] getAvailableLanguages -> ${languages.join(', ') || '<none>'}`);
    return languages.length ? languages : ['en'];
  } catch (error) {
    console.warn('[docsClient] Failed to detect languages from docs payload.', error);
    return ['en'];
  }
}
