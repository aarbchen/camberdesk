r"""
CamberDesk — Programmatic SEO (pSEO) Static Letting Dossier & Sitemap Generator (`pseo_generator.py`).
Generates:
  • `D:\CamberDesk\lettings\index.html` (50-State DOT, USACE & Municipal Letting Hub)
  • `D:\CamberDesk\lettings\project\<slug>.html` (Individual Project Preconstruction, Bid-Tab & Prevailing-Wage Dossiers)
  • `D:\CamberDesk\sitemap.xml` & `D:\CamberDesk\robots.txt`
Styled with Symbol #07 (Compass Quadrant Lock) & Editorial Theme 1 (Warm Vellum #FAF8F5 & Obsidian Ink #0A0D14 + Blueprint Navy #1E3A8A).
"""

from error_telemetry import configure_utf8_stdio
configure_utf8_stdio()

import html
import os
from datetime import datetime, timezone
from typing import Any, Dict

from build_camberdesk_site import FAVICON_DATA_URI
from camberdesk_autopilot import build_dossiers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LETTINGS_DIR = os.path.join(BASE_DIR, "lettings")
PROJECT_DIR = os.path.join(LETTINGS_DIR, "project")
SITEMAP_PATH = os.path.join(BASE_DIR, "sitemap.xml")
ROBOTS_PATH = os.path.join(BASE_DIR, "robots.txt")
SITE_BASE_URL = os.getenv("CAMBERDESK_SITE_URL", "https://camberdesk.com").rstrip("/")

LOGO_SVG = (
    '<svg viewBox="0 0 64 64" class="w-[22px] h-[22px] shrink-0 -translate-y-[1px]" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path fill="#0A0D14" d="M32 8A24 24 0 1 0 56 32H32V8Z"/>'
    '<rect x="37" y="11" width="16" height="16" rx="2" fill="#1E3A8A"/>'
    '</svg>'
)


def generate_pseo_pages() -> Dict[str, Any]:
    os.makedirs(PROJECT_DIR, exist_ok=True)
    dossiers = build_dossiers()
    urls = [
        f"{SITE_BASE_URL}/",
        f"{SITE_BASE_URL}/apis.html",
        f"{SITE_BASE_URL}/lettings/index.html",
    ]

    cards_html = []
    for pid, d in dossiers.items():
        slug = d["slug"]
        title_esc = html.escape(d["title"])
        agency_esc = html.escape(d["agency"])
        county_esc = html.escape(d["county"])
        est_fmt = f"${float(d['engineers_estimate_usd']):,.0f}"
        rec_fmt = f"${float(d['recommended_low_bid_usd']):,.0f}"
        crew_rate = d["prevailing_wage_summary"]["fully_burdened_crew_hourly_usd"]
        planholders_esc = ", ".join(html.escape(p) for p in d.get("planholders", []))

        pay_rows = []
        for pi in d.get("pay_items", []):
            pay_rows.append(
                f"<tr class='border-b border-[#CBD5E1] hover:bg-[#F1EFEA]'>"
                f"<td class='py-2.5 px-3 font-mono font-bold text-[#1E3A8A]'>{html.escape(str(pi.get('item_code')))}</td>"
                f"<td class='py-2.5 px-3 text-[#0A0D14] font-bold'>{html.escape(str(pi.get('description')))}</td>"
                f"<td class='py-2.5 px-3 font-mono font-semibold text-[#111827]'>{pi.get('quantity'):,} {html.escape(str(pi.get('unit')))}</td>"
                f"<td class='py-2.5 px-3 font-mono font-semibold text-[#0A0D14]'>${float(pi.get('hist_low_unit_usd', 0)):,.2f}</td>"
                f"<td class='py-2.5 px-3 font-mono text-[#065F46] font-extrabold'>${float(pi.get('recommended_unit_usd', 0)):,.2f}</td>"
                f"</tr>"
            )

        page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title_esc} | CamberDesk DOT Bid-Tab &amp; Takeoff Dossier</title>
  <meta name="description" content="Preconstruction unit-price bid tabulations, Davis-Bacon prevailing wage rates, CSI divisions, and planholder intelligence for {title_esc}." />
  <link rel="icon" type="image/svg+xml" href="{FAVICON_DATA_URI}" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/png" sizes="64x64" href="/favicon.png" />
  <link rel="shortcut icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ color: #0A0D14; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
    p, li, td, th, label, span {{ letter-spacing: -0.005em; }}
  </style>
