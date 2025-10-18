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

export type ThemeTokens = {
  ink_color: string
  slate_color: string
  canopy_color: string
  leaf_color: string
  moss_color: string
  sky_color: string
  sand_color: string
  border_color: string
  radius_lg: string
  radius_xl: string
  shadow_soft: string
  shadow_strong: string
  focus_ring: string
}

const DEFAULT_THEME: ThemeTokens = {
  ink_color: '#0F172A',
  slate_color: '#475569',
  canopy_color: '#12563A',
  leaf_color: '#2F855A',
  moss_color: '#A6D6B1',
  sky_color: '#E6F3F9',
  sand_color: '#F4EFE7',
  border_color: '#E2E8F0',
  radius_lg: '1rem',
  radius_xl: '1.25rem',
  shadow_soft: '0 6px 20px rgba(15, 23, 42, 0.06)',
  shadow_strong: '0 12px 32px rgba(15, 23, 42, 0.1)',
  focus_ring: '0 0 0 3px rgba(47, 133, 90, 0.35)',
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

export async function getThemeTokens(): Promise<ThemeTokens> {
  try {
    const url = normalizeUrl(`/api/method/ifitwala_doc.api.site.get_theme`)
    const raw = await fetchJSON(url)
    const theme = unwrap<ThemeTokens>(raw)
    return { ...DEFAULT_THEME, ...(theme || {}) }
  } catch (error) {
    return { ...DEFAULT_THEME }
  }
}
