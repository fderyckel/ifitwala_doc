---
title: "Documentation Authoring: Blocks and Preview Parity"
slug: docs-authoring
doc_order: 999
summary: "Use Steps, DoDont, and RelatedDocs blocks in Documentation markdown, with matching behavior in Astro and draft preview."
---

# Documentation Authoring: Blocks and Preview Parity

This page documents the supported custom blocks for `Documentation.body_md` and how they render in both Astro docs pages and Frappe draft preview.

## Supported Custom Blocks

- `Callout`: highlighted notes, tips, warnings, and information blocks
- `Steps`: numbered step cards
- `DoDont`: side-by-side Do and Don't guidance
- `RelatedDocs`: related-document cards resolved from published metadata

## Callout Block

Use `Callout` for short guidance that should stand apart from normal body copy.

Supported `type` values:

- `info`
- `tip`
- `warning`
- `note`

An optional `title` attribute adds a heading inside the callout.

<Callout type="info" title="Authoring note">
Custom authoring blocks must be saved in `Documentation.body_md`. The field is configured to preserve these tags so the Astro renderer can transform them during rebuild.
</Callout>

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

- `Callout`
- `Steps`
- `DoDont`
- `RelatedDocs`

## Publishing and Rebuild Flow

For normal documentation edits in the `Documentation` DocType:

1. Edit `Body MD`.
2. Save the document.
3. Keep the document `Published` if it should appear on the static site.
4. Use **Rebuild Docs**.

This rebuild path deploys the generated static assets. It does not need to refresh Nginx.

Use `./deploy_docs.sh` from the app root after changing file-based Astro, Vue, CSS, or other site source files. Editing an existing Astro page, including `src/pages/index.astro`, only needs this deploy command.

Built pages are served through Frappe's normal routing via `ifitwala_doc/www/index.py`, which reads the generated HTML from `sites/assets/ifitwala_doc`. Custom Nginx static routes are optional.

Use `./deploy_docs.sh --with-nginx` only when intentionally enabling or changing the optional Nginx static route snippet.
