# Ifitwala Website and Documentation

Company website, product showcase, and documentation hub for Ifitwala.

Ifitwala helps organizations grow better systems. We support ERP implementation, workflow improvement, and data governance for organizations that depend on accurate, sensitive, and operationally critical data.

Our deepest expertise is in education: schools, education groups, LMS ecosystems, admissions, student records, reporting, safeguarding workflows, and privacy-aware data operations. Ifitwala Ed is our flagship education ERP, built from direct international-school experience.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/fderyckel/ifitwala_doc --branch develop
bench install-app ifitwala_doc
```

### Contributing

Just post issues or even better pull requests!

### License

mit

### Deploying Website and Docs

Use `deploy_docs.sh` as the single command for file-based site deploys from `frappe-bench/apps/ifitwala_doc`:

```bash
./deploy_docs.sh
```

This builds the Vue marketing bundle, builds Astro, and rsyncs `dist/` to `sites/assets/ifitwala_doc`.

Use the Frappe Desk **Rebuild Docs** button on a `Documentation` record for normal documentation edits. That path saves/publishes content through Frappe, rebuilds the static docs, and deploys assets. It does not need to refresh Nginx.

Editing an existing Astro page such as `src/pages/index.astro` only needs `./deploy_docs.sh`.

Refresh Nginx only when route/static-serving configuration changes, such as adding a new top-level Astro page route that must be served directly by Nginx or editing `install_ifitwala_nginx.sh`:

```bash
./deploy_docs.sh --with-nginx
```

For an explicit content-only deploy, use:

```bash
./deploy_docs.sh --no-nginx
```

### Documentation Authoring Blocks

The docs renderer supports custom blocks inside `Documentation.body_md`.

#### 1) Callout

Use `Callout` for highlighted notes:

```md
<Callout type="info" title="When to use this">
Short guidance that should stand apart from normal body copy.
</Callout>
```

Supported `type` values are `info`, `tip`, `warning`, and `note`.

#### 2) Steps

Use `Steps` with nested `Step` entries to render numbered cards:

```md
<Steps>
  <Step title="Create the record">Open the DocType and add required fields.</Step>
  <Step title="Assign ownership">Set assignee and due date for follow-up.</Step>
</Steps>
```

You can optionally add a section title on the wrapper:

```md
<Steps title="Onboarding flow">
  <Step title="Step one">...</Step>
  <Step title="Step two">...</Step>
</Steps>
```

#### 3) Do / Don't

Use `DoDont` with `Do` and `Dont` to render side-by-side guidance:

```md
<DoDont>
  <Do>Use canonical workflow states only.</Do>
  <Dont>Write legacy aliases in new docs.</Dont>
</DoDont>
```

Custom column headings are supported via `doTitle` and `dontTitle`:

```md
<DoDont doTitle="Recommended" dontTitle="Avoid">
  <Do>Show the user what to do next.</Do>
  <Dont>Leave actions without feedback.</Dont>
</DoDont>
```

#### 4) Related docs

Use `RelatedDocs` to render related-doc cards from published metadata:

```md
<RelatedDocs slugs="workflow-states,reporting-and-analytics" />
```

Optional custom section title:

```md
<RelatedDocs slugs="workflow-states,reporting-and-analytics" title="Continue reading" />
```

Notes:

- Slugs are comma- or whitespace-separated.
- Resolution happens at build time in Astro from published docs metadata.

#### 5) TOC behavior

The TOC widget now includes:

- active-section highlighting while scrolling
- a slim reading-progress bar in the TOC card

#### 6) Preview parity

Draft preview (`/docs/preview/<language>/<slug>`) supports the same custom tags:

- `Callout`
- `Steps`
- `DoDont`
- `RelatedDocs`
