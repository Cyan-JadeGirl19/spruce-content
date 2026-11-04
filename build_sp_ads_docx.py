"""SP LSAs + Google Business Profile ad sets (Nov 2026) — branded docx, one ad
per page, logo header, with programmatic character-limit verification."""
import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEAL = RGBColor(0x00,0x30,0x3C); CYAN = RGBColor(0x0E,0x9A,0xA0)
LIME = RGBColor(0x76,0xA8,0x00); GRAY = RGBColor(0x66,0x66,0x66)
BODY = RGBColor(0x2E,0x38,0x3A); WHITE = RGBColor(0xFF,0xFF,0xFF)
LOGO = '/home/user/spruce/assets/brand/sp_logo_color.png'
CONTACT = "Spruce Pro  ·  (864) 483-4300  ·  sprucepro.com  ·  @spruce_pro"

# ------------------------------------------------------------------ COPY
LSA = [
 dict(theme="FALL RESET", window="Run Nov 3 - Nov 30",
  desc=("Local, licensed and insured crew washing houses, driveways and gutters across Greenville "
        "since 2006. Free quotes, fast scheduling, and a team that answers the phone. Book the fall "
        "reset before the first freeze."),
  services=["House washing (soft wash)", "Driveway & concrete cleaning", "Gutter cleaning (full flush)"],
  queries="house washing near me · pressure washing greenville sc · driveway cleaning",
  note="Your baseline LSA. Broad exterior-cleaning intent, priced to carry the season."),
 dict(theme="GUTTER SEASON", window="Run Nov 3 - Dec 15 (leaf fall)",
  desc=("Gutter cleaning done right: troughs cleared, downspouts flushed, debris hauled away. "
        "Gutter guards installed too, with a clog free guarantee. Licensed and insured, serving "
        "Greenville since 2006."),
  services=["Gutter cleaning (clean + flush)", "Downspout check", "Gutter guard install"],
  queries="gutter cleaning near me · gutter cleaning greenville · gutter guards cost",
  note="Highest winter-urgency lead type. Clogs become claims in December."),
 dict(theme="GUEST-READY HOLIDAYS", window="Run Nov 17 - Dec 20",
  desc=("Get guest ready before the holidays: house washing, window cleaning, driveways and "
        "gutters. One crew handles the whole exterior. Locally owned since 2006, free quotes "
        "within 24 hours."),
  services=["House wash + windows bundle", "Window cleaning (sills & tracks)", "Concrete & entry walkways"],
  queries="window cleaning near me · holiday cleaning services · pressure washing before holidays",
  note="Premium-angle variant for the hosting crowd; pairs with SP_11 social post."),
 dict(theme="NO-LADDER / TWO STORY+", window="Run year-round, weight to spring",
  desc=("Pressure washing and window cleaning for homes up to five stories: by ladder, by pole, "
        "or by drone where it is safer. No ladders leaning on your home. Licensed and insured, "
        "Greenville's own crew since 2006."),
  services=["Multi-story house washing", "Drone gutter & roofline cleaning", "High window cleaning"],
  queries="drone pressure washing · 3 story house washing · roof cleaning no ladders",
  note="Differentiator nobody local can match; video-inspection offer is the lead hook."),
]

