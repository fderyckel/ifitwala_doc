const BASE = process.env.DOCS_API_BASE || 'http://127.0.0.1:8000';
const USER_AGENT = 'astro-build';

function logWarn(message: string, error?: unknown) {
  const details = error instanceof Error ? error.message : error;
  const suffix = details ? ` – ${details}` : '';
  console.warn(`[docsClient] ${message}${suffix}`);
}

async function requestJson<T>(url: string, context: string): Promise<T | null> {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': USER_AGENT }});
    if (!res.ok) {
      logWarn(`${context} returned ${res.status} ${res.statusText}`);
      return null;
    }
    return (await res.json()) as T;
  } catch (error) {
    logWarn(`${context} request failed`, error);
    return null;
  }
}

export async function getAllDocs(lang: string) {
  const url = `${BASE}/api/method/ifitwala_doc.api.docs.fetch_all?language=${encodeURIComponent(lang)}`;
  return (await requestJson<{ docs: any[] }>(url, `fetch_all ${lang}`)) ?? { docs: [] };
}

export async function getOneDoc(lang: string, slug: string) {
  const url = `${BASE}/api/method/ifitwala_doc.api.docs.fetch_one?language=${encodeURIComponent(lang)}&slug=${encodeURIComponent(slug)}`;
  return requestJson<any>(url, `fetch_one ${lang}/${slug}`);
}
