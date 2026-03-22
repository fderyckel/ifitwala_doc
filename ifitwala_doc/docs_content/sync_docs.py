import os

import frappe
import frontmatter  # Requires: bench pip install python-frontmatter


def execute():
    """
    Syncs Markdown files from 'ifitwala_doc/docs_content' into the 'Documentation' DocType.
    Run via: bench execute ifitwala_doc.ifitwala_doc.sync_docs.execute
    """

    # 1. Define the folder path
    # This looks for: .../apps/ifitwala_doc/ifitwala_doc/docs_content/
    docs_path = frappe.get_app_path("ifitwala_doc", "docs_content")

    if not os.path.exists(docs_path):
        print(f"❌ Error: Folder not found at {docs_path}")
        print("   Please create the folder 'docs_content' inside your app module.")
        return

    print(f"📂 Scanning: {docs_path}")

    # 2. Iterate over all .md files
    synced_count = 0
    for filename in os.listdir(docs_path):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(docs_path, filename)

        try:
            # 3. Parse the file
            with open(file_path) as f:
                post = frontmatter.load(f)

            # 4. Extract Key Identifiers
            slug = post.metadata.get('slug')
            language = post.metadata.get('language', 'en') # Default to English

            if not slug:
                print(f"⚠️  Skipping {filename}: No 'slug' found in frontmatter.")
                continue

            # 5. Find or Create the Document
            # We look for an existing doc with the same Slug + Language
            existing_doc = frappe.db.get_value("Documentation",
                                             {"slug": slug, "language": language},
                                             "name")

            if existing_doc:
                doc = frappe.get_doc("Documentation", existing_doc)
                print(f"🔄 Updating: {slug}")
            else:
                doc = frappe.new_doc("Documentation")
                doc.slug = slug
                doc.language = language
                print(f"✨ Creating: {slug}")

            # 6. Map Metadata to DocType Fields
            doc.title = post.metadata.get('title')
            doc.category = post.metadata.get('category')      # Must match 'Doc Category' name
            doc.subcategory = post.metadata.get('subcategory') # Must match 'Doc Subcategory' name
            doc.doc_order = post.metadata.get('doc_order', 0)
            doc.summary = post.metadata.get('summary')

            # SEO Fields
            doc.seo_title = post.metadata.get('seo_title')
            doc.seo_description = post.metadata.get('seo_description')

            # Content (The body of the markdown)
            doc.body_md = post.content

            # Status (Default to Published if not specified)
            doc.status = "Published"

            # 7. Save
            doc.save(ignore_permissions=True)
            synced_count += 1

        except Exception as e:
            print(f"❌ Failed to sync {filename}: {e!s}")

    frappe.db.commit()
    print(f"✅ Sync Complete. Processed {synced_count} documents.")
