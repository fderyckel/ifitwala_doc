import type { NavItem, SiteSettings } from '@/lib/siteClient'

export const marketingHeaderNav: NavItem[] = [
  { label: 'Platform', href: '/platform/' },
  { label: 'Implementation', href: '/implementation/' },
  { label: 'Security', href: '/security/' },
  { label: 'Documentation', href: '/docs/' },
]

export const marketingFooterNav: NavItem[] = [
  { label: 'Home', href: '/' },
  { label: 'Platform', href: '/platform/' },
  { label: 'Implementation', href: '/implementation/' },
  { label: 'Security', href: '/security/' },
  { label: 'Documentation', href: '/docs/' },
  { label: 'Book a Demo', href: '/book-a-demo/' },
]

export function withMarketingDefaults(settings: SiteSettings): SiteSettings {
  return {
    ...settings,
    site_name: settings?.site_name || 'Ifitwala Ed',
    tagline:
      settings?.tagline ||
      'A modern education operations platform for institutions that need clarity, structure, and coordinated execution.',
    primary_cta_label: 'Book a Demo',
    primary_cta_url: '/book-a-demo/',
  }
}

export const heroSignals = [
  {
    eyebrow: 'Institution-wide workflows',
    title: 'Admissions to finance',
    detail: 'One operating surface across the workflows that usually live in separate systems.',
  },
  {
    eyebrow: 'Leadership visibility',
    title: 'Clearer operational control',
    detail: 'Give leadership and department heads better reporting, accountability, and institutional visibility.',
  },
  {
    eyebrow: 'Implementation-ready',
    title: 'Structured rollout',
    detail: 'Position the product as a serious platform for migration, training, and multi-team adoption.',
  },
]

export const proofStatements = [
  'Built for schools, districts, and colleges that need more than a standalone LMS or student database.',
  'Designed to help academics, administration, finance, and communication stay in sync.',
  'Created for institutions that want stronger operational confidence as they grow.',
]

export const platformPillars = [
  {
    number: '01',
    title: 'Student Records',
    description:
      'Maintain a complete student view across enrollment, attendance, academics, finance, and communication without duplicate entry.',
  },
  {
    number: '02',
    title: 'Academics and Assessment',
    description:
      'Support timetables, coursework, grading, reporting, and academic coordination from one connected platform.',
  },
  {
    number: '03',
    title: 'Admissions and Enrollment',
    description:
      'Track applicants, decisions, onboarding, and transitions with a process that remains visible and structured.',
  },
  {
    number: '04',
    title: 'Finance and Billing',
    description:
      'Bring invoicing, payment tracking, and financial workflows into the same platform used by operational teams.',
  },
  {
    number: '05',
    title: 'Operations and Administration',
    description:
      'Reduce manual handoffs between departments with cleaner workflows, ownership, and institutional consistency.',
  },
  {
    number: '06',
    title: 'Communication and Reporting',
    description:
      'Keep leadership, staff, and families aligned with structured communication and institution-wide reporting.',
  },
]

export const teamSegments = [
  {
    title: 'Heads of School and District Leaders',
    description:
      'Get clearer oversight across academics, operations, finance, and institutional performance.',
  },
  {
    title: 'Academic Leaders',
    description:
      'Coordinate schedules, assessment, reporting, and teaching workflows with less administrative friction.',
  },
  {
    title: 'Operations Teams',
    description:
      'Replace scattered tools with one system that keeps records, approvals, and daily processes in sync.',
  },
  {
    title: 'Finance Teams',
    description:
      'Improve billing accuracy, visibility, and coordination with the rest of the institution.',
  },
  {
    title: 'IT and Systems Teams',
    description:
      'Gain better control over permissions, platform structure, and system ownership without managing disconnected apps.',
  },
]

export const switchPainPoints = [
  {
    oldWay: 'Student data scattered across different tools and spreadsheets',
    newWay: 'One source of truth across admissions, academics, finance, and communication',
  },
  {
    oldWay: 'Manual coordination between departments and follow-up by email',
    newWay: 'Cleaner workflows, ownership, and visibility across institution teams',
  },
  {
    oldWay: 'Leadership reporting assembled after the fact',
    newWay: 'Stronger operational oversight built into daily workflows',
  },
  {
    oldWay: 'Families and staff receiving fragmented communication',
    newWay: 'Structured communication that reflects a more coordinated institution',
  },
]

export const trustPillars = [
  {
    title: 'Security and Permissions',
    description:
      'Institutional software has to manage access cleanly. The website should visibly speak to governance, role-based permissions, and accountability.',
  },
  {
    title: 'Implementation and Migration',
    description:
      'Rollout should feel guided, not improvised. Position Ifitwala as a partner in setup, migration, and adoption.',
  },
  {
    title: 'Operational Reliability',
    description:
      'Decision-makers need confidence that the platform behind daily school operations is dependable, structured, and supportable.',
  },
]

export const implementationSteps = [
  {
    number: '01',
    title: 'Discovery',
    description:
      'Map the institution structure, teams, workflows, and reporting needs that matter to leadership.',
  },
  {
    number: '02',
    title: 'Configuration',
    description:
      'Set up records, permissions, operational flows, and the data model required for a confident rollout.',
  },
  {
    number: '03',
    title: 'Adoption',
    description:
      'Launch with training, guided change management, and the workflows your teams need first.',
  },
]

