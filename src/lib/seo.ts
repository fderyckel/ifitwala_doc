export type JsonLd = Record<string, any>

export const SITE_ORIGIN = 'https://ifitwala.com'
export const SITE_URL = `${SITE_ORIGIN}/`

export const SEO_KEYWORDS = [
  'school ERP implementation',
  'education ERP implementation',
  'admissions systems',
  'ERP discovery sprint',
  'data exposure audit',
  'ERP implementation for SMEs',
  'SME ERP consulting',
  'Frappe implementation',
  'ERPNext implementation',
  'Odoo implementation',
  'open source ERP',
  'workflow mapping',
  'data migration',
  'ERP data governance',
  'education ERP',
  'school operations platform',
]

export function absoluteSiteUrl(pathname = '/'): string {
  if (/^https?:\/\//i.test(pathname)) {
    return pathname
  }
  return new URL(pathname.replace(/^\//, ''), SITE_URL).toString()
}

export function organizationSchema(siteName = 'Ifitwala', logo?: string, sameAs: string[] = []): JsonLd {
  return {
    '@type': 'Organization',
    '@id': `${SITE_URL}#organization`,
    name: siteName,
    url: SITE_URL,
    logo: logo ? absoluteSiteUrl(logo) : undefined,
    description:
      'Ifitwala helps schools and organizations handling sensitive operational data implement ERP systems, improve workflows, and govern reporting, permissions, and data access across Frappe, ERPNext, Odoo, and related platforms.',
    sameAs: sameAs.length ? sameAs : undefined,
    knowsAbout: SEO_KEYWORDS,
  }
}

export function websiteSchema(siteName = 'Ifitwala'): JsonLd {
  return {
    '@type': 'WebSite',
    '@id': `${SITE_URL}#website`,
    name: siteName,
    url: SITE_URL,
    publisher: { '@id': `${SITE_URL}#organization` },
    inLanguage: 'en',
  }
}

export function webPageSchema({
  url,
  name,
  description,
  inLanguage = 'en',
}: {
  url: string
  name: string
  description?: string
  inLanguage?: string
}): JsonLd {
  return {
    '@type': 'WebPage',
    '@id': `${url}#webpage`,
    url,
    name,
    description: description || undefined,
    inLanguage,
    isPartOf: { '@id': `${SITE_URL}#website` },
    about: { '@id': `${SITE_URL}#organization` },
  }
}

export function breadcrumbSchema(url: string): JsonLd | undefined {
  const parsed = new URL(url)
  const rawParts = parsed.pathname.split('/').filter(Boolean)
  const locale = rawParts[0] === 'en' || rawParts[0] === 'fr' ? rawParts[0] : ''
  const parts = locale ? rawParts.slice(1) : rawParts
  if (!parts.length) {
    return undefined
  }

  const itemListElement = [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'Home',
      item: SITE_URL,
    },
    ...parts.map((part, index) => {
      const path = `${locale ? `/${locale}` : ''}/${parts.slice(0, index + 1).join('/')}/`
      return {
        '@type': 'ListItem',
        position: index + 2,
        name: titleize(part),
        item: absoluteSiteUrl(path),
      }
    }),
  ]

  return {
    '@type': 'BreadcrumbList',
    '@id': `${url}#breadcrumb`,
    itemListElement,
  }
}

export function serviceSchema({
  name,
  description,
  url,
  serviceType,
  audience = 'SMEs, schools, and operational teams evaluating ERP implementation',
  areaServed = ['Belgium', 'Europe', 'International'],
  keywords = SEO_KEYWORDS,
}: {
  name: string
  description: string
  url: string
  serviceType: string
  audience?: string
  areaServed?: string[]
  keywords?: string[]
}): JsonLd {
  const serviceUrl = absoluteSiteUrl(url)
  return {
    '@type': 'Service',
    '@id': `${serviceUrl}#service`,
    name,
    description,
    url: serviceUrl,
    serviceType,
    provider: { '@id': `${SITE_URL}#organization` },
    audience: {
      '@type': 'Audience',
      audienceType: audience,
    },
    areaServed: areaServed.map((name) => ({ '@type': 'Place', name })),
    category: keywords,
  }
}

export function softwareApplicationSchema({
  name,
  description,
  url,
  applicationCategory = 'BusinessApplication',
  keywords = ['education ERP', 'school operations platform', 'student information system'],
}: {
  name: string
  description: string
  url: string
  applicationCategory?: string
  keywords?: string[]
}): JsonLd {
  const productUrl = absoluteSiteUrl(url)
  return {
    '@type': 'SoftwareApplication',
    '@id': `${productUrl}#software`,
    name,
    description,
    url: productUrl,
    applicationCategory,
    operatingSystem: 'Web',
    creator: { '@id': `${SITE_URL}#organization` },
    publisher: { '@id': `${SITE_URL}#organization` },
    keywords,
  }
}

export function faqSchema(items: { question: string; answer: string }[], id: string): JsonLd {
  return {
    '@type': 'FAQPage',
    '@id': `${absoluteSiteUrl(id)}#faq`,
    mainEntity: items.map((item) => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer,
      },
    })),
  }
}

function titleize(value: string): string {
  return value
    .split('-')
    .filter(Boolean)
    .map((part) => `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
    .join(' ')
}