</head>
<body class="bg-[#FAF8F5] text-[#0A0D14] font-sans antialiased">
  <header class="border-b border-[#CBD5E1] bg-white">
    <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
      <a href="../../index.html" class="inline-flex items-center gap-2 text-xl font-bold text-[#0A0D14]">
        {LOGO_SVG}
        <span>CamberDesk</span>
        <span class="text-[11px] font-mono font-bold px-2 py-0.5 rounded bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8]">50-STATE DOT &amp; CIVIL</span>
      </a>
      <div class="flex items-center gap-5 text-sm font-bold">
        <a href="../index.html" class="text-[#0A0D14] hover:text-[#1E3A8A]">All Lettings</a>
        <a href="../../apis.html" class="text-[#0A0D14] hover:text-[#1E3A8A]">API Catalog</a>
        <a href="../../index.html#checkout" class="px-3.5 py-1.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold transition">Unlock 6-File .ZIP Takeoff</a>
      </div>
    </div>
  </header>
  <main class="max-w-6xl mx-auto px-6 py-10 space-y-8">
    <div class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
      <div class="flex flex-wrap items-center gap-3 text-xs font-mono">
        <span class="px-2.5 py-1 rounded bg-[#EAE6DF] text-[#0A0D14] border border-[#94A3B8] font-bold">{html.escape(pid)}</span>
        <span class="px-2.5 py-1 rounded bg-[#EFF6FF] text-[#1E3A8A] border border-[#93C5FD] font-bold">LETTING: {html.escape(str(d.get('letting_date')))}</span>
        <span class="px-2.5 py-1 rounded bg-[#ECFDF5] text-[#065F46] border border-[#6EE7B7] font-bold">DBE GOAL: {d.get('dbe_goal_pct')}%</span>
      </div>
      <h1 class="text-2xl md:text-3xl font-extrabold text-[#0A0D14]">{title_esc}</h1>
      <p class="text-[#111827] font-semibold text-sm">{agency_esc} &bull; {county_esc} &bull; Wage Decision: <code class="text-[#1E3A8A] font-bold">{html.escape(str(d.get('wage_determination_id')))}</code></p>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1]">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">ENGINEER'S ESTIMATE</div>
          <div class="text-xl font-extrabold text-[#0A0D14] mt-1">{est_fmt}</div>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1]">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">RECOMMENDED LOW BID (-5.8%)</div>
          <div class="text-xl font-extrabold text-[#065F46] mt-1">{rec_fmt}</div>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1]">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">DAVIS-BACON CREW BURDEN</div>
          <div class="text-xl font-extrabold text-[#1E3A8A] mt-1">${crew_rate}/hr</div>
        </div>
        <div class="p-4 rounded-xl bg-[#F4F1EA] border border-[#CBD5E1]">
          <div class="text-xs font-mono font-bold text-[#0A0D14]">LIQUIDATED DAMAGES</div>
          <div class="text-xl font-extrabold text-[#991B1B] mt-1">${d.get('liquidated_damages_per_day_usd'):,}/day</div>
        </div>
      </div>
    </div>

    <div class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-4">
      <h2 class="text-lg font-extrabold text-[#0A0D14] font-mono">// 36-MONTH HISTORICAL DOT ITEM BID TABULATION BENCHMARKS</h2>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm border-collapse">
          <thead>
            <tr class="bg-[#EAE6DF] border-b-2 border-[#94A3B8] text-xs font-mono font-bold text-[#0A0D14]">
              <th class="py-2.5 px-3">ITEM CODE</th>
              <th class="py-2.5 px-3">PAY ITEM DESCRIPTION</th>
              <th class="py-2.5 px-3">TAKEOFF QTY</th>
              <th class="py-2.5 px-3">36-MO LOW</th>
              <th class="py-2.5 px-3">RECOMMENDED BID</th>
            </tr>
          </thead>
          <tbody>
            {''.join(pay_rows)}
          </tbody>
        </table>
      </div>
    </div>

    <div class="p-6 rounded-2xl bg-white border border-[#CBD5E1] shadow-sm space-y-3">
      <h2 class="text-lg font-extrabold text-[#0A0D14] font-mono">// ACTIVE DOT PLANHOLDERS &amp; HEAD-TO-HEAD COMPETITORS</h2>
      <p class="text-sm font-semibold text-[#111827]">{planholders_esc}</p>
      <div class="pt-3 flex flex-wrap gap-3">
        <a href="../../index.html#checkout" class="px-4 py-2.5 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-sm transition">Compile 6-File OpenXML Bid-Tab .ZIP</a>
        <a href="{html.escape(d.get('source_url', '#'))}" target="_blank" rel="noopener" class="px-4 py-2.5 rounded-lg bg-[#EAE6DF] hover:bg-[#DDD8CE] text-[#0A0D14] border border-[#94A3B8] text-sm font-bold transition">Official DOT Letting Notice</a>
      </div>
    </div>
  </main>
