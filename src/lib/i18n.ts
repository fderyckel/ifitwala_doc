import type { NavItem, SiteSettings } from '@/lib/siteClient'

export const SUPPORTED_LOCALES = ['fr', 'en'] as const
export type Locale = (typeof SUPPORTED_LOCALES)[number]

export const DEFAULT_LOCALE: Locale = 'en'
export const FALLBACK_LOCALE: Locale = 'en'

const LOCALE_SET = new Set<string>(SUPPORTED_LOCALES)

export const localeLabels: Record<Locale, string> = {
  fr: 'FR',
  en: 'EN',
}

export function isLocale(value: unknown): value is Locale {
  return typeof value === 'string' && LOCALE_SET.has(value)
}

export function normalizeLocale(value: unknown): Locale {
  return isLocale(value) ? value : FALLBACK_LOCALE
}

export function localeFromParams(value: unknown): Locale {
  if (Array.isArray(value)) {
    return normalizeLocale(value[0])
  }
  return normalizeLocale(value)
}

export function stripLocale(pathname: string): string {
  const input = normalizePath(pathname)
  const parts = input.split('/').filter(Boolean)
  if (parts.length && LOCALE_SET.has(parts[0])) {
    const rest = parts.slice(1).join('/')
    return rest ? `/${rest}/` : '/'
  }
  return input
}

export function withLocale(pathname: string, locale: Locale): string {
  const normalized = normalizePath(stripLocale(pathname))
  if (normalized === '/') {
    return `/${locale}/`
  }
  return `/${locale}${normalized}`
}

export function localizedPath(pathname: string, locale: Locale): string {
  const normalized = normalizePath(stripLocale(pathname))
  return withLocale(normalized, locale)
}

export function alternateLinks(pathname: string, locales: Locale[] = [...SUPPORTED_LOCALES]) {
  const unlocalized = stripLocale(pathname)
  return [
    ...locales.map((locale) => ({
      locale,
      hreflang: locale,
      href: localizedPath(unlocalized, locale),
    })),
    {
      locale: DEFAULT_LOCALE,
      hreflang: 'x-default',
      href: localizedPath(unlocalized, DEFAULT_LOCALE),
    },
  ]
}

export function localizeHref(href: string | undefined, locale: Locale): string {
  if (!href) {
    return href || ''
  }
  if (/^(https?:|mailto:|tel:|#)/i.test(href)) {
    return href
  }
  if (href.startsWith('/assets/') || href.startsWith('/files/')) {
    return href
  }
  if (href === '/docs/' || href === '/docs') {
    return `/docs/${locale}/`
  }
  if (href.startsWith('/docs/')) {
    return href
  }
  if (!href.startsWith('/')) {
    return href
  }
  return localizedPath(href, locale)
}

export function localizeNav(items: NavItem[], locale: Locale): NavItem[] {
  return items.map((item) => ({
    ...item,
    href: localizeHref(item.href, locale),
  }))
}

export function localizeSettings(settings: SiteSettings, locale: Locale): SiteSettings {
  return {
    ...settings,
    primary_cta_url: localizeHref(settings.primary_cta_url || '/book-a-call/', locale),
  }
}

export function normalizePath(pathname: string): string {
  const raw = typeof pathname === 'string' ? pathname.trim() : '/'
  if (!raw || raw === '/') {
    return '/'
  }
  const [pathOnly] = raw.split(/[?#]/)
  const stripped = pathOnly.replace(/^\/+|\/+$/g, '')
  return stripped ? `/${stripped}/` : '/'
}
