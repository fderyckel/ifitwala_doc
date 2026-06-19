// public/js/marketing.js
async function getNav(location = "Header") {
  const res = await fetch(
    `/api/method/ifitwala_doc.api.site.get_nav?location=${encodeURIComponent(location)}`
  );
  const { message } = await res.json();
  return Array.isArray(message) ? message : [];
}

async function renderNav() {
  // Expect your header to have: <nav id="ifw-header"></nav>
  // and your footer to have:    <nav id="ifw-footer"></nav>
  const header = document.querySelector("#ifw-header");
  const footer = document.querySelector("#ifw-footer");

  if (header) {
    const items = await getNav("Header");
    header.innerHTML = items
      .map(
        (i) =>
          `<a href="${i.href}" ${i.target_blank ? 'target="_blank" rel="noopener"' : ""}>${i.label}</a>`
      )
      .join("");
  }

  if (footer) {
    const items = await getNav("Footer");
    footer.innerHTML = items
      .map(
        (i) =>
          `<a href="${i.href}" ${i.target_blank ? 'target="_blank" rel="noopener"' : ""}>${i.label}</a>`
      )
      .join(" · ");
  }
}

// run on load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", renderNav);
} else {
  renderNav();
}
