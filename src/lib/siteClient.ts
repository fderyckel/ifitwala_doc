type Section = {
  type: string
  props: Record<string, any>
  order?: number
  block?: {
    doctype?: string
    name?: string
    label?: string
  }
}

export type PageSummary = {
  name: string
  slug: string
  title: string
  layout?: string
  is_published?: number
  modified?: string | null
  created?: string | null
}

export type PagePayload = {
  name?: string
  slug?: string
  title?: string
  layout?: string
  seo?: Record<string, any>
  sections?: Section[]
  is_published?: number
  modified?: string | null
  created?: string | null
}

export type NavItem = {
  label: string
  href: string
  target_blank?: number
  order?: number
}

export type SiteSettings = {
  site_name?: string
  brand_logo?: string
  brand_logo_alt?: string
  tagline?: string
  primary_cta_label?: string
  primary_cta_url?: string
  footer_md?: string
  updated_at?: string | null
}

const BASE =
  (typeof import.meta !== 'undefined' &&
    (import.meta as any).env &&
    ((import.meta as any).env.PUBLIC_SITE_API ||
      (import.meta as any).env.PUBLIC_DOCS_API)) ||
  process.env.SITE_API_BASE ||
  process.env.DOCS_API_BASE ||
  'http://127.0.0.1:8000'

function normalizeUrl(path: string) {
  const root = BASE.replace(/\/$/, '')
  const target = path.startsWith('/') ? path : `/${path}`
  return `${root}${target}`
}

function withCacheBust(url: string, token?: string) {
  const sep = url.includes('?') ? '&' : '?'
  const value = token || Date.now().toString(36)
  return `${url}${sep}__bust=${value}`
}

async function fetchJSON(url: string, attempt = 1): Promise<any> {
  const headers: Record<string, string> = {
    'User-Agent': 'ifitwala-site/astro-build',
    Accept: 'application/json',
  }
  const targetUrl = attempt === 1 ? url : withCacheBust(url, `${Date.now()}_${attempt}`)
  if (attempt > 1) {
    headers['Cache-Control'] = 'no-cache, no-store'
    headers.Pragma = 'no-cache'
  }

  let res: Response
  try {
    res = await fetch(targetUrl, { headers })
  } catch (error) {
    if (attempt < 3) {
      return fetchJSON(url, attempt + 1)
    }
    throw error
  }

  const text = await res.text()
  if (!res.ok) {
    throw new Error(`${targetUrl} -> ${res.status} ${res.statusText}\n${text}`)
  }

  try {
    return JSON.parse(text)
  } catch (error) {
    throw new Error(`Invalid JSON from ${targetUrl}`)
  }
}

function unwrap<T = any>(data: any): T {
  if (data && typeof data === 'object' && 'message' in data) {
    return (data as any).message as T
  }
  return data as T
}

function normalizeSlug(value: unknown): string {
  if (typeof value !== 'string') {
    return '/'
  }
  const trimmed = value.trim()
  if (!trimmed || trimmed === '/') {
    return '/'
  }
  return `/${trimmed.replace(/^\/|\/$/g, '')}`
}

export function slugToSegments(slug: string): string[] {
  return normalizeSlug(slug)
    .split('/')
    .filter(Boolean)
}

export async function listPages(opts?: { includeDrafts?: boolean }): Promise<PageSummary[]> {
  const qp = new URLSearchParams()
  if (opts?.includeDrafts) {
    qp.set('include_unpublished', '1')
  }
  const suffix = qp.size ? `?${qp.toString()}` : ''
  const raw = await fetchJSON(normalizeUrl(`/api/method/ifitwala_doc.api.site.list_pages${suffix}`))
  const items = unwrap<PageSummary[]>(raw)
  return Array.isArray(items) ? items : []
}

export async function getPage(slug = '/', opts?: { includeDrafts?: boolean }): Promise<PagePayload> {
  const qp = new URLSearchParams({ slug: normalizeSlug(slug) })
  if (opts?.includeDrafts) {
    qp.set('include_unpublished', '1')
  }
  const url = normalizeUrl(`/api/method/ifitwala_doc.api.site.get_page?${qp.toString()}`)
  const raw = await fetchJSON(url)
  return unwrap<PagePayload>(raw) || {}
}

export async function getNav(location = 'Header'): Promise<NavItem[]> {
  const qp = new URLSearchParams({ location })
  const url = normalizeUrl(`/api/method/ifitwala_doc.api.site.get_nav?${qp.toString()}`)
  const raw = await fetchJSON(url)
  const items = unwrap<NavItem[]>(raw)
  return Array.isArray(items) ? items : []
}

export async function getSiteSettings(): Promise<SiteSettings> {
  const url = normalizeUrl(`/api/method/ifitwala_doc.api.site.get_site_settings`)
  const raw = await fetchJSON(url)
  return unwrap<SiteSettings>(raw) || {}
}