</body>
</html>"""

        proj_file = os.path.join(PROJECT_DIR, f"{slug}.html")
        with open(proj_file, "w", encoding="utf-8") as fh:
            fh.write(page_html)
        urls.append(f"{SITE_BASE_URL}/lettings/project/{slug}.html")

        cards_html.append(
            f"<div class='p-5 rounded-xl bg-white border border-[#CBD5E1] shadow-sm flex flex-col justify-between gap-3'>"
            f"<div><span class='text-xs font-mono font-bold text-[#1E3A8A]'>{html.escape(pid)} &bull; {html.escape(d['state_code'])}</span>"
            f"<h3 class='text-base font-extrabold text-[#0A0D14] mt-1'><a href='project/{slug}.html' class='hover:text-[#1E3A8A]'>{title_esc}</a></h3>"
            f"<p class='text-xs font-semibold text-[#111827] mt-1.5'>{agency_esc} &bull; Est: {est_fmt}</p></div>"
            f"<div class='flex items-center justify-between pt-2.5 border-t border-[#CBD5E1] text-xs font-mono'>"
            f"<span class='text-[#065F46] font-extrabold'>Rec Bid: {rec_fmt}</span>"
            f"<a href='project/{slug}.html' class='text-[#1E3A8A] font-bold hover:underline'>Open Dossier &rarr;</a></div></div>"
        )

    hub_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>50-State DOT, USACE &amp; Public Works Letting Directory | CamberDesk</title>
  <link rel="icon" type="image/svg+xml" href="{FAVICON_DATA_URI}" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/png" sizes="64x64" href="/favicon.png" />
  <link rel="shortcut icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ color: #0A0D14; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }}
    p, li, td, th, label, span {{ letter-spacing: -0.005em; }}
  </style>
</head>
<body class="bg-[#FAF8F5] text-[#0A0D14] font-sans antialiased">
  <main class="max-w-6xl mx-auto px-6 py-10 space-y-6">
    <div class="flex items-center justify-between border-b border-[#CBD5E1] pb-4">
      <div class="flex items-center gap-3">
        {LOGO_SVG}
        <div>
          <h1 class="text-2xl font-extrabold text-[#0A0D14]">52-Portal State DOT, USACE &amp; Municipal Letting Directory</h1>
          <p class="text-sm font-medium text-[#111827] mt-0.5">Pre-shredded CSI Divisions 00–48, historical unit bid tabulations, and Davis-Bacon prevailing wage dossiers.</p>
        </div>
      </div>
      <a href="../index.html" class="px-4 py-2 rounded-lg bg-[#0A0D14] hover:bg-[#1E3A8A] text-white font-bold text-sm transition">&larr; Main CamberDesk Console</a>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {''.join(cards_html)}
    </div>
  </main>
</body>
</html>"""

    with open(os.path.join(LETTINGS_DIR, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(hub_html)

    now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sitemap_entries = "".join(
        f"  <url><loc>{u}</loc><lastmod>{now_date}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>\n"
        for u in urls
    )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + sitemap_entries
        + "</urlset>\n"
    )
    with open(SITEMAP_PATH, "w", encoding="utf-8") as fh:
        fh.write(sitemap_xml)

    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE_URL}/sitemap.xml\n"
    with open(ROBOTS_PATH, "w", encoding="utf-8") as fh:
        fh.write(robots_txt)

    print(f"[CAMBERDESK pSEO] Generated {len(dossiers)} static project dossiers, /lettings/index.html & sitemap.xml ({len(urls)} URLs).")
    return {"dossiers_count": len(dossiers), "urls_count": len(urls)}


if __name__ == "__main__":
    generate_pseo_pages()
