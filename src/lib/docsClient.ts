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

async function fetchJSON(url: string) {
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'ifitwala-docs/astro-build',
      'Accept': 'application/json',
    },
  });
  const text = await res.text();
  if (!res.ok) {
    console.error(`[docsClient] ${url} -> ${res.status} ${res.statusText}\n${text}`);
    throw new Error(`${url} -> ${res.status}`);
  }
  try {
    return JSON.parse(text);
  } catch {
    console.error(`[docsClient] Non-JSON at ${url}:\n${text}`);
    throw new Error(`Invalid JSON from ${url}`);
  }
}

function unwrap<T = any>(data: any): T {
  return data && typeof data === 'object' && 'message' in data ? data.message : data;
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
