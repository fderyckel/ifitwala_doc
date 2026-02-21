### Ifitwala Doc

Site and Docs for IFitwala Ed

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

### Convert the docs and Web Page to Astro
You need to run each time the ./deploy_docs.sh script from the your frappe-bench/apps/ifitwala_docs folder

### Documentation Authoring Blocks

The docs renderer supports custom blocks inside `Documentation.body_md`.

#### 1) Steps

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

#### 2) Do / Don't

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

#### 3) Related docs

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

#### 4) TOC behavior

The TOC widget now includes:

- active-section highlighting while scrolling
- a slim reading-progress bar in the TOC card

#### 5) Preview parity

Draft preview (`/docs/preview/<language>/<slug>`) supports the same custom tags:

- `Steps`
- `DoDont`
- `RelatedDocs`