export const showcasePanels = [
  {
    title: 'Leadership View',
    eyebrow: 'Visibility',
    items: ['Institution overview', 'Reporting surfaces', 'Cross-team signals'],
  },
  {
    title: 'Academic Operations',
    eyebrow: 'Execution',
    items: ['Scheduling and assessment', 'Records and reporting', 'Daily coordination'],
  },
  {
    title: 'Business Office',
    eyebrow: 'Control',
    items: ['Billing and finance', 'Process ownership', 'Operational follow-through'],
  },
]

export const demoHighlights = [
  'A walkthrough focused on your institution type and operating model',
  'Coverage of the workflows most relevant to leadership, academics, operations, or finance',
  'Time for implementation, migration, and support questions',
]

export const demoAudience = [
  'Heads of school, directors, or district leadership',
  'Academic leaders and registrars',
  'Operations and finance teams',
  'IT or systems administrators evaluating platform fit',
]

export const demoTopics = [
  'Student records and institution structure',
  'Academics, scheduling, and reporting',
  'Billing, communication, and operations',
  'Permissions, rollout approach, and support expectations',
]

export const platformOutcomes = [
  {
    title: 'Leadership Visibility',
    description:
      'See the institution more clearly across academic performance, operations, finance, and cross-team execution.',
  },
  {
    title: 'Operational Consistency',
    description:
      'Replace scattered processes with structured workflows that teams can follow and leadership can trust.',
  },
  {
    title: 'Cleaner Coordination',
    description:
      'Reduce handoffs, duplicate entry, and fragmented communication between departments.',
  },
  {
    title: 'Confident Growth',
    description:
      'Create a stronger operating foundation for growing schools, districts, and colleges.',
  },
]

export const workflowLanes = [
  {
    title: 'Admissions and Enrollment',
    description:
      'Track applicants, admissions decisions, onboarding, and transitions in one visible institutional process.',
    items: ['Application tracking', 'Decision workflow', 'Enrollment readiness'],
  },
  {
    title: 'Academic Coordination',
    description:
      'Connect scheduling, academic records, reporting, and classroom workflows to reduce friction for academic teams.',
    items: ['Timetables and schedules', 'Assessment and reporting', 'Academic visibility'],
  },
  {
    title: 'Business Office and Operations',
    description:
      'Bring billing, operational follow-through, and day-to-day administration into the same platform as the rest of the institution.',
    items: ['Billing and payment flow', 'Operational ownership', 'Administrative consistency'],
  },
  {
    title: 'Communication and Reporting',
    description:
      'Support a more coordinated experience for leadership, staff, families, and institution reporting needs.',
    items: ['Structured communication', 'Leadership reporting', 'Cross-team alignment'],
  },
]

export const implementationPrinciples = [
  {
    title: 'Start with institutional structure',
    description:
      'A credible rollout begins with the institution model, teams, permissions, and workflows that matter most.',
  },
  {
    title: 'Sequence adoption intentionally',
    description:
      'Launch the right workflows first so early usage builds confidence instead of confusion.',
  },
  {
    title: 'Align teams around ownership',
    description:
      'Implementation works better when leadership, academics, operations, and technical stakeholders know their roles.',
  },
  {
    title: 'Train around real work',
    description:
      'Adoption improves when training is tied to actual institutional tasks rather than abstract software tours.',
  },
]

export const implementationRoles = [
  {
    title: 'Leadership sponsor',
    description:
      'Sets priorities, success criteria, and the institutional context for the rollout.',
  },
  {
    title: 'Academic lead',
    description:
      'Represents schedules, grading, reporting, and academic coordination requirements.',
  },
  {
    title: 'Operations lead',
    description:
      'Owns the day-to-day workflows that need to stay consistent during migration and launch.',
  },
  {
    title: 'Finance or business office lead',
    description:
      'Ensures billing, collections, and finance-related processes fit the institution’s operating reality.',
  },
  {
    title: 'IT or systems lead',
    description:
      'Reviews permissions, data structure, environment ownership, and operational controls.',
  },
]

export const implementationResults = [
  'A clearer institution data model',
  'Stronger permissions and team ownership',
  'More consistent workflows across departments',
  'A rollout path leadership can explain with confidence',
]

export const securityAreas = [
  {
    title: 'Access and Permissions',
    description:
      'Institutional teams should be able to evaluate how access is structured, segmented, and governed across roles.',
  },
  {
    title: 'Data Handling and Ownership',
    description:
      'Buyers should understand where data lives, how it is managed, and what operational responsibilities sit with the platform and the institution.',
  },
  {
    title: 'Operational Continuity',
    description:
      'The trust discussion should cover backups, recovery expectations, maintenance discipline, and resilience planning.',
  },
  {
    title: 'Support and Accountability',
    description:
      'Institutions need a clear path for issue ownership, escalation, and day-to-day operational support.',
  },
]

export const securityReviewPoints = [
  'Role-based access and who can see or change sensitive information',
  'How records, operational actions, and reporting can be reviewed or audited',
  'Backup and recovery expectations appropriate to institutional operations',
  'Who owns environment, configuration, and operational changes',
  'What the support and escalation path looks like during live usage',
  'How implementation and change management reduce avoidable risk',
]

export const securityPageNotes = [
  'Trust in education software is not only about features. It is about operational discipline.',
  'A strong evaluation covers permissions, continuity, ownership, and support before rollout begins.',
  'Use the sales process to review the areas that matter most to your institution’s governance model.',
]
