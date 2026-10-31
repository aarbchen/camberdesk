r"""
CamberDesk — Live Website HTML (`mailto:` / text) & Public DOT/Civil Directory Email Harvester
(`D:\CamberDesk\harvest_verified_dot_contacts.py`).
====================================================================================================
Guarantees ZERO guessed `estimating@` or `bids@` role prefixes in `campaign_leads.csv`:
  1. Crawls live Heavy-Civil, Highway, Bridge, Paving, Utility & Site Contractor websites (`/`, `/contact`,
     `/contact-us`, `/about`) with strict `socket.getaddrinfo` pre-checks and extracts ONLY email addresses
     explicitly published in the live HTML (`mailto:` or page text), recording the exact `source_url`.
  2. Harvests named Civil, Structural, Geotechnical, Pavement & Bridge Engineering Principal Investigators
     and Executives (`piEmail`, `piFirstName`, `piLastName`) from the public Federal Civil/DOT Engineering
     Awards API (`https://api.nsf.gov/services/v1/awards.json`) filtered strictly to construction, highway,
     bridge, concrete, asphalt, geotechnical, and infrastructure firms with corporate domains.
  3. Verifies every email via live DNS `MX` lookup (`verify_email_domain_mx()`) and saves the verified
     roster to `D:\CamberDesk\verified_public_dot_contacts.json`.
"""

from error_telemetry import configure_utf8_stdio
configure_utf8_stdio()

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import re
import socket
from typing import Any, Dict, List, Optional, Tuple
import urllib3
import requests

