import fs from 'node:fs'
import path from 'node:path'

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

export type PageSEO = {
  title?: string
  description?: string
  canonical_url?: string
  meta_description?: string
  seo_title?: string
  seo_description?: string
  seo_keywords?: string
  seo_noindex?: number
  seo_nofollow?: number
  og_image?: string
  og_title?: string
  og_description?: string
  og_image_alt?: string
  og_type?: string
}

export type PagePayload = {
  name?: string
  slug?: string
  title?: string
  layout?: string
  seo?: PageSEO
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
  social_links?: { platform?: string; url?: string; icon?: string; display_order?: number }[]
  social_same_as?: string[]
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

export type StorySummary = {
  name?: string
  slug: string
  title: string
  hero_subtitle?: string | null
  summary?: string | null
  story_type?: string | null
  topic?: string | null
  author_name?: string | null
  author_role?: string | null
  published_on?: string | null
  estimated_read_minutes?: number | null
  cover_image?: string | null
  cover_image_alt?: string | null
  featured?: number | boolean
  featured_priority?: number | null
}

export type StoryCTA = {
  label: string
  href: string
}

export type StoryTakeaway = {
  title?: string
  detail?: string
  order?: number
}

export type StoryPayload = StorySummary & {
  status?: string | null
  body_md?: string | null
  seo_title?: string | null
  seo_description?: string | null
  canonical_url?: string | null
  og_image?: string | null
  noindex?: number | boolean
  key_takeaways?: StoryTakeaway[]
  primary_cta?: StoryCTA | null
  secondary_cta?: StoryCTA | null
  related_stories?: StorySummary[]
}

export type StoryTopic = {
  topic: string
  count: number
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

const LOCAL_API_HOSTS = new Set(['127.0.0.1', 'localhost'])
const warnedFallbacks = new Set<string>()
const SITE_NAME_HEADER = resolveBenchSiteName()

function normalizeUrl(path: string) {
  const root = BASE.replace(/\/$/, '')
  const target = path.startsWith('/') ? path : `/${path}`
  return `${root}${target}`
}

function resolveBenchSiteName(): string | undefined {
  const explicitCandidates = [
    process.env.IFITWALA_DOC_SITE_NAME,
    process.env.FRAPPE_SITE,
    process.env.SITE_NAME,
  ]
  for (const candidate of explicitCandidates) {
    if (typeof candidate === 'string' && candidate.trim()) {
      return candidate.trim()
    }
  }

  let currentDir = process.cwd()
  for (let depth = 0; depth < 6; depth += 1) {
    const sitesDir = path.join(currentDir, 'sites')
    const commonConfig = path.join(sitesDir, 'common_site_config.json')
    if (fs.existsSync(commonConfig)) {
      try {
        const parsed = JSON.parse(fs.readFileSync(commonConfig, 'utf8'))
        if (typeof parsed?.default_site === 'string' && parsed.default_site.trim()) {
          return parsed.default_site.trim()
        }
      } catch {
        // Ignore malformed local config and continue searching.
      }
    }

    const currentSiteFile = path.join(sitesDir, 'currentsite.txt')
    if (fs.existsSync(currentSiteFile)) {
      try {
        const siteName = fs.readFileSync(currentSiteFile, 'utf8').trim()
        if (siteName) {
          return siteName
        }
      } catch {
        // Ignore unreadable fallback files and continue searching.
      }
    }

    const parentDir = path.dirname(currentDir)
    if (parentDir === currentDir) {
      break
    }
    currentDir = parentDir
  }

  return undefined
}

function maybeAttachSiteHeader(targetUrl: string, headers: Record<string, string>) {
  if (!SITE_NAME_HEADER) {
    return
  }

  try {
    const hostname = new URL(targetUrl).hostname.toLowerCase()
    if (LOCAL_API_HOSTS.has(hostname)) {
      headers['X-Frappe-Site-Name'] = SITE_NAME_HEADER
    }
  } catch {
    // Ignore invalid URLs and fall back to plain headers.
  }
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
  maybeAttachSiteHeader(targetUrl, headers)
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

function warnOptionalFetchFailure(scope: string, error: unknown) {
  if (warnedFallbacks.has(scope)) {
    return
  }
  warnedFallbacks.add(scope)

  const message =
    error instanceof Error
      ? error.message.split('\n')[0]
      : typeof error === 'string'
        ? error
        : 'unknown error'

  console.warn(`[site] ${scope} unavailable, using fallback (${message})`)
}

function normalizeSlug(value: unknown): string {
  if (typeof value !== 'string') {
    return '/'
  }
  const trimmed = value.trim()
  if (!trimmed || trimmed === '/') {
    return '/'
  }
  const stripped = trimmed.replace(/^\/+|\/+$/g, '')
  if (!stripped) {
    return '/'
  }
  const lowered = stripped.toLowerCase()
  if (lowered === 'index' || lowered === 'home') {
    return '/'
  }
  let normalized = stripped
  if (lowered.endsWith('/index')) {
    normalized = stripped.slice(0, -6)
  }
  normalized = normalized.replace(/^\/+|\/+$/g, '')
  if (!normalized) {
    return '/'
  }
  return `/${normalized}`
}

function normalizeStorySlug(value: unknown): string {
  if (typeof value !== 'string') {
    return ''
  }
  return value.trim().replace(/^\/+|\/+$/g, '').toLowerCase()
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
  const fallbackNav = (): NavItem[] => {
    if (location === 'Header') {
      return [
        { label: 'Services', href: '/services/', order: 10 },
        { label: 'Ifitwala Ed', href: '/ifitwala-ed/', order: 20 },
        { label: 'Data Governance', href: '/data-governance/', order: 30 },
        { label: 'Docs', href: '/docs/', order: 40 },
      ]
    }
    if (location === 'Footer') {
      return [
        { label: 'Services', href: '/services/', order: 10 },
        { label: 'Education', href: '/education/', order: 20 },
        { label: 'Ifitwala Ed', href: '/ifitwala-ed/', order: 30 },
        { label: 'Docs', href: '/docs/', order: 40 },
      ]
    }
    return []
  }

  try {
    const qp = new URLSearchParams({ location })
    const url = normalizeUrl(`/api/method/ifitwala_doc.api.site.get_nav?${qp.toString()}`)
    const raw = await fetchJSON(url)
    const items = unwrap<NavItem[]>(raw)
    return Array.isArray(items) && items.length ? items : fallbackNav()
  } catch (error) {
    warnOptionalFetchFailure(`nav:${location}`, error)
    return fallbackNav()
  }
}

export async function getSiteSettings(): Promise<SiteSettings> {
  try {
    const url = normalizeUrl(`/api/method/ifitwala_doc.api.site.get_site_settings`)
    const raw = await fetchJSON(url)
    return unwrap<SiteSettings>(raw) || {}
  } catch (error) {
    warnOptionalFetchFailure('site-settings', error)
    return {}
  }
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

export async function listStories(opts?: {
  includeDrafts?: boolean
  topic?: string
  storyType?: string
  limit?: number
}): Promise<StorySummary[]> {
  try {
    const params = new URLSearchParams()
    if (opts?.includeDrafts) {
      params.set('include_unpublished', '1')
    }
    if (opts?.topic) {
      params.set('topic', opts.topic)
    }
    if (opts?.storyType) {
      params.set('story_type', opts.storyType)
    }
    if (typeof opts?.limit === 'number' && Number.isFinite(opts.limit) && opts.limit > 0) {
      params.set('limit', String(Math.floor(opts.limit)))
    }
    const suffix = params.toString() ? `?${params.toString()}` : ''
    const raw = await fetchJSON(normalizeUrl(`/api/method/ifitwala_doc.api.site.list_stories${suffix}`))
    const items = unwrap<StorySummary[]>(raw)
    return Array.isArray(items) ? items : []
  } catch (error) {
    warnOptionalFetchFailure('stories:list', error)
    return []
  }
}

export async function getStory(
  slug: string,
  opts?: { includeDrafts?: boolean }
): Promise<StoryPayload> {
  const normalizedSlug = normalizeStorySlug(slug)
  try {
    const params = new URLSearchParams({ slug: normalizedSlug })
    if (opts?.includeDrafts) {
      params.set('include_unpublished', '1')
    }
    const raw = await fetchJSON(
      normalizeUrl(`/api/method/ifitwala_doc.api.site.get_story?${params.toString()}`)
    )
    return unwrap<StoryPayload>(raw) || { slug: normalizedSlug, title: '' }
  } catch (error) {
    warnOptionalFetchFailure(`story:${normalizedSlug || 'unknown'}`, error)
    return { slug: normalizedSlug, title: '' }
  }
}

export async function getStoryTopics(opts?: { includeDrafts?: boolean }): Promise<StoryTopic[]> {
  try {
    const params = new URLSearchParams()
    if (opts?.includeDrafts) {
      params.set('include_unpublished', '1')
    }
    const suffix = params.toString() ? `?${params.toString()}` : ''
    const raw = await fetchJSON(
      normalizeUrl(`/api/method/ifitwala_doc.api.site.get_story_topics${suffix}`)
    )
    const items = unwrap<StoryTopic[]>(raw)
    return Array.isArray(items) ? items : []
  } catch (error) {
    warnOptionalFetchFailure('stories:topics', error)
    return []
  }
}
