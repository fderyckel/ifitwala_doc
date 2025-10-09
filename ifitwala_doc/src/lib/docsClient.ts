const BASE = process.env.DOCS_API_BASE || 'http://127.0.0.1:8000';

export async function getAllDocs(lang: string) {
  const url = `${BASE}/api/method/ifitwala_doc.api.docs.fetch_all?language=${encodeURIComponent(lang)}`
  const res = await fetch(url, { headers: { 'User-Agent': 'astro-build' }})
  if (!res.ok) throw new Error(`fetch_all failed: ${res.status}`)
  return res.json() as Promise<{ docs: any[] }>
}

export async function getOneDoc(lang: string, slug: string) {
  const url = `${BASE}/api/method/ifitwala_doc.api.docs.fetch_one?language=${encodeURIComponent(lang)}&slug=${encodeURIComponent(slug)}`
  const res = await fetch(url, { headers: { 'User-Agent': 'astro-build' }})
  if (!res.ok) throw new Error(`fetch_one failed: ${lang}/${slug}`)
  return res.json()
}