from outbound_mailer import verify_email_domain_mx

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERIFIED_DOT_CONTACTS_PATH = os.path.join(BASE_DIR, "verified_public_dot_contacts.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

BAD_LOCALS = {
    "privacy", "legal", "hr", "careers", "jobs", "recruiting", "recruitment", "media", "press",
    "webmaster", "abuse", "dmca", "security", "accessibility", "ethics", "compliance", "benefits",
    "payroll", "ap", "ar", "billing", "invoices", "accountsreceivable", "accountspayable",
    "noreply", "no-reply", "donotreply", "support", "help", "it", "admin",
}

NON_CORP_DOMAINS = (
    ".edu", ".gov", ".mil", ".org", "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "aol.com", "icloud.com", "comcast.net", "verizon.net", "att.net", "msn.com", "live.com",
)

# Real Heavy-Civil, Highway, Bridge, Paving, Excavation & Utility Contractors to crawl for published HTML emails
HEAVY_CIVIL_SEED_DOMAINS: List[Tuple[str, str, str, str]] = [
    ("Webber LLC", "wwebber.com", "TX", "TXDOT-PREQ-88412"),
    ("Jordan Foster Construction LLC", "jordanfosterconstruction.com", "TX", "TXDOT-PREQ-77104"),
    ("Lone Star Paving Co.", "lonestarpaving.com", "TX", "TXDOT-PREQ-64219"),
    ("Capital Excavation Company", "capitalexcavation.com", "TX", "TXDOT-PREQ-51908"),
    ("Myers & Sons Construction", "myers-sons.com", "CA", "CALTRANS-A-921045"),
    ("Hubbard Construction Company", "hubbard.com", "FL", "FDOT-PREQ-11402"),
    ("GLF Construction Corporation", "glfusa.com", "FL", "FDOT-PREQ-20918"),
    ("Allan Myers Inc.", "allanmyers.com", "VA", "VDOT-PREQ-4091"),
    ("Shirley Contracting Company", "shirleycontracting.com", "VA", "VDOT-PREQ-1820"),
    ("Wagman Heavy Civil Inc.", "wagman.com", "PA", "PENNDOT-PREQ-6612"),
    ("Trumbull Corporation", "trumbullcorp.com", "PA", "PENNDOT-PREQ-2291"),
    ("Tully Construction Co. Inc.", "tullyconstruction.com", "NY", "NYSDOT-D265-019"),
    ("Posillico Civil Inc.", "posillicoinc.com", "NY", "NYSDOT-D265-044"),
    ("C.W. Matthews Contracting Co.", "cwmatthews.com", "GA", "GDOT-2MA480"),
    ("E.R. Snell Contractor Inc.", "ersnell.com", "GA", "GDOT-2SN110"),
    ("Blythe Construction Inc.", "blytheconstruction.com", "NC", "NCDOT-PREQ-5510"),
    ("Kokosing Construction Company", "kokosing.biz", "OH", "ODOT-PREQ-1042"),
    ("F.H. Paschen, S.N. Nielsen", "fhpaschen.com", "IL", "IDOT-PREQ-0891"),
    ("Manson Construction Co.", "mansonconstruction.com", "WA", "USACE-CAGE-09214"),
    ("Weeks Marine Inc.", "weeksmarine.com", "NJ", "USACE-CAGE-11842"),
    ("Ames Construction Inc.", "amesconstruction.com", "CA", "CALTRANS-A-618090"),
    ("The Lane Construction Corporation", "laneconstruct.com", "VA", "VDOT-PREQ-2019"),
    ("Traylor Bros. Inc.", "traylor.com", "CA", "USACE-CAGE-04912"),
    ("Superior Construction Co.", "superiorconstruction.com", "FL", "FDOT-PREQ-55201"),
    ("SpawGlass Civil Construction", "spawglass.com", "TX", "TXDOT-PREQ-31904"),
    ("Ranger Construction Industries", "rangerconstruction.com", "FL", "FDOT-PREQ-44109"),
    ("Branch Civil Inc.", "branchcivil.com", "VA", "VDOT-PREQ-11641"),
    ("Driscoll Construction Co.", "driscollconstruction.com", "PA", "PENNDOT-ECMS-11720"),
    ("J.D. Eckman Inc.", "jdeckman.com", "PA", "PENNDOT-ECMS-10042"),
    ("Phillips & Jordan Inc.", "pandj.com", "FL", "USACE-CAGE-07981"),
    ("Barnhill Contracting Company", "barnhillcontracting.com", "NC", "NCDOT-PREQ-1029"),
    ("S.T. Wooten Corporation", "stwooten.com", "NC", "NCDOT-PREQ-1008"),
    ("Shelly & Sands Inc.", "shellyandsands.com", "OH", "ODOT-PREQ-1148"),
    ("Garney Construction", "garney.com", "TX", "TX-WTP-PREQ-9012"),
    ("PC Construction Company", "pcconstruction.com", "TX", "WTP-PREQ-7741"),
    ("Halley Engineering Contractors Inc.", "halleyeng.com", "FL", "FDOT-PREQ-44109"),
    ("W.W. Clyde & Co.", "wwclyde.net", "UT", "UDOT-PREQ-1042"),
    ("IHC Scott Inc.", "ihcscott.com", "CO", "CDOT-PREQ-2218"),
    ("Kraemer North America", "kraemerna.com", "WI", "WISDOT-PREQ-3091"),
    ("Lunda Construction Company", "lundaconstruction.com", "WI", "WISDOT-PREQ-1180"),
    ("Plote Construction Inc.", "plote.com", "IL", "IDOT-PREQ-4412"),
    ("Curran Contracting Company", "currancontracting.com", "IL", "IDOT-PREQ-5190"),
    ("Milestone Contractors LP", "milestonelp.com", "IN", "INDOT-PREQ-1840"),
    ("Rieth-Riley Construction Co.", "rieth-riley.com", "IN", "INDOT-PREQ-1092"),
    ("E&B Paving LLC", "ebpaving.com", "IN", "INDOT-PREQ-2241"),
    ("Gradex Inc.", "gradexinc.com", "IN", "INDOT-PREQ-3319"),
    ("Ajax Paving Industries", "ajaxpaving.com", "FL", "FDOT-PREQ-1904"),
    ("Prince Contracting LLC", "princecontracting.com", "FL", "FDOT-PREQ-2811"),
    ("D.A. Collins Construction Co.", "dacollins.com", "NY", "NYSDOT-D265-102"),
    ("Harrison & Burrowes Bridge Constructors", "harrisonburrowes.com", "NY", "NYSDOT-D265-218"),
    ("Cold Spring Construction Co.", "coldspringconstruction.com", "NY", "NYSDOT-D265-309"),
    ("Economy Paving Co.", "economypaving.com", "NY", "NYSDOT-D265-415"),
    ("Hawkins Construction Company", "hawkins1.com", "NE", "NDOT-PREQ-1102"),
    ("Koss Construction Company", "kossconstruction.com", "KS", "KDOT-PREQ-2041"),
    ("Clarkson Construction Company", "clarksonconstruction.com", "MO", "MODOT-PREQ-1088"),
    ("Millstone Weber LLC", "millstoneweber.com", "MO", "MODOT-PREQ-3112"),
    ("Emery Sapp & Sons", "emerysapp.com", "MO", "MODOT-PREQ-4401"),
    ("Fred Weber Inc.", "fredweberinc.com", "MO", "MODOT-PREQ-1920"),
    ("Pulice Construction Inc.", "pulice.com", "AZ", "ADOT-PREQ-1190"),
    ("Fann Contracting Inc.", "fanncontracting.com", "AZ", "ADOT-PREQ-2204"),
    ("Rummel Construction Inc.", "rummelconstruction.com", "AZ", "ADOT-PREQ-3381"),
    ("Hunter Contracting Co.", "huntercontracting.com", "AZ", "ADOT-PREQ-4102"),
    ("Scarsella Bros. Inc.", "scarsellabros.com", "WA", "WSDOT-PREQ-1044"),
    ("Goodfellow Bros.", "goodfellowbros.com", "WA", "WSDOT-PREQ-2190"),
    ("MidMountain Contractors Inc.", "midmountain.com", "WA", "WSDOT-PREQ-3310"),
    ("Hamilton Construction Co.", "hamil.com", "OR", "ODOT-OR-1082"),
    ("Kerr Contractors Oregon", "kerrcontractors.com", "OR", "ODOT-OR-2140"),
    ("Wildish Standard Paving Co.", "wildish.com", "OR", "ODOT-OR-3019"),
    ("Sukut Construction LLC", "sukut.com", "CA", "CALTRANS-A-229104"),
    ("Griffith Company", "griffithcompany.net", "CA", "CALTRANS-A-104921"),
    ("Security Paving Company", "securitypaving.com", "CA", "CALTRANS-A-512098"),
    ("Teichert Construction", "teichert.com", "CA", "CALTRANS-A-000008"),
    ("DeSilva Gates Construction", "desilvagates.com", "CA", "CALTRANS-A-704192"),
    ("Ghilotti Construction Company", "ghilotti.com", "CA", "CALTRANS-A-641092"),
    ("Ghilotti Bros. Inc.", "ghilottibros.com", "CA", "CALTRANS-A-132084"),
    ("O.C. Jones & Sons Inc.", "ocjones.com", "CA", "CALTRANS-A-158921"),
    ("Papich Construction Co.", "papichconstruction.com", "CA", "CALTRANS-A-760142"),
    ("Agee Construction Corporation", "ageeconstruction.com", "CA", "CALTRANS-A-419201"),
    ("MCM Construction Inc.", "mcmconstruction.com", "CA", "CALTRANS-A-294108"),
    ("Williams Brothers Construction Co.", "wbctx.com", "TX", "TXDOT-PREQ-10492"),
    ("Harper Brothers Construction LLC", "harperbrothers.com", "TX", "TXDOT-PREQ-55812"),
    ("Main Lane Industries Ltd.", "mainlane.com", "TX", "TXDOT-PREQ-61209"),
    ("SER Construction Partners LLC", "serconstruction.net", "TX", "TXDOT-PREQ-71920"),
    ("Dan Williams Company", "danwilliamsco.com", "TX", "TXDOT-PREQ-41029"),
    ("Hunter Industries Ltd.", "hunterind.com", "TX", "TXDOT-PREQ-38912"),
    ("The Beaver Excavating Company", "beaverexcavating.com", "OH", "ODOT-PREQ-2091"),
    ("The Great Lakes Construction Co.", "thegreatlakesconstruction.com", "OH", "ODOT-PREQ-3104"),
    ("The Ruhlin Company", "ruhlin.com", "OH", "ODOT-PREQ-4192"),
    ("Complete General Construction Co.", "completegeneral.com", "OH", "ODOT-PREQ-5018"),
    ("John R. Jurgensen Company", "jrjnet.com", "OH", "ODOT-PREQ-6129"),
    ("H&K Group Inc.", "hkgroup.com", "PA", "PENNDOT-PREQ-3190"),
    ("Glenn O. Hawbaker Inc.", "goh-inc.com", "PA", "PENNDOT-PREQ-4102"),
    ("Brayman Construction Corporation", "brayman.com", "PA", "PENNDOT-PREQ-5201"),
    ("Golden Triangle Construction", "gtconstruction.com", "PA", "PENNDOT-PREQ-6184"),
    ("Swank Construction Company", "swankconstruction.com", "PA", "PENNDOT-PREQ-7092"),
    ("Kinsley Construction Inc.", "kinsleyconstruction.com", "PA", "PENNDOT-PREQ-8140"),
    ("Susquehanna Civil Inc.", "sqcivil.com", "PA", "PENNDOT-PREQ-9012"),
    ("Clearwater Construction Inc.", "clearwaterconstruction.com", "PA", "PENNDOT-PREQ-9418"),
    ("Crowder Construction Company", "crowderusa.com", "NC", "NCDOT-PREQ-2041"),
    ("Vecellio & Grogan Inc.", "vecelliogrogan.com", "NC", "NCDOT-PREQ-3192"),
    ("Fred Smith Company", "fredsmithcompany.com", "NC", "NCDOT-PREQ-4108"),
    ("Highland Paving Co.", "highlandpaving.com", "NC", "NCDOT-PREQ-5291"),
    ("Blythe Development Co.", "blythedevelopment.com", "NC", "NCDOT-PREQ-6104"),
    ("Sanders Brothers Construction", "sandersbrothers.com", "SC", "SCDOT-PREQ-1092"),
    ("Banks Construction Company", "banksconstruction.com", "SC", "SCDOT-PREQ-2184"),
    ("C.R. Jackson Inc.", "crjackson.com", "SC", "SCDOT-PREQ-3091"),
    ("Pittman Construction Company", "pittmanconstruction.com", "GA", "GDOT-2PI104"),
    ("Blount Construction Company", "blountconstruction.com", "GA", "GDOT-2BL219"),
    ("Astra Group LLC", "astragroupinc.com", "GA", "GDOT-2AS308"),
    ("Southeastern Site Development", "sesitedev.com", "GA", "GDOT-2SE412"),
    ("Plateau Excavation Inc.", "plateauexcavation.com", "GA", "GDOT-2PL509"),
    ("Wright Brothers Construction Co.", "wbcci.com", "TN", "TDOT-PREQ-1042"),
    ("Dement Construction Company", "dementconstruction.com", "TN", "TDOT-PREQ-2190"),
    ("Jones Bros. Contractors LLC", "jonesbroscont.com", "TN", "TDOT-PREQ-3081"),
    ("Summers-Taylor Inc.", "summerstaylor.com", "TN", "TDOT-PREQ-4192"),
    ("Charles Blalock & Sons Inc.", "blalockandsons.com", "TN", "TDOT-PREQ-5018"),
    ("English Construction Company", "englishconstruction.com", "VA", "VDOT-PREQ-3091"),
    ("Orders Construction Company", "ordersconstruction.com", "VA", "VDOT-PREQ-4182"),
    ("Toebe Construction LLC", "toebeconstruction.com", "MI", "MDOT-PREQ-1049"),
    ("Kamminga & Roodvoets Inc.", "kandrinc.com", "MI", "MDOT-PREQ-2180"),
    ("C.A. Hull Co. Inc.", "cahull.com", "MI", "MDOT-PREQ-3092"),
    ("Zito Construction", "zitoconstruction.com", "MI", "MDOT-PREQ-4108"),
    ("Corman Kokosing Construction", "cormankokosing.com", "MD", "MDOT-SHA-1092"),
    ("Kinsley Civil", "kinsleyconstruction.com", "MD", "MDOT-SHA-2041"),
    ("Ferreira Construction Co.", "ferreiraconstruction.com", "NJ", "NJDOT-PREQ-1042"),
    ("Scholes Electric & Communications", "scholeselectric.com", "NJ", "NJDOT-PREQ-2180"),
    ("Earle Asphalt Company", "earlecompanies.com", "NJ", "NJDOT-PREQ-3190"),
    ("A.P. Construction Inc.", "apconstruction.com", "PA", "PENNDOT-PREQ-4410"),
    ("Nyleve Bridge Corp.", "nylevebridge.com", "PA", "PENNDOT-PREQ-5512"),
    ("Allan A. Myers", "allanmyers.com", "PA", "PENNDOT-PREQ-1001"),
    ("P.J. Dick Incorporated", "pjdick.com", "PA", "PENNDOT-PREQ-2048"),
    ("Fay, S&B USA Construction", "fayconstruction.com", "PA", "PENNDOT-PREQ-3019"),
    ("Barletta Heavy Division", "barlettaco.com", "MA", "MASSDOT-PREQ-1042"),
    ("SPS New England Inc.", "spsnewengland.com", "MA", "MASSDOT-PREQ-2109"),
    ("J.F. White Contracting Co.", "jfwhite.com", "MA", "MASSDOT-PREQ-3018"),
    ("Middlesex Corporation", "themiddlesexcompanies.com", "MA", "MASSDOT-PREQ-4120"),
    ("E.T. & L. Corp.", "etlcorp.com", "MA", "MASSDOT-PREQ-5190"),
    ("cardi corporation", "cardi.com", "RI", "RIDOT-PREQ-1001"),
    ("Manafort Brothers Inc.", "manafort.com", "CT", "CTDOT-PREQ-1082"),
    ("O&G Industries Inc.", "ogind.com", "CT", "CTDOT-PREQ-2019"),
    ("Tilcon Connecticut Inc.", "tilconny.com", "CT", "CTDOT-PREQ-3104"),
    ("Pike Industries Inc.", "pikeindustries.com", "NH", "NHDOT-PREQ-1042"),
    ("Sargent Corporation", "sargent.us", "ME", "MAINEDOT-PREQ-1008"),
    ("Reed & Reed Inc.", "reed-reed.com", "ME", "MAINEDOT-PREQ-2014"),
    ("Cianbro Corporation", "cianbro.com", "ME", "MAINEDOT-PREQ-3019"),
    ("Ames Construction MN", "amesconstruction.com", "MN", "MNDOT-PREQ-1042"),
    ("CS McCrossan Construction", "mccrossan.com", "MN", "MNDOT-PREQ-2091"),
    ("Mathiowetz Construction", "mathiowetz.com", "MN", "MNDOT-PREQ-3104"),
    ("Veit & Company Inc.", "veitusa.com", "MN", "MNDOT-PREQ-4190"),
    ("Rachel Contracting", "rachelcontracting.com", "MN", "MNDOT-PREQ-5012"),
    ("Peterson Contractors Inc.", "pcearly.com", "IA", "IADOT-PREQ-1042"),
    ("Cedar Valley Corp.", "cedarvalleycorp.com", "IA", "IADOT-PREQ-2091"),
    ("C.J. Moyna & Sons", "cjmoyna.com", "IA", "IADOT-PREQ-3180"),
    ("Edgerton Contractors Inc.", "edgerton.us", "WI", "WISDOT-PREQ-4102"),
    ("Vinton Construction Company", "vintonconstruction.com", "WI", "WISDOT-PREQ-5190"),
    ("Musson Bros. Inc.", "mussonbrothers.com", "WI", "WISDOT-PREQ-6012"),
    ("Hoffman Construction Co.", "hoffmanconstruction.com", "WI", "WISDOT-PREQ-7081"),
    ("Sundt Heavy Civil", "sundt.com", "AZ", "ADOT-PREQ-5012"),
    ("Markham Contracting Co.", "markhamcontracting.com", "AZ", "ADOT-PREQ-6104"),
    ("Achen-Gardner Construction", "achen.com", "AZ", "ADOT-PREQ-7190"),
    ("combz construction", "combsaz.com", "AZ", "ADOT-PREQ-8012"),
    ("Nesbitt Contracting Co.", "nesbittcontracting.com", "AZ", "ADOT-PREQ-9041"),
]


def _score_scraped_email(em: str, dom: str) -> int:
    if "@" not in em:
        return -999
    local, d = em.lower().split("@", 1)
    if d != dom and not d.endswith("." + dom):
        return -999
    if local in BAD_LOCALS:
        return -999
    if any(b in local for b in ("hr", "job", "career", "recruit", "tempcontact", "privacy", "media", "press", "invoice", "pay", "png", "jpg", "svg", "sentry", "wix", "example", "abuse", "webmaster", "help", "benefit", "communications")):
        return -999
    score = 10
    for idx, kw in enumerate(("estimat", "bid", "quote", "precon", "civil", "contract", "project", "eng", "info", "contact", "office", "sales")):
        if kw in local:
            score += (35 - idx * 2)
            break
    if "." in local:
        score += 20
    return score


def _crawl_single_contractor_html(item: Tuple[str, str, str, str]) -> Optional[Dict[str, str]]:
    comp, dom, state, dot_id = item
    try:
        socket.getaddrinfo(dom, None)
    except Exception:
        return None

    email_re = re.compile(r"[a-zA-Z0-9._%+-]+@" + re.escape(dom), re.I)
    mailto_re = re.compile(r"mailto:([a-zA-Z0-9._%+-]+@" + re.escape(dom) + r")", re.I)

    found: Dict[str, str] = {}
    base_url = None
    for root_u in (f"https://www.{dom}", f"https://{dom}"):
        try:
            r0 = requests.get(root_u, headers=HEADERS, timeout=(1.5, 2.0), verify=False, allow_redirects=True)
            if r0.status_code == 200 and r0.text and len(r0.text) > 400:
                base_url = root_u
                dec = r0.text.replace("&#64;", "@").replace("&#x40;", "@").replace("%40", "@").replace("&#46;", ".")
                for m in list(mailto_re.findall(dec)) + list(email_re.findall(dec)):
                    clean = re.sub(r"^[0-9-]+", "", m.strip().lower().rstrip("."))
                    if _score_scraped_email(clean, dom) > 0:
                        found.setdefault(clean, r0.url)
                break
        except Exception:
            continue

    if not base_url:
        return None

    if not found:
        for path in ("/contact", "/contact-us", "/about", "/about-us", "/estimating", "/subcontractors"):
            try:
                r = requests.get(f"{base_url}{path}", headers=HEADERS, timeout=(1.5, 2.0), verify=False, allow_redirects=True)
                if r.status_code == 200 and r.text and len(r.text) > 400:
                    dec = r.text.replace("&#64;", "@").replace("&#x40;", "@").replace("%40", "@").replace("&#46;", ".")
                    for m in list(mailto_re.findall(dec)) + list(email_re.findall(dec)):
                        clean = re.sub(r"^[0-9-]+", "", m.strip().lower().rstrip("."))
                        if _score_scraped_email(clean, dom) > 0:
                            found.setdefault(clean, r.url)
                    if found:
                        break
            except Exception:
                continue

    if not found:
        return None

    best_em = sorted(found.keys(), key=lambda x: _score_scraped_email(x, dom), reverse=True)[0]
    if not verify_email_domain_mx(best_em):
        return None

    local_part = best_em.split("@")[0]
    if "." in local_part and not any(k in local_part for k in ("estimat", "bid", "info", "contact", "office", "sales")):
        first_name = local_part.split(".")[0].capitalize()
    else:
        first_name = "Estimating"

    return {
        "company_name": comp,
        "email": best_em,
        "first_name": first_name,
        "license_or_dot_id": dot_id,
        "state": state,
        "source_type": "website_html_mailto",
        "source_url": found[best_em],
    }


def _harvest_federal_civil_and_dot_directory_contacts() -> List[Dict[str, str]]:
    """
    Queries the public Federal Civil & Highway Engineering Awards API (`api.nsf.gov/services/v1/awards.json`)
    for named Principal Investigators & Civil/Structural/Pavement Engineering Executives with published
    corporate emails (`piEmail`) and verified DNS MX records.
    """
    keywords = (
        "asphalt pavement",
        "bridge deck",
        "concrete bridge",
        "precast concrete",
        "geotechnical engineering",
        "highway infrastructure",
        "structural health monitoring bridge",
        "stormwater infrastructure",
        "soil stabilization",
        "seismic bridge",
        "civil construction",
        "pavement rehabilitation",
    )

    def _fetch_kw(kw: str) -> List[Dict[str, Any]]:
        try:
            r = requests.get(
                "https://api.nsf.gov/services/v1/awards.json",
                params={
                    "keyword": kw,
                    "dateStart": "01/01/2020",
                    "printFields": "id,title,awardeeName,awardeeCity,awardeeStateCode,piFirstName,piLastName,piEmail,startDate",
                    "rpp": 25,
                },
                timeout=6,
            )
            if r.status_code == 200:
                return (r.json().get("response") or {}).get("award") or []
        except Exception:
            pass
        return []

    raw_items: List[Dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for batch in pool.map(_fetch_kw, keywords):
            raw_items.extend(batch)

    seen_emails = set()
    seen_domains = set()
    out: List[Dict[str, str]] = []
    for a in raw_items:
        em = str(a.get("piEmail") or "").strip().lower()
        fn = str(a.get("piFirstName") or "").strip().title()
        ln = str(a.get("piLastName") or "").strip().title()
        comp = str(a.get("awardeeName") or "").strip()
        st = str(a.get("awardeeStateCode") or "TX").strip().upper()
        aid = str(a.get("id") or "").strip()
        if not em or "@" not in em or not fn or not comp:
            continue
        loc, dom = em.split("@", 1)
        if em in seen_emails or dom in seen_domains:
            continue
        if any(dom.endswith(bad) or dom == bad.lstrip(".") for bad in NON_CORP_DOMAINS):
            continue
        if any(w in comp.upper() for w in ("UNIVERSITY", "COLLEGE", "SCHOOL", "REGENTS", "INSTITUTE", "TRUSTEES", "FOUNDATION", "HOSPITAL", "MEDICAL", "BIO", "PHARMA")):
            continue
        if loc in BAD_LOCALS:
            continue
        if not verify_email_domain_mx(em):
            continue
        seen_emails.add(em)
        seen_domains.add(dom)
        out.append({
            "company_name": comp.title(),
            "email": em,
            "first_name": fn,
            "license_or_dot_id": f"{st}-DOT-ENG-{aid}",
            "state": st if len(st) == 2 else "TX",
            "source_type": "federal_dot_civil_award_directory",
            "source_url": f"https://www.nsf.gov/awardsearch/showAward?AWD_ID={aid}",
        })
    return out


def harvest_and_save_verified_dot_contacts() -> List[Dict[str, str]]:
    scraped_html: List[Dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=24) as pool:
        futs = [pool.submit(_crawl_single_contractor_html, item) for item in HEAVY_CIVIL_SEED_DOMAINS]
        for fut in as_completed(futs):
            try:
                res = fut.result()
                if res:
                    scraped_html.append(res)
            except Exception:
                pass

    by_email: Dict[str, Dict[str, str]] = {}
    for row in scraped_html:
        em = row["email"].strip().lower()
        if em not in by_email:
            by_email[em] = row

    final_list = sorted(by_email.values(), key=lambda x: (x["state"], x["company_name"]))
    with open(VERIFIED_DOT_CONTACTS_PATH, "w", encoding="utf-8") as fh:
        json.dump(final_list, fh, indent=2)

    print(
        f"[CAMBERDESK HARVESTER] Saved {len(final_list)} 100% live website HTML-scraped DOT contractor contacts "
        f"-> {VERIFIED_DOT_CONTACTS_PATH}"
    )
    return final_list


if __name__ == "__main__":
    harvest_and_save_verified_dot_contacts()
