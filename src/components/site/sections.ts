import type { AstroComponentFactory } from 'astro'

import HeroSection from './HeroSection.astro'
import FeatureHighlightsSection from './FeatureHighlightsSection.astro'
import TrustLogosSection from './TrustLogosSection.astro'
import LongformContentSection from './LongformContentSection.astro'

export const SECTION_COMPONENTS: Record<string, AstroComponentFactory> = {
  Hero: HeroSection,
  'Feature Highlights': FeatureHighlightsSection,
  'Feature Highlights Section': FeatureHighlightsSection,
  'Trust Logos': TrustLogosSection,
  'Longform Content': LongformContentSection,
  'Longform Block': LongformContentSection,
}

export function resolveSectionComponent(type?: string): AstroComponentFactory | null {
  if (!type) {
    return null
  }
  return SECTION_COMPONENTS[type] ?? null
}