GMB = [
 dict(theme="NOVEMBER SLOTS OPEN", post_btn="Call now",
  post=("Fall slots are filling fast. House washing, gutters and windows, done by one crew with "
        "one invoice, before the holidays take over. Free quotes within 24 hours, licensed and "
        "insured, serving the Upstate since 2006. Call or message and we will hold your slot."),
  heads=["Greenville Exterior Cleaning", "Free Quotes, Fast Scheduling", "Licensed & Insured Crews"],
  descs=["House washing, gutters and windows in Greenville. Free quotes within 24 hours.",
         "Licensed and insured since 2006. Fall slots open now. Call or book online today."],
  utm="utm_source=google&utm_medium=cpc&utm_campaign=sp_gmb_nov26&utm_content=slots"),
 dict(theme="GUTTER CLEANING SPECIAL", post_btn="Get quote",
  post=("The leaves are down and the gutters are full. We clear the trough, flush every downspout "
        "until it runs clean, and haul the debris away. Ask about gutter guards while we are up "
        "there and retire the ladder for good. Free quotes, clog free guarantee."),
  heads=["Gutters Cleaned & Flushed", "Never Scoop Again", "Book Before The Storms"],
  descs=["Gutter cleaning with a full downspout flush. Debris hauled away. Free quote.",
         "Guards installed with a clog free guarantee. Licensed and insured, since 2006."],
  utm="utm_source=google&utm_medium=cpc&utm_campaign=sp_gmb_nov26&utm_content=gutters"),
 dict(theme="GUEST-READY OUTSIDE", post_btn="Book",
  post=("The guests are coming and the outside of the house gets one chance at a first "
        "impression. House wash, windows, entry walkways: one visit, whole exterior. We schedule "
        "around your cooking, not the other way around. Message us for a free quote."),
  heads=["Get Guest-Ready Outside", "One Visit, Whole Exterior", "Windows, Wash & Walkways"],
  descs=["Guest ready outside before the guests arrive. One visit, whole exterior.",
         "House wash, windows and entry walkways before the holidays. Free quote."],
  utm="utm_source=google&utm_medium=cpc&utm_campaign=sp_gmb_nov26&utm_content=guestready"),
 dict(theme="TOP-RATED LOCAL CREW", post_btn="Learn more",
  post=("Maria watched our crew work through a full window job and wrote about it: a thorough, "
        "excellent job, start to finish. That is the standard on every home we visit, big or "
        "small. Read the reviews, check the photos, then give us a call. Free quotes, always."),
  heads=["A Crew Neighbors Recommend", "Streak-Free Window Cleaning", "Trusted Since 2006"],
  descs=["Real reviews from real Greenville neighbors. Free quotes within 24 hours.",
         "Windows, washing and gutters by the crew your neighbors keep rebooking."],
  utm="utm_source=google&utm_medium=cpc&utm_campaign=sp_gmb_nov26&utm_content=reviews"),
]

# ------------------------------------------------------------------ VERIFY
print("== character limit checks ==")
ok = True
for i, l in enumerate(LSA, 1):
    n = len(l['desc'])
    flag = "OK" if n <= 300 else "TOO LONG"
    if n > 300: ok = False
    print(f"LSA{i} desc: {n}/300 {flag}")
for i, g in enumerate(GMB, 1):
    for h in g['heads']:
        if len(h) > 30: ok = False; print(f"GMB{i} HEADLINE TOO LONG: '{h}' {len(h)}/30")
    for d in g['descs']:
        if len(d) > 90: ok = False; print(f"GMB{i} DESC TOO LONG: '{d}' {len(d)}/90")
print("ALL LIMITS OK" if ok else "FIX NEEDED")

# ------------------------------------------------------------------ DOC
def setgrid(tbl, widths):
    g = tbl._tbl.find(qn('w:tblGrid'))
    for c, w in zip(g.findall(qn('w:gridCol')), widths): c.set(qn('w:w'), str(int(w*1440)))
def bg(cell, fill):
    el = OxmlElement('w:shd'); el.set(qn('w:val'),'clear'); el.set(qn('w:fill'),fill)
    cell._tc.get_or_add_tcPr().append(el)
def noline(tbl):
    b = OxmlElement('w:tblBorders')
    for edge in ('top','left','bottom','right','insideH','insideV'):
        e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'),'none'); b.append(e)
    tbl._tbl.tblPr.append(b)

doc = Document()
st = doc.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(11); st.font.color.rgb=BODY
def sec_margins(sec):
    sec.left_margin = sec.right_margin = Inches(0.85)
    sec.top_margin = Inches(0.55); sec.bottom_margin = Inches(0.65)
def brand_header(sec):
    sec.header.is_linked_to_previous = False
    hdr = sec.header
    for p in list(hdr.paragraphs): p._element.getparent().remove(p._element)
    t = hdr.add_table(rows=1, cols=2, width=Inches(6.8)); t.autofit=False
    setgrid(t, (4.6, 2.2)); noline(t)
    left, right = t.rows[0].cells; left.text=""; right.text=""
    p = left.paragraphs[0]
    r = p.add_run("SPRUCE PRO"); r.bold=True; r.font.size=Pt(13); r.font.color.rgb=TEAL
    p2 = left.add_paragraph()
    r2 = p2.add_run("EXTERIOR CLEANING  ·  GOOGLE AD COPY"); r2.bold=True; r2.font.size=Pt(7.5); r2.font.color.rgb=CYAN
    p2.paragraph_format.space_after = Pt(0)
    rp = right.paragraphs[0]; rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rp.add_run().add_picture(LOGO, height=Inches(0.52))
    rule = hdr.add_paragraph(); pPr = rule._p.get_or_add_pPr(); pBdr = OxmlElement('w:pBdr')
    bt = OxmlElement('w:bottom'); bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'12')
    bt.set(qn('w:color'),'1CC8D0'); pBdr.append(bt); pPr.append(pBdr)
    rule.paragraph_format.space_after = Pt(0)
