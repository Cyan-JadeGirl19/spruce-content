"""Split audit decks (Nov 2026): one deck per company per discipline.
SL/SP x Google Ads / Google Analytics / SEO = 6 self-contained branded decks."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

ROOT = "/home/user/spruce"
W, H = Inches(13.333), Inches(7.5)
WHITE = RGBColor(0xFF,0xFF,0xFF)
RED   = RGBColor(0xC8,0x20,0x28)
AMBER = RGBColor(0xE8,0x96,0x14)
OKGRN = RGBColor(0x5A,0xA0,0x46)
DATE  = "November 4, 2026"

SL = dict(key="sl", name="Spruce Holiday Lighting & Events", domain="sprucelights.com",
    contact="sprucelights.com  ·  (864) 288-2459  ·  @spruceholidaylighting",
    logo=f"{ROOT}/assets/brand/sl_logo.png", logo_w=f"{ROOT}/assets/brand/sl_logo_white.png",
    HEAD="Georgia", BODY="Calibri",
    PINE=RGBColor(0x1E,0x46,0x20), PINE_D=RGBColor(0x12,0x2A,0x14),
    ACC=RGBColor(0xFF,0xC9,0x3C), ACC2=RGBColor(0xB8,0x86,0x0B),
    BG=RGBColor(0xFA,0xF7,0xF0), INK=RGBColor(0x17,0x24,0x1B),
    MUT=RGBColor(0x5E,0x6E,0x60), CARD=RGBColor(0xEF,0xF5,0xE8),
    SUB=RGBColor(0xCF,0xE2,0xD2))
SP = dict(key="sp", name="Spruce Pro · Exterior Cleaning", domain="sprucepro.com",
    contact="sprucepro.com  ·  (864) 483-4300  ·  @spruce_pro",
    logo=f"{ROOT}/assets/brand/sp_logo_color.png", logo_w=f"{ROOT}/assets/brand/sp_logo_white.png",
    HEAD="Arial", BODY="Calibri",
    PINE=RGBColor(0x00,0x30,0x3C), PINE_D=RGBColor(0x00,0x21,0x2A),
    ACC=RGBColor(0x1C,0xC8,0xD0), ACC2=RGBColor(0x90,0xD0,0x00),
    BG=RGBColor(0xFA,0xF7,0xF0), INK=RGBColor(0x0A,0x1A,0x20),
    MUT=RGBColor(0x5A,0x6E,0x72), CARD=RGBColor(0xE8,0xF4,0xF5),
    SUB=RGBColor(0xC5,0xE4,0xE6))

def rect(s, x, y, w, h, fill, line=None):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is not None:
        sh.line.color.rgb = line; sh.line.width = Pt(1)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh

def txt(s, x, y, w, h, runs, size=14, color=None, bold=False, font=None,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    if isinstance(runs, str): runs = [runs]
    first = True
    for item in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        if isinstance(item, str): item = [(item, {})]
        elif isinstance(item, tuple): item = [item]
        for text, o in item:
            p.alignment = o.get("align", align)
            p.line_spacing = o.get("spacing", spacing)
            p.space_after = Pt(o.get("after", 6)); p.space_before = Pt(o.get("before", 0))
            r = p.add_run(); r.text = text
            r.font.size = Pt(o.get("size", size)); r.font.bold = o.get("bold", bold)
            col = o.get("color", color)
            if col is not None: r.font.color.rgb = col
            r.font.name = o.get("font", font)
            if o.get("italic"): r.font.italic = True
    return tb

def chip(s, x, y, label, color, w=Inches(2.2), size=10):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, Inches(0.34))
    sh.adjustments[0] = 0.5
    sh.fill.solid(); sh.fill.fore_color.rgb = color; sh.line.fill.background()
    sh.shadow.inherit = False
    p = sh.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = "Calibri"
    return sh

def logo_img(s, T, x, y, h, white=False):
    p = T["logo_w"] if white else T["logo"]
    s.shapes.add_picture(p, x, y, height=h)

def bullets(s, T, x, y, w, items, size=13.5, gap=8, tcolor=None, marker_color=None):
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

def table(s, T, x, y, w, rows, col_w, row_h=Inches(0.42), size=11.5):
    tbl = s.shapes.add_table(len(rows), len(rows[0]), x, y, w, row_h * len(rows)).table
    for ci, cw in enumerate(col_w): tbl.columns[ci].width = cw
    for ri, row in enumerate(rows):
        for ci, val in enumerate(row):
            c = tbl.cell(ri, ci); c.text = ""
            p = c.text_frame.paragraphs[0]; r = p.add_run(); r.text = str(val)
            r.font.size = Pt(size); r.font.name = T["BODY"]
            c.fill.solid()
            if ri == 0:
                c.fill.fore_color.rgb = T["PINE"]; r.font.bold = True; r.font.color.rgb = WHITE
            else:
                c.fill.fore_color.rgb = T["CARD"] if ri % 2 else WHITE
                r.font.color.rgb = T["INK"]
            c.margin_left = Inches(0.08); c.margin_top = Inches(0.03); c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tbl

def base(prs, T, kicker, num, title):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["BG"])
    rect(s, 0, 0, Inches(0.18), H, T["PINE"])
    chip(s, Inches(0.55), Inches(0.32), kicker, T["PINE"])
    logo_img(s, T, W - Inches(1.9), Inches(0.28), Inches(0.62))
    txt(s, Inches(0.55), Inches(0.78), Inches(11.0), Inches(0.85), title,
        size=30, bold=True, color=T["PINE"], font=T["HEAD"])
    rect(s, Inches(0.58), Inches(1.5), Inches(1.5), Inches(0.05), T["ACC"])
    txt(s, W - Inches(5.1), Inches(6.98), Inches(4.0), Inches(0.4),
        f"Audited from public sources · {DATE}", size=9, color=T["MUT"], align=PP_ALIGN.RIGHT)
    txt(s, W - Inches(1.15), Inches(6.98), Inches(0.9), Inches(0.4),
        str(num), size=9, color=T["MUT"], align=PP_ALIGN.RIGHT)
    return s

def dark(prs, T):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["PINE"])
    rect(s, 0, H - Inches(0.22), W, Inches(0.22), T["ACC"])
    logo_img(s, T, W - Inches(2.05), Inches(0.5), Inches(0.7), white=True)
    return s

def cover(prs, T, disc):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, W, H, T["PINE"])
    rect(s, 0, H - Inches(0.25), W, Inches(0.25), T["ACC"])
    rect(s, Inches(0.9), Inches(1.62), Inches(0.09), Inches(2.5), T["ACC"])
    txt(s, Inches(1.25), Inches(1.7), Inches(10.5), Inches(0.5), T["name"].upper(),
        size=16, bold=True, color=T["ACC"])
    txt(s, Inches(1.22), Inches(2.2), Inches(11.2), Inches(1.6),
        [[(disc, {"size": 52, "bold": True, "color": WHITE, "font": T["HEAD"]})],
         [("Audit", {"size": 52, "bold": True, "color": T["ACC"], "font": T["HEAD"]})]], spacing=1.02)
    txt(s, Inches(1.25), Inches(4.15), Inches(10.0), Inches(0.5),
        "One of three standalone audits  ·  Google Ads  ·  Analytics  ·  SEO",
        size=15, color=T["SUB"])
    logo_img(s, T, Inches(9.4), Inches(0.75), Inches(1.05), white=True)
    txt(s, Inches(1.25), Inches(5.4), Inches(10.0), Inches(0.4),
        f"Prepared {DATE}  ·  verified from public sources", size=12.5, color=T["SUB"])
    txt(s, Inches(1.25), Inches(6.6), Inches(10.5), Inches(0.4), T["contact"],
        size=12, bold=True, color=T["ACC"])
    return s

def howto(prs, T, num):
    s = base(prs, T, "HOW TO READ THIS", num, "What this audit is — and isn't")
    txt(s, Inches(0.6), Inches(1.85), Inches(7.3), Inches(2.6),
        [[("Every finding was verified from public sources on " + DATE + ": your live website's "
           "actual code, its page inventory, and the search results your customers see.", {"size": 13.5})],
         [("This deck is the " + "portion of the November audit. The Analytics and SEO audits are "
           "separate decks — each stands alone.", {"size": 13.5})],
         [("Account-level numbers (spend, clicks, calls, conversions) live inside Google's tools. "
           "The access checklist near the end lists exactly what to grant or export to sharpen "
           "every number.", {"size": 13.5})]], color=T["INK"])
    lg = [("BROKEN", RED, "Losing data or customers today — fix first"),
          ("AT RISK", AMBER, "Working against you quietly — fix within 90 days"),
          ("HEALTHY", OKGRN, "Working — protect and build on it")]
    yy = Inches(1.95)
    for lab, c, d in lg:
        rect(s, Inches(8.35), yy, Inches(4.3), Inches(1.28), WHITE, line=T["MUT"])
        rect(s, Inches(8.35), yy, Inches(0.14), Inches(1.28), c)
        txt(s, Inches(8.62), yy + Inches(0.12), Inches(3.9), Inches(0.4), lab, size=14, bold=True, color=c)
        txt(s, Inches(8.62), yy + Inches(0.48), Inches(3.95), Inches(0.75), d, size=11, color=T["MUT"])
        yy += Inches(1.52)
    return s

def access(prs, T, num, rows, extra):
    s = base(prs, T, "ACCESS CHECKLIST", num, "What to grant or export — and what it unlocks")
    table(s, T, Inches(0.55), Inches(1.8), Inches(12.25), rows,
          [Inches(4.4), Inches(6.65), Inches(1.2)], row_h=Inches(0.62), size=11.5)
    txt(s, Inches(0.55), Inches(6.05), Inches(11.5), Inches(1.1),
        [[("Our added recommendations: ", {"bold": True, "color": T["PINE"], "size": 12.5}),
          (extra, {"size": 12.5, "color": T["INK"]})]])
    return s

def close(prs, T, sprint, closing):
    s = dark(prs, T)
    txt(s, Inches(0.9), Inches(1.0), Inches(11.5), Inches(1.0), "The first 90 days",
        size=40, bold=True, color=WHITE, font=T["HEAD"])
    rect(s, Inches(0.95), Inches(1.95), Inches(1.5), Inches(0.05), T["ACC"])
    yy = Inches(2.35)
    for lab, body in sprint:
        txt(s, Inches(0.95), yy, Inches(2.2), Inches(0.6), lab, size=14, bold=True, color=T["ACC"])
        txt(s, Inches(3.3), yy, Inches(9.0), Inches(0.8), body, size=15, color=WHITE)
        yy += Inches(0.92)
    rect(s, Inches(0.9), Inches(6.15), Inches(0.09), Inches(0.75), T["ACC"])
    txt(s, Inches(1.15), Inches(6.2), Inches(11.0), Inches(0.8),
        [[(T["name"], {"bold": True, "size": 14, "color": WHITE})],
         [(T["contact"], {"size": 12, "color": T["ACC"]})]], spacing=1.15)
    return s

def roadmap(prs, T, num, hz):
    s = base(prs, T, "THE ROADMAP", num, "1 · 3 · 5 — what each year is for")
    xx = Inches(0.55)
    for ttl, sub, pts in hz:
        rect(s, xx, Inches(1.8), Inches(4.0), Inches(4.75), WHITE, line=T["MUT"])
        rect(s, xx, Inches(1.8), Inches(4.0), Inches(0.7), T["PINE"])
        txt(s, xx + Inches(0.2), Inches(1.88), Inches(3.6), Inches(0.35), ttl, size=15, bold=True, color=T["ACC"])
        txt(s, xx + Inches(0.2), Inches(2.22), Inches(3.7), Inches(0.3), sub, size=9.5, bold=True, color=T["SUB"])
        bullets(s, T, xx + Inches(0.2), Inches(2.72), Inches(3.62), pts, size=10.5, gap=8)
        xx += Inches(4.22)
    return s

# ------------------------------------------------------------------ ADS
def build_ads(T):
    sl = T["key"] == "sl"
    f = f"/home/user/{'SL' if sl else 'SP'}_Google_Ads_Audit_Nov2026.pptx"
    prs = Presentation(); prs.slide_width, prs.slide_height = W, H
    cover(prs, T, "Google Ads")
    howto(prs, T, 2)
    # headline
    s = dark(prs, T)
    txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.7),
        [[("NO CONVERSION TAG.", {"size": 46, "bold": True, "color": T["ACC"], "font": T["HEAD"]})],
         [("If ads ran, nobody knows what they sold.", {"size": 36, "bold": True, "color": WHITE, "font": T["HEAD"]})]],
        spacing=1.05)
    bullets(s, T, Inches(0.95), Inches(3.3), Inches(11.4), [
        ("No AW- conversion tag, no tag manager, no call-tracking number anywhere on " + T["domain"] + " (checked " + DATE + ").", RED),
        ("Without a conversion tag Google optimizes for clicks, not jobs — the most expensive way to buy traffic.", RED),
        ("Demand reality: " + ("a 10-week lighting season on a 12-week decision window — budget must surge Sep-Dec."
            if sl else "year-round demand with a spring pollen peak and a fall leaf/gutter peak — December is the quiet month."), T["ACC"]),
        ("Fix cost: one afternoon of instrumentation. Fix value: every dollar finally reports what it earned.", WHITE),
    ], size=16, gap=12, marker_color=T["ACC"], tcolor=WHITE)
    # findings
    s = base(prs, T, "GOOGLE ADS", 4, "What we can prove from outside")
    items = [
        ("No AW- (Google Ads) tag, no GTM container, no call-tracking number on any page — checked " + DATE + ".", RED),
        ("Translation: if ads are running, Google has no idea which clicks become calls — optimization is impossible by definition.", RED),
        ("Only tracker found on site: " + ("UA-151910917-5, abandoned by Google on Jul 1, 2023." if sl else
            "three GTM containers, which could hide a conversion tag — verify inside each container."), RED if sl else AMBER),
        ("No verifiable live ads surfaced in public results this week — confirm inside the account.", AMBER),
        ("Market: " + ("Foothills (375+ reviews) and Walters dominate the brand-adjacent queries; LSAs with the Google Guarantee badge are the open flank."
            if sl else "C3 Wash Pros (460 reviews) and Clean Verde (430) hold the map pack; LSAs are the open flank."), T["ACC2"]),
    ]
    bullets(s, T, Inches(0.6), Inches(1.85), Inches(7.4), items, size=13, gap=12)
    rect(s, Inches(8.3), Inches(1.85), Inches(4.45), Inches(4.55), T["CARD"])
    txt(s, Inches(8.55), Inches(2.05), Inches(4.0), Inches(0.4), "WHY THIS MATTERS", size=13, bold=True, color=T["PINE"])
    txt(s, Inches(8.55), Inches(2.5), Inches(3.95), Inches(3.7),
        [[("Home services ads convert on the phone.", {"bold": True, "size": 13})],
         [("Without conversion tags and call tracking, you are paying Google for strangers, not jobs. "
           "Every competitor with a tagged campaign is learning weekly while you fly blind. "
           "The fix is not more budget — it is instrumentation first, spend second.", {"size": 12.5})],
         [("One tagged season is worth more than three untagged ones.", {"italic": True, "size": 12, "color": T["ACC2"]})]],
        color=T["INK"], spacing=1.1)
    # market 5-3-1
    s = base(prs, T, "GOOGLE ADS", 5, "The market, over 5 · 3 · 1 years")
    rows = [
        ["Window", "What changed in the market", "What it means for " + ("Spruce Lights" if sl else "Spruce Pro")],
        ["5 years", "Local Services Ads + the map pack became how homeowners choose home-service companies",
         "Lighting is a trust purchase: LSAs with the Google Guarantee badge fit a seasonal, high-ticket install" if sl
         else "LSAs fit wash quotes perfectly — pay per lead, badge builds instant trust"],
        ["3 years", "Category leaders stacked review engines (375-460 reviews) — review volume now feeds Ad Rank and map-pack rank",
         "Their review moat makes their ads cheaper and theirs ranks higher. The gap compounds yearly"],
        ["1 year", "AI Overviews compress generic 'near me' queries; brand + verified local signals decide who gets the click",
         "Generic keywords are a rising-cost trap. Win on brand, map pack, LSAs — not broad match"],
    ]
    table(s, T, Inches(0.55), Inches(1.85), Inches(12.25), rows,
          [Inches(1.15), Inches(5.6), Inches(5.5)], row_h=Inches(1.02), size=12)
    txt(s, Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.8),
        [[("Season budget curve: ", {"bold": True, "size": 12.5, "color": T["PINE"]}),
          ("Sep 10% · Oct 25% · Nov 35% · Dec 25% · Jan 5% (early-bird rebooking)" if sl else
           "Mar-May 40% · Jun-Aug 20% · Sep-Nov 30% (leaf + gutter) · Dec 10% (holiday prep)",
           {"size": 12.5})]])
    # fix
    s = base(prs, T, "GOOGLE ADS", 6, "The fix: instrument first, spend second")
    steps = [
        ("WEEK 1-2", "Install ONE Google Tag Manager. Fire the Google Ads conversion tag + call tracking (tracked number on site and Business Profile). Every click becomes data."),
        ("WEEK 3-4", "Turn on Local Services Ads: pay per lead, Google Guaranteed badge. Highest-intent dollars in home services."),
        ("WEEK 5-8", "One tight Search campaign: " + ("'christmas light installation greenville sc' + 'holiday lighting company' — exact and phrase only"
            if sl else "'pressure washing greenville sc', 'soft wash house washing', 'gutter cleaning greenville' — exact and phrase only")
            + ". Negatives: DIY, rental, equipment, salary."),
        ("WEEK 9-12", "First read-out: cost per call, call length, booked-job rate. Kill losers, feed winners. " +
            ("January: 'early bird 2027 booking' catches post-holiday resolve." if sl else
             "Add an ad group for drone gutter cleaning — near-zero competition.")),
    ]
    yy = Inches(1.85)
    for lab, body in steps:
        rect(s, Inches(0.55), yy, Inches(12.25), Inches(1.08), WHITE, line=T["MUT"])
        rect(s, Inches(0.55), yy, Inches(0.12), Inches(1.08), T["ACC2"])
        txt(s, Inches(0.85), yy + Inches(0.14), Inches(1.7), Inches(0.8), lab, size=13, bold=True, color=T["PINE"])
        txt(s, Inches(2.6), yy + Inches(0.10), Inches(10.0), Inches(0.92), body, size=12.5)
        yy += Inches(1.22)
    # roadmap
    roadmap(prs, T, 7, [
        ("YEAR 1", "INSTRUMENT AND RUN ONE REAL SEASON",
         ["Tags + call tracking live; first clean cost-per-lead data",
          "LSA switched on; one tight Search campaign per the season curve",
          "Every dollar reports where it went — no more faith-based spend",
          "Season audiences captured for next year's remarketing"]),
        ("YEAR 3", "CHEAPEST LEADS IN THE MARKET",
         ["Review moat crossed: ad costs fall as rating rises",
          "Remarketing lists cutting cost per booking every cycle",
          "Season contracts sold from tracked lead data",
          "Winning keywords owned; waste terms eliminated"]),
        ("YEAR 5", "CATEGORY LEADER ECONOMICS",
         ["Brand searches do the heavy lifting; paid CAC down 30%+",
          "LSA + Search + remarketing run as one learned system",
          "Budget set by tracked return, not gut feel",
          "New service lines launch into warmed audiences"]),
    ])
    # access
    access(prs, T, 8, [
        ["Grant access to / export", "What it verifies or unlocks", "Priority"],
        ["Google Ads account (read) + search terms report", "Whether campaigns ran, real spend, wasted terms, conversion truth", "P1"],
        ["Google Business Profile insights", "Calls and direction requests — the local baseline ads must beat", "P1"],
        ["Call logs / estimate inbox by month", "Seasonality truth: when leads actually arrive vs when we spend", "P2"],
        ["Any historic ad accounts or MCC links", "Legacy campaign history worth learning from", "P2"],
    ], "put the call-tracking number on the Business Profile too, and UTM-tag every social post so the content calendar becomes a measurement calendar.")
    close(prs, T, [
        ("WEEKS 1-2", "GTM + conversion tag + call tracking live. Data starts moving the same day."),
        ("WEEKS 3-4", "Local Services Ads on; negatives locked; tracked number on the Business Profile."),
        ("WEEKS 5-8", "Tight Search campaign per the season curve; first cost-per-call reads."),
        ("WEEKS 9-12", "First read-out: cost per call, per booked job. Kill losers, feed winners."),
    ], "")
    prs.save(f); return f

# ------------------------------------------------------------- ANALYTICS
def build_ga(T):
    sl = T["key"] == "sl"
    f = f"/home/user/{'SL' if sl else 'SP'}_Google_Analytics_Audit_Nov2026.pptx"
    prs = Presentation(); prs.slide_width, prs.slide_height = W, H
    cover(prs, T, "Google Analytics")
    howto(prs, T, 2)
    # headline
    s = dark(prs, T)
    if sl:
        txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.7),
            [[("JULY 1, 2023 —", {"size": 46, "bold": True, "color": T["ACC"], "font": T["HEAD"]})],
             [("the day your data stopped.", {"size": 46, "bold": True, "color": WHITE, "font": T["HEAD"]})]], spacing=1.05)
        bullets(s, T, Inches(0.95), Inches(3.3), Inches(11.4), [
            ("Your site carries Universal Analytics tag UA-151910917-5 — installed twice on every page (property created ~2020).", RED),
            ("Google stopped processing Universal Analytics on July 1, 2023. No GA4 was ever installed.", RED),
            ("Visitor counts, call volume, top pages, lead sources — the last 28 months simply do not exist.", WHITE),
            ("Fix cost: one afternoon. Fix value: every future decision stops being a guess.", T["ACC"]),
        ], size=16, gap=12, marker_color=T["ACC"], tcolor=WHITE)
    else:
        txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.7),
            [[("THREE TAG MANAGERS,", {"size": 46, "bold": True, "color": T["ACC2"], "font": T["HEAD"]})],
             [("one website, zero single source of truth.", {"size": 40, "bold": True, "color": WHITE, "font": T["HEAD"]})]], spacing=1.05)
        bullets(s, T, Inches(0.95), Inches(3.3), Inches(11.4), [
            ("Every page loads GTM-5X29VK9F, GTM-MS2LNTJB and GTM-MXCZRFMH — each injected twice.", T["ACC2"]),
            ("Three containers means at least three separate installs by three different hands across the years.", WHITE),
            ("Typical results: double-counted sessions, competing conversion tags, polluted remarketing audiences.", WHITE),
            ("Fix: crown one container, archive the rest. One focused afternoon.", T["ACC2"]),
        ], size=16, gap=12, marker_color=T["ACC2"], tcolor=WHITE)
    # timeline table
    s = base(prs, T, "GOOGLE ANALYTICS", 4, "What went wrong, and exactly when")
    rows = ([
        ["When", "What happened", "Evidence"],
        ["~2020", "UA-151910917-5 installed (property ID range dates to spring 2020)", "Tag live on every page today"],
        ["2020-2023", "Two identical UA tags fire per page — sessions double-counted, page-speed taxed", "2 hits of the ID in homepage source"],
        ["Jul 1, 2023", "Google kills UA processing. Recording stops mid-season — right before the rush", "Google sunset; no GA4 found on site"],
        ["Jul 2023 → today", "28 months of zero data: traffic, calls, sources, top pages — all unrecorded", "No GA4, no GTM, no alternative tag"],
    ] if sl else [
        ["When", "What happened", "Evidence"],
        ["Unknown split", "Three separate GTM containers installed by three different hands over the years", "3 GTM IDs in homepage source"],
        ["Today", "Each container loads twice per page — 6 tag-manager boots per view", "2 hits per ID in homepage source"],
        ["Ongoing", "Duplicate pageview + conversion risk: inflated sessions, broken audiences, contradictory attribution", "Standard failure mode of stacked containers"],
        ["Unknown owner", "Nobody on record knows which container is authoritative — needs 30 minutes in admin", "Container history lives in each GTM"],
    ])
    table(s, T, Inches(0.55), Inches(1.85), Inches(12.25), rows,
          [Inches(1.6), Inches(6.4), Inches(4.25)], row_h=Inches(0.78), size=11.5)
    cost = ("you cannot answer 'which pages win jobs?' or 'did October beat October last year?' — the two questions that plan a season."
            if sl else "no trustworthy baseline, so no campaign, page or service can be judged honestly.")
    txt(s, Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.8),
        [[("What it costs: ", {"bold": True, "size": 13, "color": T["PINE"]}), (cost, {"size": 13})]])
    # rebuild
    s = base(prs, T, "GOOGLE ANALYTICS", 5, "The rebuild: one afternoon, data flowing in 24 hours")
    arch = [
        ("1", "Crown ONE Google Tag Manager container",
         "Install GTM fresh (there is none today) on every page, once." if sl else
         "Keep the newest owned container; remove the other two sets of scripts site-wide."),
        ("2", "GA4 property inside GTM", "One tag, one property. Pages, scroll, clicks measured from minute one."),
        ("3", "Call tracking on the real number", "Dynamic number swap shows which source made the phone ring — the metric that pays for everything."),
        ("4", "Link Search Console + Google Ads", "Queries, rankings and ad conversions finally land in one report."),
        ("5", "Four events that matter", "call_click · quote_form_submit · service_page_engagement · " +
         ("gallery_to_contact" if sl else "before_after_engagement") + ". Ignore vanity metrics."),
        ("6", "Season audience lists", "Everyone who visits this season joins next season's remarketing list — the cheapest bookings you will ever buy."),
    ]
    xx, yy = Inches(0.55), Inches(1.85)
    for i, (n, ttl, body) in enumerate(arch):
        cx = xx + (i % 3) * Inches(4.22); cy = yy + (i // 3) * Inches(2.28)
        rect(s, cx, cy, Inches(4.0), Inches(2.08), WHITE, line=T["MUT"])
        sh = s.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.18), cy + Inches(0.16), Inches(0.42), Inches(0.42))
        sh.fill.solid(); sh.fill.fore_color.rgb = T["ACC"]; sh.line.fill.background(); sh.shadow.inherit = False
        p = sh.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = n; r.font.bold = True; r.font.size = Pt(15); r.font.color.rgb = T["PINE_D"]
        txt(s, cx + Inches(0.72), cy + Inches(0.14), Inches(3.15), Inches(0.55), ttl, size=12.5, bold=True, color=T["PINE"])
        txt(s, cx + Inches(0.2), cy + Inches(0.72), Inches(3.6), Inches(1.3), body, size=11)
    txt(s, Inches(0.55), Inches(6.45), Inches(12.2), Inches(0.6),
        [[("Timeline: ", {"bold": True, "size": 12.5, "color": T["PINE"]}),
          ("data in 24 hours · reliable trends in 90 days · year-over-year comparisons from Oct 2027.", {"size": 12.5})]])
    # measurement roadmap
    roadmap(prs, T, 6, [
        ("YEAR 1", "A BASELINE YOU CAN TRUST",
         ["GA4 + call tracking live; first clean season read",
          "Four events tracked; lead sources labeled in the CRM",
          "First true cost-per-lead by channel",
          "Year-over-year comparisons armed for next season"]),
        ("YEAR 3", "DECISIONS ON AUTOPILOT",
         ["YoY curves guide budget timing to the week",
          "Page and campaign verdicts take days, not guesses",
          "Audiences compound; remarketing cheapens bookings",
          "Reporting is a template, not a project"]),
        ("YEAR 5", "AN INSTITUTIONAL MEMORY",
         ["Five seasons of clean data guide every launch",
          "New service lines measured against known baselines",
          "Nothing depends on anyone's gut feel",
          "The data library is a competitive moat"]),
    ])
    access(prs, T, 7, ([
        ["Grant access to / export", "What it verifies or unlocks", "Priority"],
        ["Universal Analytics property UA-151910917-5 (read)", "Confirms the Jul 2023 cutoff; exports any salvageable pre-2023 baselines", "P1"],
        ["Google Tag Manager — all containers", "Fresh install; document owners and what each container fires", "P2"],
        ["Google Business Profile insights", "Calls and direction requests — the truth while analytics slept", "P1"],
        ["Call logs / estimate inbox by month", "Rebuilds the missing 28 months from the phones side", "P1"],
    ] if sl else [
        ["Grant access to / export", "What it verifies or unlocks", "Priority"],
        ["Google Tag Manager — all three containers", "Container owners, creation dates, what each one fires; crown the survivor", "P1"],
        ["Any GA4 property that may already exist", "Avoid creating a duplicate property; adopt, don't stack", "P1"],
        ["Google Business Profile insights", "Calls and direction requests — baseline until GA4 is trustworthy", "P1"],
        ["Call logs / estimate inbox by month", "Ground-truth seasonality to validate the new GA4 against", "P2"],
    ]), "add a 'how did you hear about us' field to the estimate form, and keep a lead-source column in the CRM from day one of GA4.")
    close(prs, T, [
        ("WEEKS 1-2", "GTM + GA4 + call tracking live. Data starts moving the same day."),
        ("WEEKS 3-4", "Four lead events tracked; Search Console and Ads linked in."),
        ("WEEKS 5-8", "Lead-source labeling in the estimate flow; first monthly read."),
        ("WEEKS 9-12", "Reliable trends on the board; audiences building for next season."),
    ], "")
    prs.save(f); return f

# ------------------------------------------------------------------ SEO
def build_seo(T):
    sl = T["key"] == "sl"
    f = f"/home/user/{'SL' if sl else 'SP'}_SEO_Audit_Nov2026.pptx"
    prs = Presentation(); prs.slide_width, prs.slide_height = W, H
    cover(prs, T, "SEO & Local Search")
    howto(prs, T, 2)
    # headline
    s = dark(prs, T)
    txt(s, Inches(0.9), Inches(1.15), Inches(11.5), Inches(1.7),
        [[("THE REVIEW GAP.", {"size": 46, "bold": True, "color": T["ACC"], "font": T["HEAD"]})],
         [("The single biggest thing between you and the map pack.", {"size": 34, "bold": True, "color": WHITE, "font": T["HEAD"]})]],
        spacing=1.05)
    bullets(s, T, Inches(0.95), Inches(3.3), Inches(11.4), [
        ("Competitors hold " + ("375+ Google reviews (Foothills Exterior). Your public count sits near 55." if sl
            else "200-460+ Google reviews (C3: 460, Clean Verde: 430, Carolina PW: 300+)."), RED),
        ("Reviews are the #1 local ranking and trust signal — this gap compounds every month it stays open.", RED),
        ("On-site: " + ("46 thin pages, duplicated titles, no LocalBusiness schema." if sl
            else "strong 187-page base, but legacy service URLs now return 404 — old links are leaking."), AMBER),
        ("The engine is fixable: a post-job review link + weekly Business Profile posts, both fed by content we already make.", T["ACC"]),
    ], size=16, gap=12, marker_color=T["ACC"], tcolor=WHITE)
    # findings
    s = base(prs, T, "SEO", 4, "The site, checked page by page")
    items = ([
        ("46 total URLs across the whole site — thin for a company with 47+ designed posts and 24 real installs to show.", AMBER),
        ("Title duplication: the homepage and /municipalities both compete for 'Christmas Lighting Installers' — Google picks one, you lose the other.", RED),
        ("Schema is Yoast defaults only (WebSite / WebPage). No LocalBusiness, no Service, no FAQ — the markup that wins map-pack adjacency is missing.", RED),
        ("Homepage HTML alone is ~340KB — heavy WordPress payload; compress and cache before peak season.", AMBER),
        ("Strengths worth keeping: clean robots + sitemap, one H1 per page, the WordPress + Yoast stack is the right foundation.", OKGRN),
    ] if sl else [
        ("187 URLs — real depth, including service pages for every city you serve. This is a genuine asset.", OKGRN),
        ("Legacy service URLs now return 404 (checked " + DATE + ": two key service paths). Any old links or citations pointing there are leaking.", RED),
        ("FAQ, Organization and PostalAddress schema already on the homepage — ahead of most competitors. Add Service schema per page next.", OKGRN),
        ("Multi-state titles (e.g. window cleaning SC & NC) show smart intent targeting — replicate that pattern on gutter/graffiti pages.", OKGRN),
        ("Six tag-manager boots per page view (3 GTMs x2) tax every load — fixing Analytics fixes speed too.", AMBER),
    ])
    bullets(s, T, Inches(0.6), Inches(1.8), Inches(7.55), items, size=12.5, gap=11)
    rect(s, Inches(8.4), Inches(1.8), Inches(4.35), Inches(4.6), T["PINE"])
    txt(s, Inches(8.65), Inches(2.0), Inches(3.9), Inches(0.4), "GOOGLE REVIEW ARMS RACE",
        size=12.5, bold=True, color=T["ACC"])
    rr = (["Foothills Exterior — 375+", "Walters Exterior — 5.0 rated", "Christmas Decor — multi-city commercial"] if sl else
          ["C3 Wash Pros — 460", "Clean Verde — 430", "Carolina PW — 300+ · BBB A+", "Clear View — 226"])
    yy = Inches(2.5)
    for nm in rr:
        txt(s, Inches(8.65), yy, Inches(3.9), Inches(0.35), nm, size=12, bold=True, color=WHITE)
        yy += Inches(0.52)
    txt(s, Inches(8.65), yy + Inches(0.1), Inches(3.9), Inches(1.2),
        "Reviews feed both map-pack rank and ad quality. Closing this gap is the highest-leverage SEO move of the next 12 months.",
        size=11.5, color=WHITE)
    # keywords
    s = base(prs, T, "SEO", 5, "Where the money keywords are")
    rows = ([
        ["Keyword", "Why it matters", "Priority"],
        ["christmas light installation greenville sc", "The category. Foothills and Walters own it today", "P1"],
        ["holiday lighting company near me", "Map-pack trigger phrase; reviews decide it", "P1"],
        ["commercial holiday lighting greenville", "Highest ticket; multi-city competitors target it", "P1"],
        ["municipality holiday decorations program", "Your real portfolio; near-zero competition content", "P2"],
        ["christmas light removal near me", "Overlooked January query — free rebooking opportunity", "P2"],
        ["permanent holiday lights upstate sc", "Emerging product; early content = early authority", "P3"],
    ] if sl else [
        ["Keyword", "Why it matters", "Priority"],
        ["pressure washing greenville sc", "The head term; C3 and Clean Verde hold the map pack", "P1"],
        ["soft wash house washing greenville", "Your differentiator (science-based) — ours to own", "P1"],
        ["gutter cleaning greenville sc", "Fall spike + feeds guard installs", "P1"],
        ["drone gutter cleaning / no-ladder", "Near-zero competition; you have the rig and the photos", "P1"],
        ["window cleaning greenville sc", "Review-repost friendly; bundles with washes", "P2"],
        ["parking deck cleaning restriping", "Commercial, high-value, barely contested locally", "P2"],
    ])
    table(s, T, Inches(0.55), Inches(1.85), Inches(12.25), rows,
          [Inches(4.3), Inches(6.85), Inches(1.1)], row_h=Inches(0.62), size=12)
    txt(s, Inches(0.55), Inches(6.35), Inches(12.2), Inches(0.7),
        [[("Honest note: ", {"bold": True, "color": T["PINE"], "size": 12.5}),
          ("exact positions need Search Console access (checklist, slide 8). This maps demand from the live public results — "
           "the opportunities are visible without an account.", {"size": 12.5})]])
    # fixes
    s = base(prs, T, "SEO", 6, "The fix list, in order of payoff")
    fixes = ([
        ("1", "Kill the duplicate titles", "Unique title per page: home = brand + residential; municipalities = municipal & commercial government holiday lighting."),
        ("2", "Add LocalBusiness + Service schema", "LocalBusiness with phone, service area and review count; Service markup on every audience page."),
        ("3", "Review engine", "Post-job text with a direct Google review link. Target: +50 reviews before next December (55 to 105+)."),
        ("4", "Weekly Business Profile posts", "The install and Did You Know posts belong on the Profile the day they ship."),
        ("5", "Speed pass", "Compress, cache, lazy-load images before the October traffic spike."),
        ("6", "Harvest the content bank", "47 designed posts = a ready-made topical map. Turn each campaign into an on-site page or article."),
    ] if sl else [
        ("1", "301 the dead URLs", "Redirect the 404-ing legacy service paths to their live successors so old links and citations stop leaking."),
        ("2", "Add Service schema sitewide", "One Service block per service page (name, provider, areaServed) — the homepage pattern, copied down."),
        ("3", "Review engine", "Post-job text with a direct Google review link. Target: +50 in 6 months, closing on the 200 club."),
        ("4", "Weekly Business Profile posts", "The Did You Know and before/after posts belong on the Profile the day they ship."),
        ("5", "Tag-diet speed pass", "Two GTM containers removed = leaner pages; then compress hero images."),
        ("6", "Harvest the content bank", "28 designed posts = a ready-made topical map. Turn each campaign into an on-site page or article."),
    ])
    xx, yy = Inches(0.55), Inches(1.8)
    for i, (n, ttl, body) in enumerate(fixes):
        cx = xx + (i % 2) * Inches(6.25); cy = yy + (i // 2) * Inches(1.52)
        rect(s, cx, cy, Inches(6.0), Inches(1.36), WHITE, line=T["MUT"])
        sh = s.shapes.add_shape(MSO_SHAPE.OVAL, cx + Inches(0.14), cy + Inches(0.14), Inches(0.4), Inches(0.4))
        sh.fill.solid(); sh.fill.fore_color.rgb = T["ACC2"]; sh.line.fill.background(); sh.shadow.inherit = False
        p = sh.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = n; r.font.bold = True; r.font.size = Pt(14); r.font.color.rgb = WHITE
        txt(s, cx + Inches(0.66), cy + Inches(0.1), Inches(5.2), Inches(0.4), ttl, size=13, bold=True, color=T["PINE"])
        txt(s, cx + Inches(0.66), cy + Inches(0.5), Inches(5.2), Inches(0.85), body, size=11)
    roadmap(prs, T, 7, ([
        ("YEAR 1", "CLEAN HOUSE, START THE ENGINE",
         ["Unique titles, schema, speed pass shipped",
          "105+ Google reviews; review link in every job-close text",
          "Weekly Profile posts from the content bank",
          "Top-5 map pack on the P1 keyword set"]),
        ("YEAR 3", "OWN THE MAP",
         ["Top-3 map pack across the money keywords",
          "250+ reviews — parity with the leaders",
          "Season contracts marketed from the content library",
          "Every service page earning, none competing"]),
        ("YEAR 5", "CATEGORY LEADER, COMPOUNDING MOAT",
         ["The default local brand for the category",
          "Brand searches do the heavy lifting",
          "Municipal/commercial portfolio as case-study pages",
          "The content library is a moat Google rewards weekly"]),
    ] if sl else [
        ("YEAR 1", "PLUG THE LEAKS, START THE ENGINE",
         ["301 map live; Service schema sitewide",
          "+50 reviews; two GTM containers retired (speed wins)",
          "Weekly Profile posts from the content bank",
          "Top-5 map pack on 'soft wash house washing'"]),
        ("YEAR 3", "OWN THE MAP",
         ["Top-3 map pack across the money keywords",
          "250+ reviews — parity with C3 / Clean Verde",
          "Commercial accounts (decks, HOAs) on annual contracts",
          "Drone line owns its own keyword"]),
        ("YEAR 5", "CATEGORY LEADER, COMPOUNDING MOAT",
         ["Upstate leader; Greenville, Asheville, Charleston branded",
          "Brand searches do the heavy lifting; CAC down 30%+",
          "Commercial portfolio as case-study pages",
          "The content library is a moat Google rewards weekly"]),
    ]))
    access(prs, T, 8, [
        ["Grant access to / export", "What it verifies or unlocks", "Priority"],
        ["Search Console (" + T["domain"] + ")", "Exact queries, positions, CTR — turns the keyword map into a scoreboard", "P1"],
        ["Google Business Profile insights", "Calls, direction requests, photo views — the local truth", "P1"],
        ["Review count + velocity export", "Monthly review-velocity goal vs the leaders", "P2"],
        ["Call logs / estimate inbox by month", "Seasonality truth for content timing", "P2"],
    ], "review velocity is a monthly goal, not a yearly wish — put the review link into the job-close text message today.")
    close(prs, T, ([
        ("WEEKS 1-2", "Unique titles + LocalBusiness/Service schema live."),
        ("WEEKS 3-4", "Review link into the job-close text; first 10 review asks out."),
        ("WEEKS 5-8", "Weekly Profile posts from the content bank; speed pass done."),
        ("WEEKS 9-12", "Content bank pages shipping weekly; first map-pack movement reads."),
    ] if sl else [
        ("WEEKS 1-2", "301 redirect map live; Service schema rolling out."),
        ("WEEKS 3-4", "Review link into the job-close text; first 10 review asks out."),
        ("WEEKS 5-8", "Weekly Profile posts; two GTM containers retired (speed win)."),
        ("WEEKS 9-12", "Content bank pages shipping weekly; first map-pack movement reads."),
    ]), "")
    prs.save(f); return f

made = []
for T in (SL, SP):
    made += [build_ads(T), build_ga(T), build_seo(T)]
for m in made: print("built:", m)
