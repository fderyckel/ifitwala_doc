export function storyHref(slug?: string | null) {
  const clean = typeof slug === 'string' ? slug.trim().replace(/^\/+|\/+$/g, '') : ''
  return clean ? `/insights/${clean}/` : '/insights/'
}

export function formatStoryDate(value?: string | null) {
  if (!value || typeof value !== 'string') {
    return 'Coming soon'
  }

  const trimmed = value.trim()
  const match = trimmed.match(/^(\d{4})-(\d{2})-(\d{2})$/)
  if (match) {
    const [, year, month, day] = match
    const date = new Date(Number(year), Number(month) - 1, Number(day))
    return new Intl.DateTimeFormat('en', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
    }).format(date)
  }

  const parsed = new Date(trimmed)
  if (Number.isNaN(parsed.getTime())) {
    return trimmed
  }

  return new Intl.DateTimeFormat('en', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  }).format(parsed)
}

export function readTimeLabel(minutes?: number | null) {
  if (typeof minutes !== 'number' || !Number.isFinite(minutes) || minutes <= 0) {
    return null
  }
  return `${Math.max(1, Math.round(minutes))} min read`
}

export function isFeatured(value: unknown) {
  if (typeof value === 'boolean') return value
  if (typeof value === 'number') return value !== 0
  if (typeof value === 'string') {
    const normalized = value.trim().toLowerCase()
    return normalized === '1' || normalized === 'true' || normalized === 'yes'
  }
  return false
}