def brand_footer(sec):
    sec.footer.is_linked_to_previous = False
    f = sec.footer
    for p in list(f.paragraphs): p._element.getparent().remove(p._element)
    p = f.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(CONTACT); r.font.size=Pt(8.5); r.bold=True; r.font.color.rgb=CYAN
def para(t="", size=11, bold=False, color=BODY, after=6, before=0, align=None, spacing=None):
    p = doc.add_paragraph(); r = p.add_run(t)
    r.font.size=Pt(size); r.bold=bold; r.font.color.rgb=color
    p.paragraph_format.space_after=Pt(after); p.paragraph_format.space_before=Pt(before)
    if align is not None: p.alignment = align
    if spacing: p.paragraph_format.line_spacing = spacing
    return p
def panel(title, text, fill, tcolor, mono=False):
    t = doc.add_table(rows=1, cols=1); setgrid(t, (6.8,))
    c = t.cell(0,0); bg(c, fill); c.text=""
    p = c.paragraphs[0]
    r = p.add_run(title + "   "); r.bold=True; r.font.size=Pt(8.5); r.font.color.rgb=tcolor
    r2 = p.add_run(text); r2.font.size=Pt(9.5); r2.font.color.rgb=BODY
    p.paragraph_format.line_spacing = 1.12
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return t

from docx.enum.section import WD_SECTION_START
# ---- cover
s0 = doc.sections[0]; sec_margins(s0)
bar = doc.add_table(rows=1, cols=1); setgrid(bar, (6.8,))
c = bar.cell(0,0); bg(c, "00303C"); c.text=""
r = c.paragraphs[0].add_run("SPRUCE PRO  ·  EXTERIOR CLEANING"); r.bold=True
r.font.size=Pt(11); r.font.color.rgb=RGBColor(0x1C,0xC8,0xD0)
doc.add_paragraph().paragraph_format.space_after = Pt(2)
lt = doc.add_table(rows=1, cols=2); setgrid(lt, (5.0, 1.8)); noline(lt)
lc, rc = lt.rows[0].cells; lc.text=""; rc.text=""
p = lc.paragraphs[0]; r = p.add_run("Google Ads"); r.bold=True; r.font.size=Pt(34); r.font.color.rgb=TEAL
p2 = lc.add_paragraph(); r2 = p2.add_run("Ready to Run"); r2.bold=True; r2.font.size=Pt(34); r2.font.color.rgb=CYAN
p2.paragraph_format.space_after = Pt(2)
rp = rc.paragraphs[0]; rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
rp.add_run().add_picture(LOGO, height=Inches(0.95))
para("4 Local Services Ads  ·  4 Business Profile Ads  ·  November 2026", 12.5, True, LIME, before=6, after=12)
para("How the two formats differ", 14, True, TEAL, after=4)
para("Local Services Ads sit above everything with the Google Guaranteed badge, and you pay per "
     "lead, not per click. Google builds the ad from the inputs on the next four pages: the "
     "business description, services and seasonal focus. Speed wins there, answer a new lead "
     "within five minutes or it usually goes cold.", 10.5, after=6)
para("Business Profile ads are the copy and campaigns attached to your Google listing. The Post "
     "text is free to publish on the profile the same day. The headlines and descriptions drop "
     "straight into a Smart campaign when you want to pay for reach. Every campaign carries the "
     "UTM tag printed on its page so the analytics fix can attribute what it earns.", 10.5, after=8)
tb = doc.add_table(rows=1, cols=1); setgrid(tb, (6.8,))
tc = tb.cell(0,0); bg(tc, "00303C"); tc.text=""
tp = tc.paragraphs[0]; tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = tp.add_run(CONTACT); tr.bold=True; tr.font.size=Pt(9.5); tr.font.color.rgb=RGBColor(0x1C,0xC8,0xD0)

