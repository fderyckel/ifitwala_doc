---
title: "Documentation Authoring: Blocks and Preview Parity"
slug: docs-authoring
doc_order: 999
summary: "Use Steps, DoDont, and RelatedDocs blocks in Documentation markdown, with matching behavior in Astro and draft preview."
---

# Documentation Authoring: Blocks and Preview Parity

This page documents the supported custom blocks for `Documentation.body_md` and how they render in both Astro docs pages and Frappe draft preview.

## Supported Custom Blocks

- `Steps`: numbered step cards
- `DoDont`: side-by-side Do and Don't guidance
- `RelatedDocs`: related-document cards resolved from published metadata

## Steps Block

Use `Steps` with one or more nested `Step` entries. Each step can include a `title` attribute.

<Steps title="Example: Intake flow">
  <Step title="Capture">Create the inquiry from web form or Desk.</Step>
  <Step title="Assign">Set ownership so follow-up has a clear owner.</Step>
  <Step title="Close loop">Mark contacted or archive when done.</Step>
</Steps>

## Do / Don't Block

Use `DoDont` with nested `Do` and `Dont` entries.

Optional wrapper attributes:

- `doTitle`
- `dontTitle`

<DoDont doTitle="Do" dontTitle="Don't">
  <Do>Use explicit actions with user feedback.</Do>
  <Do>Keep workflow state transitions server-validated.</Do>
  <Dont>Allow silent failures on button click.</Dont>
  <Dont>Depend on UI behavior for correctness invariants.</Dont>
</DoDont>

## Related Docs Block

Use `RelatedDocs` with a `slugs` list (comma- or whitespace-separated).  
An optional `title` attribute customizes the section heading.

<RelatedDocs slugs="program,student-log" title="Related examples" />

## TOC Active State and Reading Progress

The docs TOC now tracks the active section while scrolling and shows a slim reading-progress bar for the current page.

## Draft Preview Parity

Preview rendering (`/docs/preview/<language>/<slug>`) supports the same custom tags as Astro docs pages:

- `Steps`
- `DoDont`
- `RelatedDocs`
