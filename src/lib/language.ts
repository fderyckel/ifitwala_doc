const DIACRITIC_RX = /[\u0300-\u036f]/g;
const NON_ALNUM_RX = /[^a-zA-Z0-9]+/g;
const EDGE_DASH_RX = /^-+|-+$/g;

type LanguageInfo = {
  raw: string;
  slug: string;
};

export function describeLanguage(value: unknown): LanguageInfo {
  if (typeof value !== 'string') {
    return { raw: '', slug: '' };
  }

  const raw = value.trim();
  if (!raw) {
    return { raw: '', slug: '' };
  }

  const normalized =
    typeof raw.normalize === 'function' ? raw.normalize('NFKD') : raw;
  const ascii = normalized.replace(DIACRITIC_RX, '');
  const basicSlug = ascii
    .replace(NON_ALNUM_RX, '-')
    .replace(EDGE_DASH_RX, '')
    .toLowerCase();

  if (basicSlug) {
    return { raw, slug: basicSlug };
  }

  const fallback = Array.from(raw)
    .map((char) => {
      const code = char.codePointAt(0);
      return code ? code.toString(16) : '';
    })
    .filter(Boolean)
    .join('');

  return { raw, slug: fallback ? `lang-${fallback}` : 'lang' };
}

export function languageSlug(value: unknown): string {
  return describeLanguage(value).slug;
}

export function languageRaw(value: unknown): string {
  return describeLanguage(value).raw;
}
