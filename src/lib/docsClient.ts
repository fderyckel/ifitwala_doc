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