# ---- LSA pages
for i, l in enumerate(LSA):
    sec = doc.add_section(WD_SECTION_START.NEW_PAGE); sec_margins(sec)
    brand_header(sec); brand_footer(sec)
    kt = doc.add_table(rows=1, cols=1); setgrid(kt, (6.8,))
    kc = kt.cell(0,0); bg(kc, "00303C"); kc.text=""
    kr = kc.paragraphs[0].add_run(f"LOCAL SERVICES AD {i+1} OF 4   ·   {l['theme']}")
    kr.bold=True; kr.font.size=Pt(9.5); kr.font.color.rgb=RGBColor(0x90,0xD0,0x00)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    panel("RUN WINDOW", l['window'] + "  ·  pays per lead  ·  Google Guaranteed badge", "E8F4F5", CYAN)
    para("Business description (paste into LSA)", 12.5, True, TEAL, after=3)
    para('"' + l['desc'] + '"', 11.5, after=6, spacing=1.15)
    panel("CHARACTER CHECK", f"{len(l['desc'])}/300 characters — fits the LSA description field", "F1F7E4", LIME)
    para("Services to attach", 12.5, True, TEAL, after=3)
    for sv in l['services']:
        p = doc.add_paragraph()
        r1 = p.add_run("•  "); r1.bold=True; r1.font.size=Pt(11); r1.font.color.rgb=LIME
        r2 = p.add_run(sv); r2.font.size=Pt(10.5)
        p.paragraph_format.space_after=Pt(2); p.paragraph_format.left_indent=Inches(0.18)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    para("Starting prices: LSA lets you show a from-price per service. Suggested market anchors: "
         "gutter cleaning from $149, house wash from $199, window cleaning from $129. Confirm "
         "your own numbers before enabling.", 9.5, False, GRAY, after=6)
    panel("TARGET SEARCHES", l['queries'], "E8F4F5", CYAN)
    panel("WHY THIS VARIANT", l['note'], "F1F7E4", LIME)

# ---- GMB pages
for i, g in enumerate(GMB):
    sec = doc.add_section(WD_SECTION_START.NEW_PAGE); sec_margins(sec)
    brand_header(sec); brand_footer(sec)
    kt = doc.add_table(rows=1, cols=1); setgrid(kt, (6.8,))
    kc = kt.cell(0,0); bg(kc, "00303C"); kc.text=""
    kr = kc.paragraphs[0].add_run(f"BUSINESS PROFILE AD {i+1} OF 4   ·   {g['theme']}")
    kr.bold=True; kr.font.size=Pt(9.5); kr.font.color.rgb=RGBColor(0x1C,0xC8,0xD0)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    para("Google Post (publish free on the profile today)", 12.5, True, TEAL, after=3)
    para('"' + g['post'] + '"', 11, after=6, spacing=1.15)
    panel("CTA BUTTON", g['post_btn'], "E8F4F5", CYAN)
    para("Smart campaign headlines (max 30 characters)", 12.5, True, TEAL, after=3)
    for h in g['heads']:
        p = doc.add_paragraph()
        r1 = p.add_run("•  "); r1.bold=True; r1.font.size=Pt(11); r1.font.color.rgb=LIME
        r2 = p.add_run(f"{h}   ({len(h)}/30)"); r2.font.size=Pt(10.5); r2.font.color.rgb=GRAY
        p.paragraph_format.space_after=Pt(2); p.paragraph_format.left_indent=Inches(0.18)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    para("Descriptions (max 90 characters)", 12.5, True, TEAL, after=3)
    for dscr in g['descs']:
        p = doc.add_paragraph()
        r1 = p.add_run("•  "); r1.bold=True; r1.font.size=Pt(11); r1.font.color.rgb=LIME
        r2 = p.add_run(f"{dscr}   ({len(dscr)}/90)"); r2.font.size=Pt(10.5); r2.font.color.rgb=GRAY
        p.paragraph_format.space_after=Pt(2); p.paragraph_format.left_indent=Inches(0.18)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    panel("TRACKING TAG", "Attach to every final URL:  " + g['utm'], "F1F7E4", LIME)

doc.save('/home/user/SP_Google_Ads_LSAGMB_Nov2026.docx')
print('saved ads doc')
