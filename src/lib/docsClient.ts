const BASE = process.env.DOCS_API_BASE || 'http://127.0.0.1:8000';

async function fetchJSON(url: string) {
  const res = await fetch(url, { headers: { 'User-Agent': 'astro-build' } });
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
  // Frappe returns { message: ... }
  return (data && typeof data === 'object' && 'message' in data) ? data.message : data;
}

export async function getAllDocs(lang?: string) {
  const qp = lang ? `?language=${encodeURIComponent(lang)}` : '';
  const raw = await fetchJSON(`${BASE}/api/method/ifitwala_doc.api.docs.fetch_all${qp}`);
  return unwrap<{ docs: any[] }>(raw);
}

export async function getOneDoc(lang: string, slug: string) {
  const raw = await fetchJSON(
    `${BASE}/api/method/ifitwala_doc.api.docs.fetch_one?language=${encodeURIComponent(lang)}&slug=${encodeURIComponent(slug)}`
  );
  return unwrap<any>(raw);
}
