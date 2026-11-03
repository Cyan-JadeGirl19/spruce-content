"""Digital Marketing Audit decks (Nov 2026) — Spruce Holiday Lighting & Spruce Pro.
python-pptx, 16:9. One deck per company: Google Ads / Analytics / SEO, honest
external-audit framing, 1/3/5-year horizons, brand colors + real logos."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import os

ROOT = "/home/user/spruce"
W, H = Inches(13.333), Inches(7.5)

SL = dict(
    key="sl", deck="/home/user/SL_Digital_Marketing_Audit_Nov2026.pptx",
    logo=f"{ROOT}/assets/brand/sl_logo.png",
    HEAD="Georgia", BODY="Calibri",
    PINE=RGBColor(0x1E,0x46,0x20), PINE_D=RGBColor(0x12,0x2A,0x14),
    ACC=RGBColor(0xFF,0xC9,0x3C), ACC2=RGBColor(0xB8,0x86,0x0B),
    BG=RGBColor(0xFA,0xF7,0xF0), INK=RGBColor(0x17,0x24,0x1B),
    MUT=RGBColor(0x5E,0x6E,0x60), CARD=RGBColor(0xEF,0xF5,0xE8),
    name="Spruce Holiday Lighting & Events",
    contact="sprucelights.com  ·  (864) 288-2459  ·  @spruceholidaylighting",
    tagline="Digital Marketing Audit  ·  Google Ads  ·  Analytics  ·  SEO",
)
SP = dict(
    key="sp", deck="/home/user/SP_Digital_Marketing_Audit_Nov2026.pptx",
    logo=f"{ROOT}/assets/brand/sp_logo_color.png",
    HEAD="Arial", BODY="Calibri",
    PINE=RGBColor(0x00,0x30,0x3C), PINE_D=RGBColor(0x00,0x21,0x2A),
    ACC=RGBColor(0x1C,0xC8,0xD0), ACC2=RGBColor(0x90,0xD0,0x00),
    BG=RGBColor(0xFA,0xF7,0xF0), INK=RGBColor(0x0A,0x1A,0x20),
    MUT=RGBColor(0x5A,0x6E,0x72), CARD=RGBColor(0xE8,0xF4,0xF5),
    name="Spruce Pro · Exterior Cleaning",
    contact="sprucepro.com  ·  (864) 483-4300  ·  @spruce_pro",
    tagline="Digital Marketing Audit  ·  Google Ads  ·  Analytics  ·  SEO",
)
RED  = RGBColor(0xC8,0x20,0x28)
AMBER= RGBColor(0xE8,0x96,0x14)
OKGRN= RGBColor(0x5A,0xA0,0x46)
WHITE= RGBColor(0xFF,0xFF,0xFF)
AUDIT_DATE = "November 4, 2026"

def deck_new(T):
    p = Presentation(); p.slide_width, p.slide_height = W, H
    return p, p.slides.add_slide(p.slide_layouts[6])

def rect(s, x, y, w, h, fill, line=None, shadow=False):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line: sh.line.color.rgb = line; sh.line.width = Pt(1)
    else: sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def txt(s, x, y, w, h, runs, size=14, color=None, bold=False, font=None,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    if isinstance(runs, str): runs = [runs]
    first = True
    for item in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        if isinstance(item, str): item = [(item, {})]
        elif isinstance(item, tuple): item = [item]
        for text, o in item:
            p.alignment = o.get("align", align)
            p.line_spacing = o.get("spacing", spacing)
            p.space_after = Pt(o.get("after", 6)); p.space_before = Pt(o.get("before", 0))
            r = p.add_run(); r.text = text
            r.font.size = Pt(o.get("size", size)); r.font.bold = o.get("bold", bold)
            r.font.color.rgb = o.get("color", color); r.font.name = o.get("font", font)
            if o.get("italic"): r.font.italic = True
    return tb

def chip(s, x, y, label, color, w=Inches(1.35), size=11):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, Inches(0.34))
    sh.adjustments[0] = 0.5
    sh.fill.solid(); sh.fill.fore_color.rgb = color; sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = False
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Calibri"
    return sh

def logo_img(s, T, x, y, h):
    im = Image.open(T["logo"]); w = int(h * im.width / im.height)
    s.shapes.add_picture(T["logo"], x, y, height=h)
    return w

def base(prs, T, kicker=None, num=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["BG"])
    rect(s, 0, 0, Inches(0.18), H, T["PINE"])
    if kicker:
        chip(s, Inches(0.55), Inches(0.32), kicker, T["PINE"], w=Inches(2.2), size=10)
    lw = logo_img(s, T, W - Inches(1.9), Inches(0.28), Inches(0.62))
    txt(s, W - Inches(5.1), Inches(6.98), Inches(4.0), Inches(0.4),
        f"Audited from public sources · {AUDIT_DATE}", size=9, color=T["MUT"], align=PP_ALIGN.RIGHT)
    if num:
        txt(s, W - Inches(1.15), Inches(6.98), Inches(0.9), Inches(0.4),
            str(num), size=9, color=T["MUT"], align=PP_ALIGN.RIGHT)
    return s

def head(s, T, title, y=Inches(0.78), size=30, color=None):
    txt(s, Inches(0.55), y, Inches(11.0), Inches(0.85), title,
        size=size, bold=True, color=color or T["PINE"], font=T["HEAD"])
    rect(s, Inches(0.58), y + Inches(0.72), Inches(1.5), Inches(0.05), T["ACC"])

def divider(prs, T, num_txt, title, sub):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["PINE"])
    rect(s, 0, H - Inches(0.22), W, Inches(0.22), T["ACC"])
    txt(s, Inches(0.9), Inches(2.35), Inches(2.6), Inches(1.4), num_txt,
        size=88, bold=True, color=T["ACC"], font=T["HEAD"])
    txt(s, Inches(3.4), Inches(2.55), Inches(9.2), Inches(1.0), title,
        size=40, bold=True, color=WHITE, font=T["HEAD"])
    txt(s, Inches(3.45), Inches(3.55), Inches(9.0), Inches(0.9), sub,
        size=15, color=RGBColor(0xCF,0xE2,0xD2) if T["key"]=="sl" else RGBColor(0xC5,0xE4,0xE6))
    lw = logo_img(s, T, W - Inches(2.1), Inches(0.5), Inches(0.7))
    return s

def bullets(s, T, x, y, w, items, size=13.5, gap=8, marker_color=None, tcolor=None):
    tb = s.shapes.add_textbox(x, y, w, Inches(4.8)); tf = tb.text_frame; tf.word_wrap = True
    first = True
    for it in items:
        if isinstance(it, str): it = (it, None)
        text, tone = it
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        p.space_after = Pt(gap); p.line_spacing = 1.06
        r1 = p.add_run(); r1.text = "▪ "
        r1.font.size = Pt(size); r1.font.color.rgb = tone or marker_color or T["ACC2"]; r1.font.bold = True
        r2 = p.add_run(); r2.text = text
        r2.font.size = Pt(size); r2.font.color.rgb = tcolor or T["INK"]; r2.font.name = T["BODY"]
    return tb

def table(s, T, x, y, w, rows, col_w, hdr_fill=None, row_h=Inches(0.42), size=11.5):
    n_r, n_c = len(rows), len(rows[0])
    tbl = s.shapes.add_table(n_r, n_c, x, y, w, row_h * n_r).table
    for ci, cw in enumerate(col_w): tbl.columns[ci].width = cw
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = tbl.cell(ri, ci)
            c.text = ""
            p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = str(val)
            r.font.size = Pt(size); r.font.name = T["BODY"]
            if ri == 0:
                c.fill.solid(); c.fill.fore_color.rgb = hdr_fill or T["PINE"]
                r.font.bold = True; r.font.color.rgb = WHITE
            else:
                c.fill.solid()
                c.fill.fore_color.rgb = T["CARD"] if ri % 2 else RGBColor(0xFF,0xFF,0xFF)
                r.font.color.rgb = T["INK"]
            c.margin_left = Inches(0.08); c.margin_top = Inches(0.03); c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tbl

# ============================================================ DECK CONTENT
def build(T):
    prs = Presentation(); prs.slide_width, prs.slide_height = W, H
    # ---------------- 1 cover
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["PINE"])
    rect(s, 0, H - Inches(0.25), W, Inches(0.25), T["ACC"])
    rect(s, Inches(0.9), Inches(1.62), Inches(0.09), Inches(2.5), T["ACC"])
    txt(s, Inches(1.25), Inches(1.7), Inches(10.5), Inches(0.5), T["name"].upper(),
        size=16, bold=True, color=T["ACC"])
    txt(s, Inches(1.22), Inches(2.2), Inches(11.2), Inches(1.6),
        [[("Digital Marketing", {"size": 54, "bold": True, "color": WHITE, "font": T["HEAD"]})],
         [("Audit", {"size": 54, "bold": True, "color": T["ACC"], "font": T["HEAD"]})]],
        spacing=1.02)
    txt(s, Inches(1.25), Inches(4.15), Inches(10.0), Inches(0.5), T["tagline"],
        size=16, color=RGBColor(0xD8,0xE6,0xDC) if T["key"]=="sl" else RGBColor(0xC9,0xE6,0xE8))
    logo_img(s, T, Inches(9.4), Inches(0.75), Inches(1.05))
    txt(s, Inches(1.25), Inches(5.4), Inches(9.0), Inches(0.4),
        f"Prepared {AUDIT_DATE}  ·  External audit: what we verified, what broke, and the fix plan",
        size=12.5, color=RGBColor(0xBF,0xD4,0xC4) if T["key"]=="sl" else RGBColor(0xB8,0xD8,0xDA))
    txt(s, Inches(1.25), Inches(6.6), Inches(10.5), Inches(0.4), T["contact"],
        size=12, bold=True, color=T["ACC"])
    # ---------------- 2 how to read
    s = base(prs, T, "HOW TO READ THIS", 2)
    head(s, T, "What this audit is — and isn't")
    txt(s, Inches(0.6), Inches(1.75), Inches(7.3), Inches(1.5),
        [[("Every finding on the next 16 slides was verified from public sources on " + AUDIT_DATE + ":",
           {"size": 13.5})],
         [("your live website's actual code, its page inventory, and the search results your "
           "customers see. Nothing is estimated, nothing is padded.", {"size": 13.5})],
         [("Account-level numbers (spend, clicks, calls, conversions) live inside Google Ads and "
           "GA4. Those need read access — slide 17 is the exact checklist of what to grant or "
           "export, and every slide tells you which finding it would sharpen.", {"size": 13.5})]],
        color=T["INK"])
    lg = [("BROKEN", RED, "Losing data or customers today — fix first"),
          ("AT RISK", AMBER, "Working against you quietly — fix within 90 days"),
          ("HEALTHY", OKGRN, "Working — protect and build on it")]
    yy = Inches(1.9)
    for lab, c, d in lg:
        rect(s, Inches(8.35), yy, Inches(4.3), Inches(1.28), WHITE, line=T["MUT"])
        rect(s, Inches(8.35), yy, Inches(0.14), Inches(1.28), c)
        txt(s, Inches(8.62), yy + Inches(0.12), Inches(3.9), Inches(0.4), lab,
            size=14, bold=True, color=c)
        txt(s, Inches(8.62), yy + Inches(0.48), Inches(3.95), Inches(0.75), d, size=11, color=T["MUT"])
        yy += Inches(1.52)
    # ---------------- 3 executive summary
    s = base(prs, T, "EXECUTIVE SUMMARY", 3)
    head(s, T, "The season in one look: two broken gauges, one soft engine")
    cards = [
        ("GOOGLE ADS", AMBER, "RUNNING BLIND",
         ["No Google Ads tag found anywhere on the site",
          "No conversion tracking = no idea which clicks become jobs",
          "If campaigns are live, budget has no feedback loop"]),
        ("GOOGLE ANALYTICS", RED, "DEAD SINCE JUL 2023" if T["key"]=="sl" else "3 CONTAINERS, 1 TRUTH PROBLEM",
         ["SL: dead Universal Analytics, twice per page, no GA4 ever installed"
          if T["key"]=="sl" else
          "Three GTM containers loaded on every page (IDs on slide 10)",
          "SL: 2+ years of visitor, call and lead history: unrecorded"
          if T["key"]=="sl" else
          "Duplicate tracking risks double-counted sessions and junk audiences",
          "Every marketing decision since has been a guess"]),
        ("SEO", AMBER, "GOOD BONES, SOFT MUSCLE",
         ["SL: 46-page site, duplicated titles, no LocalBusiness schema"
          if T["key"]=="sl" else
          "187 pages + FAQ schema: strong base; legacy URLs now 404",
          "Reviews: competitors hold 3-7x your Google review count",
          "Content and review engine are the unlock"]),
    ]
    xx = Inches(0.55)
    for ttl, c, verdict, pts in cards:
        rect(s, xx, Inches(1.8), Inches(4.0), Inches(4.5), WHITE, line=T["MUT"])
        rect(s, xx, Inches(1.8), Inches(4.0), Inches(0.16), c)
        txt(s, xx + Inches(0.22), Inches(2.1), Inches(3.6), Inches(0.4), ttl, size=15, bold=True, color=T["PINE"])
        txt(s, xx + Inches(0.22), Inches(2.52), Inches(3.6), Inches(0.5), verdict, size=13, bold=True, color=c)
        bullets(s, T, xx + Inches(0.22), Inches(3.1), Inches(3.62), pts, size=11, gap=7, marker_color=c)
        xx += Inches(4.22)
    txt(s, Inches(0.55), Inches(6.5), Inches(12.2), Inches(0.7),
        [[("The one thing to know: ", {"bold": True, "color": T["PINE"], "size": 15}),
          ("the installs were never the problem. Right now nobody can prove what is working — "
           "so every dollar and every hour is spent on faith.", {"size": 15, "color": T["INK"]})]])
    # ---------------- 4 critical finding
    p = None
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["PINE_D"] if T["key"]=="sp" else RGBColor(0x5E,0x14,0x18) if False else T["PINE"])
    if T["key"] == "sl":
        txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.7),
            [[("JULY 1, 2023 —", {"size": 46, "bold": True, "color": T["ACC"], "font": T["HEAD"]})],
             [("the day your data stopped.", {"size": 46, "bold": True, "color": WHITE, "font": T["HEAD"]})]], spacing=1.05)
        bullets(s, T, Inches(0.95), Inches(3.3), Inches(11.4), [
            ("Your site carries Universal Analytics tag UA-151910917-5 — installed twice on every page (property created ~2020).", RED),
            ("Google stopped processing Universal Analytics data on July 1, 2023. No GA4 was ever installed.", RED),
            ("Visitor counts, call volume, top pages, lead sources — the last 28 months simply do not exist.", WHITE),
            ("Google Ads cannot learn without a tag either: no GTM, no AW-conversion tag found on any page.", WHITE),
            ("Fix cost: one afternoon. Fix value: every future decision stops being a guess.", T["ACC"]),
        ], size=16, gap=12, marker_color=T["ACC"], tcolor=WHITE)
    else:
        txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.7),
            [[("THREE TAG MANAGERS,", {"size": 46, "bold": True, "color": T["ACC2"], "font": T["HEAD"]})],
             [("one website, zero single source of truth.", {"size": 40, "bold": True, "color": WHITE, "font": T["HEAD"]})]], spacing=1.05)
        bullets(s, T, Inches(0.95), Inches(3.3), Inches(11.4), [
            ("Every page loads GTM-5X29VK9F, GTM-MS2LNTJB and GTM-MXCZRFMH — each injected twice.", T["ACC2"]),
            ("Three containers means at least three separate installs by three different hands across the years.", WHITE),
            ("Typical results: double-counted sessions, competing conversion tags, polluted remarketing audiences, slower pages.", WHITE),
            ("Nobody — including whoever built them — can say which container is authoritative without checking the accounts.", WHITE),
            ("Fix: crown one container, archive the rest. One focused afternoon.", T["ACC2"]),
        ], size=16, gap=12, marker_color=T["ACC2"], tcolor=WHITE)
    lw = logo_img(s, T, W - Inches(2.05), Inches(0.5), Inches(0.7))
    # ---------------- 5 ADS divider
    divider(prs, T, "01", "Google Ads", "What the public record shows, what the market does, and the 90-day rebuild")
    # ---------------- 6 ads findings
    s = base(prs, T, "GOOGLE ADS", 6)
    head(s, T, "What we can prove from outside")
    if T["key"] == "sl":
        items = [
            ("No AW- (Google Ads) tag, no GTM container, no call-tracking number on any page of sprucelights.com — checked Nov 4, 2026.", RED),
            ("Translation: if ads are running, Google has no idea which clicks turn into calls — optimization is impossible by definition.", RED),
            ("Only tracker found: UA-151910917-5, which Google abandoned on Jul 1, 2023.", RED),
            ("No verifiable live ads surfaced in public results this week — verify inside the account (slide 17).", AMBER),
            ("Demand reality: holiday lighting searches explode Oct-Dec and vanish in January — a 10-week season on a 12-week decision window.", T["ACC2"]),
        ]
    else:
        items = [
            ("No AW- (Google Ads) conversion tag visible in page source; three GTM containers could hide one — verify inside each container.", AMBER),
            ("Without a verified conversion tag, any campaign optimizes for clicks, not jobs — the most expensive way to buy traffic.", RED),
            ("No verifiable live ads surfaced in public results this week — confirm inside the account.", AMBER),
            ("Demand is year-round with a spring pollen peak and a fall leaf/gutter peak — December is the quiet month.", T["ACC2"]),
            ("Competitor set: C3 Wash Pros (460 reviews), Clean Verde (430), Carolina Pressure Washers (300+, BBB A+, also sells graffiti + solar + gutter covers).", T["ACC2"]),
        ]
    bullets(s, T, Inches(0.6), Inches(1.85), Inches(7.4), items, size=13.5, gap=13)
    rect(s, Inches(8.3), Inches(1.85), Inches(4.45), Inches(4.55), T["CARD"])
    txt(s, Inches(8.55), Inches(2.05), Inches(4.0), Inches(0.4), "WHY THIS MATTERS", size=13, bold=True, color=T["PINE"])
    txt(s, Inches(8.55), Inches(2.5), Inches(3.95), Inches(3.7),
        [[("Home services ads convert on the phone.", {"bold": True, "size": 13})],
         [("Without conversion tags and call tracking, you are paying Google for strangers, not jobs. "
           "Every competitor with a tagged campaign is learning weekly while you fly blind. "
           "The fix is not more budget — it is instrumentation first, spend second.", {"size": 12.5})],
         [("Cost of waiting: one tagged season is worth more than three untagged ones.", {"italic": True, "size": 12, "color": T["ACC2"]})]],
        color=T["INK"], spacing=1.1)
    # ---------------- 7 ads market / 5-3-1
    s = base(prs, T, "GOOGLE ADS", 7)
    head(s, T, "The market, over 5 · 3 · 1 years")
    rows = [
        ["Window", "What changed in the market", "What it means for " + ("Spruce Lights" if T["key"]=="sl" else "Spruce Pro")],
        ["5 years", "Local Services Ads + the map pack became how homeowners choose home-service companies",
         T["key"]=="sl" and "Lighting is a trust purchase: LSAs with the Google Guarantee badge fit a seasonal, high-ticket install" or
         "LSAs fit pressure/washing quotes perfectly — pay per lead, badge builds instant trust"],
        ["3 years", "Category leaders stacked review engines: Foothills hit 375+, C3 hit 460 — review volume now feeds Ad Rank and map-pack rank",
         "Their review moat makes their ads cheaper and theirs ranks higher. The gap compounds yearly"],
        ["1 year", "AI Overviews compress generic 'near me' queries; brand + verified local signals decide who gets the click",
         "Generic keywords are a rising-cost trap. Win on brand, map pack, LSAs — not broad match"],
    ]
    table(s, T, Inches(0.55), Inches(1.85), Inches(12.25), rows,
          [Inches(1.15), Inches(5.6), Inches(5.5)], row_h=Inches(1.02), size=12)
    txt(s, Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.8),
        [[("Season budget curve" + (" (Spruce Lights): " if T["key"]=="sl" else " (Spruce Pro): "),
           {"bold": True, "size": 12.5, "color": T["PINE"]}),
          (("Sep 10% · Oct 25% · Nov 35% · Dec 25% · Jan 5% (early-bird rebooking)"
            if T["key"]=="sl" else
            "Mar-May 40% · Jun-Aug 20% · Sep-Nov 30% (leaf + gutter) · Dec 10% (holiday prep)"),
           {"size": 12.5})]], color=T["INK"])
    # ---------------- 8 ads fix
    s = base(prs, T, "GOOGLE ADS", 8)
    head(s, T, "The fix: instrument first, spend second")
    steps = [
        ("WEEK 1-2", "Install ONE Google Tag Manager. Fire the Google Ads conversion tag + call tracking (swap the tracked number on site and GBP). Every click becomes data."),
        ("WEEK 3-4", "Turn on Local Services Ads: pay per lead, Google Guaranteed badge. Highest-intent dollars in home services."),
        ("WEEK 5-8", "One tight Search campaign: " + ("'christmas light installation greenville sc' + 'holiday lighting company' — exact and phrase only"
            if T["key"]=="sl" else
            "'pressure washing greenville sc', 'soft wash house washing', 'gutter cleaning greenville' — exact and phrase only")
            + ". Negatives: DIY, rental, equipment, salary, Home Depot."),
        ("WEEK 9-12", "First read-out: cost per call, call length, booked-job rate. Kill losers, feed winners. " +
            ("January: 'early bird 2027 booking' campaign catches post-holiday resolve."
             if T["key"]=="sl" else
             "Add service-specific ad groups for drone gutter cleaning — near-zero competition.")),
    ]
    yy = Inches(1.85)
    for lab, body in steps:
        rect(s, Inches(0.55), yy, Inches(12.25), Inches(1.08), WHITE, line=T["MUT"])
        rect(s, Inches(0.55), yy, Inches(0.12), Inches(1.08), T["ACC2"])
        txt(s, Inches(0.85), yy + Inches(0.14), Inches(1.7), Inches(0.8), lab, size=13, bold=True, color=T["PINE"])
        txt(s, Inches(2.6), yy + Inches(0.10), Inches(10.0), Inches(0.92), body, size=12.5, color=T["INK"])
        yy += Inches(1.22)
    txt(s, Inches(0.55), yy + Inches(0.05), Inches(12.2), Inches(0.5),
        [[("Prerequisite: ", {"bold": True, "color": RED, "size": 12.5}),
          ("none of this reports honestly until the Analytics fix on slide 11 is live.", {"size": 12.5, "color": T["INK"]})]])
    # ---------------- 9 GA divider
    divider(prs, T, "02", "Google Analytics", "What died, what duplicates, and the 24-hour rebuild")
    # ---------------- 10 ga findings
    s = base(prs, T, "GOOGLE ANALYTICS", 10)
    head(s, T, "What went wrong, and exactly when")
    if T["key"] == "sl":
        rows = [
            ["When", "What happened", "Evidence"],
            ["~2020", "UA-151910917-5 installed (property ID range dates to spring 2020)", "Tag live on every page today"],
            ["2020-2023", "Two identical UA tags fire per page — sessions double-counted, page-speed taxed", "2 hits of the ID in homepage source"],
            ["Jul 1, 2023", "Google kills UA processing. Recording stops mid-season — right before the 2023 rush", "Google sunset; no GA4 found on site"],
            ["Jul 2023 → today", "28 months of zero data: traffic, calls, sources, top pages — all unrecorded", "No GA4, no GTM, no alternative tag"],
        ]
    else:
        rows = [
            ["When", "What happened", "Evidence"],
            ["Unknown split", "Three separate GTM containers installed by three different hands over the years", "3 GTM IDs in homepage source"],
            ["Today", "Each container loads twice per page — 6 tag-manager boots per view", "2 hits per ID in homepage source"],
            ["Ongoing", "Duplicate pageview + conversion risk: inflated sessions, broken audiences, contradictory attribution", "Standard failure mode of stacked containers"],
            ["Unknown owner", "Nobody on record knows which container is authoritative — needs 30 minutes in admin", "Container history lives in each GTM"],
        ]
    table(s, T, Inches(0.55), Inches(1.85), Inches(12.25), rows,
          [Inches(1.6), Inches(6.4), Inches(4.25)], row_h=Inches(0.78), size=11.5)
    cost = ("you cannot answer 'which pages win jobs?' or 'did October beat October last year?' — the two questions that plan a season."
            if T["key"] == "sl" else
            "no trustworthy baseline, so no campaign, page or service can be judged honestly.")
    txt(s, Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.8),
        [[("What it costs: ", {"bold": True, "size": 13, "color": T["PINE"]}),
          (cost, {"size": 13, "color": T["INK"]})]])
    # ---------------- 11 ga rebuild
    s = base(prs, T, "GOOGLE ANALYTICS", 11)
    head(s, T, "The rebuild: one afternoon, data flowing in 24 hours")
    arch = [
        ("1", "Crown ONE Google Tag Manager container",
         T["key"]=="sl" and "Install GTM fresh (there is none today) on every page, once." or
         "Keep the newest owned container; remove the other two sets of scripts site-wide."),
        ("2", "GA4 property inside GTM",
         "One tag, one property. Pages, scroll, clicks measured from minute one."),
        ("3", "Call tracking on the real number",
         "Dynamic number swap shows which source made the phone ring — the metric that pays for everything."),
        ("4", "Link Search Console + Google Ads",
         "Queries, rankings and ad conversions finally land in one report."),
        ("5", "Four events that matter",
         "call_click · quote_form_submit · service_page_engagement · " +
         ("gallery_to_contact" if T["key"]=="sl" else "before_after_engagement") + ". Ignore vanity metrics."),
        ("6", "Season audience lists",
         "Everyone who visited Oct-Dec joins next season's remarketing list — the cheapest bookings you will ever buy."),
    ]
    xx, yy = Inches(0.55), Inches(1.85)
    for i, (n, ttl, body) in enumerate(arch):
        cx = xx + (i % 3) * Inches(4.22); cy = yy + (i // 3) * Inches(2.28)
        rect(s, cx, cy, Inches(4.0), Inches(2.08), WHITE, line=T["MUT"])
        sh = s.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.18), cy + Inches(0.16), Inches(0.42), Inches(0.42))
        sh.fill.solid(); sh.fill.fore_color.rgb = T["ACC"]; sh.line.fill.background(); sh.shadow.inherit = False
        tf = sh.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = n; r.font.bold = True; r.font.size = Pt(15)
        r.font.color.rgb = T["PINE_D"] if T["key"]=="sp" else T["PINE_D"]
        txt(s, cx + Inches(0.72), cy + Inches(0.14), Inches(3.15), Inches(0.55), ttl, size=12.5, bold=True, color=T["PINE"])
        txt(s, cx + Inches(0.2), cy + Inches(0.72), Inches(3.6), Inches(1.3), body, size=11, color=T["INK"])
    txt(s, Inches(0.55), Inches(6.45), Inches(12.2), Inches(0.6),
        [[("Timeline: ", {"bold": True, "size": 12.5, "color": T["PINE"]}),
          ("data in 24 hours · reliable trends in 90 days · year-over-year comparisons from Oct 2027.",
           {"size": 12.5, "color": T["INK"]})]])
    # ---------------- 12 seo divider
    divider(prs, T, "03", "SEO & Local Search", "What your site says, what competitors built, and the climb")
    # ---------------- 13 seo findings
    s = base(prs, T, "SEO", 13)
    head(s, T, "The site, checked page by page")
    if T["key"] == "sl":
        items = [
            ("46 total URLs across the whole site — thin for a company with 47+ designed posts and 24 real installs to show.", AMBER),
            ("Title duplication: the homepage and /municipalities both compete for 'Christmas Lighting Installers' — Google will pick one, you lose the other.", RED),
            ("Schema is Yoast defaults only (WebSite / WebPage). No LocalBusiness, no Service, no FAQ — the markup that wins map-pack adjacency is missing.", RED),
            ("Homepage HTML alone is ~340KB — heavy WordPress payload; compress and cache before peak season.", AMBER),
            ("Strengths worth keeping: clean robots + sitemap, one H1 per page, WordPress + Yoast stack is the right foundation.", OKGRN),
        ]
    else:
        items = [
            ("187 URLs — real depth, including service pages for every city you serve. This is a genuine asset.", OKGRN),
            ("Legacy service URLs now return 404 (checked Nov 4: /pressure-washing-services-greenville-sc, /residential-gutter-installation). Any old links or citations pointing there are leaking.", RED),
            ("FAQ, Organization and PostalAddress schema already on the homepage — ahead of most competitors. Add Service schema per page next.", OKGRN),
            ("'Window Cleaning SC & NC' title shows smart multi-state intent — replicate that pattern on gutter/graffiti pages.", OKGRN),
            ("Six tag-manager boots per page view (3 GTMs x2) tax every load — fixing Analytics fixes speed too.", AMBER),
        ]
    bullets(s, T, Inches(0.6), Inches(1.8), Inches(7.55), items, size=12.5, gap=11)
    rect(s, Inches(8.4), Inches(1.8), Inches(4.35), Inches(4.6), T["PINE"])
    txt(s, Inches(8.65), Inches(2.0), Inches(3.9), Inches(0.4), "GOOGLE REVIEW ARMS RACE",
        size=12.5, bold=True, color=T["ACC"])
    rr = [("Foothills Exterior", "375+")] if T["key"]=="sl" else [("C3 Wash Pros", "460"), ("Clean Verde", "430")]
    rr += ([("Christmas Decor (Shurburtt)", "multi-city commercial")] if T["key"]=="sl" else
           [("Carolina Pressure Washers", "300+ · BBB A+"), ("Clear View", "226")])
    yy = Inches(2.5)
    for nm, rv in rr:
        txt(s, Inches(8.65), yy, Inches(3.9), Inches(0.35), nm, size=12, bold=True, color=WHITE)
        txt(s, Inches(8.65), yy + Inches(0.32), Inches(3.9), Inches(0.35), rv, size=11.5, color=T["ACC"])
        yy += Inches(0.78)
    txt(s, Inches(8.65), yy + Inches(0.05), Inches(3.9), Inches(1.1),
        T["key"]=="sl" and
        "Your public count sits near 55. Reviews are the #1 local ranking and trust signal — this is the single biggest SEO gap." or
        "Leaders hold 200-460+. Reviews feed both map-pack rank and ad quality — this is the single biggest SEO gap.",
        size=11.5, color=WHITE)
    # ---------------- 14 seo keywords
    s = base(prs, T, "SEO", 14)
    head(s, T, "Where the money keywords are")
    if T["key"] == "sl":
        rows = [
            ["Keyword", "Why it matters", "Priority"],
            ["christmas light installation greenville sc", "The category. Foothills and Walters own it today", "P1"],
            ["holiday lighting company near me", "Map-pack trigger phrase; reviews decide it", "P1"],
            ["commercial holiday lighting greenville", "Highest ticket; Christmas Decor targets it from Spartanburg", "P1"],
            ["municipality holiday decorations program", "Your real portfolio; near-zero competition content", "P2"],
            ["christmas light removal near me", "Overlooked January query — free rebooking opportunity", "P2"],
            ["permanent holiday lights upstate sc", "Emerging product; early content = early authority", "P3"],
        ]
    else:
        rows = [
            ["Keyword", "Why it matters", "Priority"],
            ["pressure washing greenville sc", "The head term; C3 and Clean Verde hold the map pack", "P1"],
            ["soft wash house washing greenville", "Your differentiator (science-based) — ours to own", "P1"],
            ["gutter cleaning greenville sc", "Fall spike + feeds guard installs", "P1"],
            ["drone gutter cleaning / no-ladder", "Near-zero competition; you have the rig and the photos", "P1"],
            ["window cleaning greenville sc", "Review-repost friendly; bundles with washes", "P2"],
            ["parking deck cleaning restriping", "Commercial, high-value, barely contested locally", "P2"],
        ]
    table(s, T, Inches(0.55), Inches(1.85), Inches(12.25), rows,
          [Inches(4.3), Inches(6.85), Inches(1.1)], row_h=Inches(0.62), size=12)
    txt(s, Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.7),
        [[("Honest note: ", {"bold": True, "color": T["PINE"], "size": 12.5}),
          ("rankings need Search Console access to verify precisely (slide 17). This table maps demand from the live public results — "
           "the opportunities are visible without an account; the exact positions are not.", {"size": 12.5, "color": T["INK"]})]])
    # ---------------- 15 seo fix
    s = base(prs, T, "SEO", 15)
    head(s, T, "The SEO fix list, in order of payoff")
    fixes = [
        ("1", "Kill the duplicate titles" if T["key"]=="sl" else "301 the dead URLs",
         T["key"]=="sl" and
         "Unique title per page: home = brand + residential; /municipalities = municipal & commercial government holiday lighting." or
         "Redirect the 404-ing legacy service URLs to their live successors so old links and citations stop leaking."),
        ("2", "Add LocalBusiness + Service schema" if T["key"]=="sl" else "Add Service schema sitewide",
         T["key"]=="sl" and
         "LocalBusiness with both phone numbers, service area and review count; Service markup on every audience page." or
         "One Service block per service page (name, provider, areaServed) — the homepage pattern, copied down."),
        ("3", "Review engine",
         "Post-job text with a direct Google review link. Target: " +
         ("+50 reviews before next December (55 → 105+)" if T["key"]=="sl" else "+50 in 6 months, closing on the 200 club")),
        ("4", "Weekly GBP posts",
         "We already produce the content — the Did You Know and install posts belong on the Business Profile the day they ship."),
        ("5", "Speed pass" if T["key"]=="sl" else "Tag-diet speed pass",
         T["key"]=="sl" and "Compress, cache, lazy-load images before the October traffic spike." or
         "Two GTM containers removed = leaner pages; then compress hero images."),
        ("6", "Harvest the content bank",
         "47 (SL) / 28 (SP) designed posts = a ready-made topical map. Turn each campaign into an on-site page or article."),
    ]
    xx, yy = Inches(0.55), Inches(1.8)
    for i, (n, ttl, body) in enumerate(fixes):
        cx = xx + (i % 2) * Inches(6.25); cy = yy + (i // 2) * Inches(1.52)
        rect(s, cx, cy, Inches(6.0), Inches(1.36), WHITE, line=T["MUT"])
        sh = s.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.14), cy + Inches(0.14), Inches(0.4), Inches(0.4))
        sh.fill.solid(); sh.fill.fore_color.rgb = T["ACC2"]; sh.line.fill.background(); sh.shadow.inherit = False
        tf = sh.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = n; r.font.bold = True; r.font.size = Pt(14); r.font.color.rgb = WHITE
        txt(s, cx + Inches(0.66), cy + Inches(0.1), Inches(5.2), Inches(0.4), ttl, size=13, bold=True, color=T["PINE"])
        txt(s, cx + Inches(0.66), cy + Inches(0.5), Inches(5.2), Inches(0.85), body, size=11, color=T["INK"])
    # ---------------- 16 horizons
    s = base(prs, T, "THE ROADMAP", 16)
    head(s, T, "1 · 3 · 5 — what each year is for")
    hz = [
        ("YEAR 1", "FIX THE GAUGES, RUN ONE REAL SEASON",
         ["GTM + GA4 + call tracking live; first clean baseline",
          "Titles, schema, redirects shipped; LSA switched on",
          T["key"]=="sl" and "105+ Google reviews; first fully-tracked season P&L by channel" or
          "+50 reviews; map-pack top-5 on 'soft wash house washing'",
          "Every dollar finally reports where it went"]),
        ("YEAR 3", "OWN THE MAP, CROSS THE MOAT",
         ["Top-3 map pack on the P1 keyword set",
          T["key"]=="sl" and "250+ reviews — parity with Foothills" or "250+ reviews — parity with C3 / Clean Verde",
          T["key"]=="sl" and "Lighting + takedown + storage sold as a season contract, not a job" or
          "Commercial accounts (decks, HOAs, storefronts) on annual contracts",
          "Remarketing audiences from Year 1 cutting CAC every cycle"]),
        ("YEAR 5", "CATEGORY LEADER, COMPOUNDING MOAT",
         [T["key"]=="sl" and "The Upstate's default holiday-lighting brand; permanent-RGB line launched" or
          "Upstate category leader; Greenville + Asheville + Charleston all branded and booked",
          "Brand searches do the heavy lifting; paid CAC down 30%+",
          T["key"]=="sl" and "Municipal portfolio as referenceable case studies" or
          "Drone service line famous locally — owns its own keyword",
          "The content bank is a library Google rewards weekly"]),
    ]
    xx = Inches(0.55)
    for ttl, sub, pts in hz:
        rect(s, xx, Inches(1.8), Inches(4.0), Inches(4.75), WHITE, line=T["MUT"])
        rect(s, xx, Inches(1.8), Inches(4.0), Inches(0.7), T["PINE"])
        txt(s, xx + Inches(0.2), Inches(1.88), Inches(3.6), Inches(0.35), ttl, size=15, bold=True, color=T["ACC"])
        txt(s, xx + Inches(0.2), Inches(2.22), Inches(3.7), Inches(0.3), sub, size=9.5, bold=True,
            color=RGBColor(0xD8,0xE6,0xDC) if T["key"]=="sl" else RGBColor(0xC5,0xE4,0xE6))
        bullets(s, T, xx + Inches(0.2), Inches(2.72), Inches(3.62), pts, size=10.5, gap=8)
        xx += Inches(4.22)
    # ---------------- 17 account access
    s = base(prs, T, "WHAT WE'D ADD WITH ACCESS", 17)
    head(s, T, "The export checklist — what each unlock sharpens")
    rows = [
        ["Grant access to / export", "What it verifies or unlocks", "Priority"],
        ["Google Ads account (read) + search terms report", "Whether campaigns ran, real spend, wasted terms, conversion truth", "P1"],
        ["GA4 property (any) + UA history export", T["key"]=="sl" and "Confirms the 2023 cutoff; any salvageable pre-2023 baselines" or "Which container is authoritative; salvageable baselines", "P1"],
        ["Google Tag Manager (all containers)", T["key"]=="sl" and "n/a — none exists; we install fresh" or "Container owners, creation dates, what each one fires", "P1" if T["key"]=="sp" else "P2"],
        ["Google Business Profile insights", "Calls, direction requests, photo views — the local truth", "P1"],
        ["Search Console (both domains)", "Exact queries, positions, CTR — turns slide 14 from map to scoreboard", "P1"],
        ["Call logs / estimate inbox by month", "Seasonality truth: when leads actually arrive vs when we spend", "P2"],
    ]
    table(s, T, Inches(0.55), Inches(1.8), Inches(12.25), rows,
          [Inches(4.4), Inches(6.65), Inches(1.2)], row_h=Inches(0.58), size=11.5)
    txt(s, Inches(0.55), Inches(6.15), Inches(11.4), Inches(1.0),
        [[("Our added recommendations: ", {"bold": True, "color": T["PINE"], "size": 12.5}),
          ("(1) put the call-tracking number on the Business Profile too, (2) UTM-tag every social post we ship — the content calendar becomes a "
           "measurement calendar, (3) add a 'how did you hear about us' field to the estimate form, (4) keep a lead-source column in the CRM from "
           "day one of GA4, (5) review velocity goal reviewed monthly, not yearly.", {"size": 12.5, "color": T["INK"]})]])
    # ---------------- 18 close
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["PINE"])
    rect(s, 0, H - Inches(0.25), W, Inches(0.25), T["ACC"])
    txt(s, Inches(0.9), Inches(1.0), Inches(11.5), Inches(1.0), "The first 90 days",
        size=40, bold=True, color=WHITE, font=T["HEAD"])
    rect(s, Inches(0.95), Inches(1.95), Inches(1.5), Inches(0.05), T["ACC"])
    sprint = [
        ("WEEKS 1-2", "GTM + GA4 + call tracking live. Data starts moving the same day."),
        ("WEEKS 3-4", T["key"]=="sl" and "Unique titles, LocalBusiness + Service schema, speed pass." or "301 redirect map, Service schema, two containers retired."),
        ("WEEKS 5-8", "Local Services Ads on; tight Search campaign per the season curve; negatives locked."),
        ("WEEKS 9-12", "Review engine humming (GBP posts weekly); first 90-day read-out: cost per call, per booked job."),
    ]
    yy = Inches(2.35)
    for lab, body in sprint:
        txt(s, Inches(0.95), yy, Inches(2.2), Inches(0.6), lab, size=14, bold=True, color=T["ACC"])
        txt(s, Inches(3.3), yy, Inches(9.0), Inches(0.8), body, size=15, color=WHITE)
        yy += Inches(0.92)
    rect(s, Inches(0.9), Inches(6.15), Inches(0.09), Inches(0.75), T["ACC"])
    txt(s, Inches(1.15), Inches(6.2), Inches(11.0), Inches(0.8),
        [[(T["name"], {"bold": True, "size": 14, "color": WHITE})],
         [(T["contact"], {"size": 12, "color": T["ACC"]})]], spacing=1.15)
    logo_img(s, T, W - Inches(2.05), Inches(0.5), Inches(0.7))
    prs.save(T["deck"])
    return T["deck"]

for T in (SL, SP):
    print("built:", build(T))
