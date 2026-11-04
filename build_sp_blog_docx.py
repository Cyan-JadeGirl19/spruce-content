"""SP_Blog_Posts_Nov2026.docx — branded layout: cover page, then one page per
post with logo header, teal/cyan/lime brand styling and publish-notes box."""
import re, sys
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEAL = RGBColor(0x00,0x30,0x3C); CYAN = RGBColor(0x0E,0x9A,0xA0)
LIME = RGBColor(0x76,0xA8,0x00); GRAY = RGBColor(0x66,0x66,0x66)
BODY = RGBColor(0x2E,0x38,0x3A); WHITE = RGBColor(0xFF,0xFF,0xFF)
LOGO = '/home/user/spruce/assets/brand/sp_logo_color.png'
CONTACT = "Spruce Pro  ·  (864) 483-4300  ·  sprucepro.com  ·  @spruce_pro"

raw = open('/home/user/spruce/sp_blog_posts_nov2026.txt').read()
parts = re.split(r'(?m)^POST \d+\s*$', raw)[1:]
posts = []
for b in parts:
    posts.append(dict(
        title = re.search(r'TITLE: (.+)', b).group(1).strip(),
        slug  = re.search(r'SLUG: (.+)', b).group(1).strip(),
        meta  = re.search(r'META: (.+)', b).group(1).strip(),
        body  = b.split('BODY:\n')[1].strip()))
CATS = ["GUTTER CLEANING", "GUTTER GUARDS", "WINDOW CARE", "ROOF CARE"]
LINKS = [
 ("PUBLISH NOTES", "Week of Nov 10, before the wet season. Link to the Gutter Cleaning service page and the SP_21 Did You Know post (500 gallon fact)."),
 ("PUBLISH NOTES", "Week of Nov 17. Link to the Gutter Guards service page and the SP_26 Did You Know post (surface tension)."),
 ("PUBLISH NOTES", "Week of Nov 24, or hold for the first sprinkler season in March. Link to the Window Cleaning page and the SP_23 Did You Know post (sprinkler etching)."),
 ("PUBLISH NOTES", "Any time; evergreen topic. Link to the Roof Cleaning / SoftWash page and the SP_22 Did You Know post (algae)."),
]

doc = Document()
st = doc.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(11); st.font.color.rgb=BODY

def sec_margins(sec):
    sec.left_margin = sec.right_margin = Inches(0.85)
    sec.top_margin = Inches(0.55); sec.bottom_margin = Inches(0.65)

def setgrid(tbl, widths):
    g = tbl._tbl.find(qn('w:tblGrid'))
    for c, w in zip(g.findall(qn('w:gridCol')), widths): c.set(qn('w:w'), str(int(w*1440)))

def bg(cell, fill):
    el = OxmlElement('w:shd'); el.set(qn('w:val'),'clear'); el.set(qn('w:fill'),fill)
    cell._tc.get_or_add_tcPr().append(el)

def noline(tbl):
    tblPr = tbl._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top','left','bottom','right','insideH','insideV'):
        e = OxmlElement(f'w:{edge}'); e.set(qn('w:val'),'none'); borders.append(e)
    tblPr.append(borders)

def para(t="", size=11, bold=False, color=BODY, after=6, before=0, align=None,
         container=None, spacing=None):
    host = container if container is not None else doc
    p = host.add_paragraph(); r = p.add_run(t)
    r.font.size=Pt(size); r.bold=bold; r.font.color.rgb=color
    p.paragraph_format.space_after=Pt(after); p.paragraph_format.space_before=Pt(before)
    if align is not None: p.alignment = align
    if spacing: p.paragraph_format.line_spacing = spacing
    return p

def brand_header(sec):
    sec.header.is_linked_to_previous = False
    hdr = sec.header
    for p in list(hdr.paragraphs): p._element.getparent().remove(p._element)
    t = hdr.add_table(rows=1, cols=2, width=Inches(6.8))
    t.autofit = False; setgrid(t, (4.6, 2.2)); noline(t)
    left, right = t.rows[0].cells
    left.text = ""
    p = left.paragraphs[0]
    r = p.add_run("SPRUCE PRO"); r.bold=True; r.font.size=Pt(13); r.font.color.rgb=TEAL
    p2 = left.add_paragraph()
    r2 = p2.add_run("EXTERIOR CLEANING  ·  BLOG CONTENT"); r2.bold=True; r2.font.size=Pt(7.5); r2.font.color.rgb=CYAN
    p2.paragraph_format.space_after = Pt(0)
    right.text = ""
    rp = right.paragraphs[0]; rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rp.add_run().add_picture(LOGO, height=Inches(0.52))
    # thin cyan rule under the header
    rule = hdr.add_paragraph()
    pPr = rule._p.get_or_add_pPr(); pBdr = OxmlElement('w:pBdr')
    bt = OxmlElement('w:bottom'); bt.set(qn('w:val'),'single'); bt.set(qn('w:sz'),'12')
    bt.set(qn('w:color'),'1CC8D0'); pBdr.append(bt); pPr.append(pBdr)
    rule.paragraph_format.space_after = Pt(0)

def brand_footer(sec):
    sec.footer.is_linked_to_previous = False
    f = sec.footer
    for p in list(f.paragraphs): p._element.getparent().remove(p._element)
    p = f.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(CONTACT); r.font.size=Pt(8.5); r.bold=True; r.font.color.rgb=CYAN

# ============================================================ COVER (sec 0)
sec0 = doc.sections[0]; sec_margins(sec0)
bar = doc.add_table(rows=1, cols=1); setgrid(bar, (6.8,))
c = bar.cell(0,0); bg(c, "00303C"); c.text=""
r = c.paragraphs[0].add_run("SPRUCE PRO  ·  EXTERIOR CLEANING"); r.bold=True
r.font.size=Pt(11); r.font.color.rgb=RGBColor(0x1C,0xC8,0xD0)
doc.add_paragraph().paragraph_format.space_after = Pt(2)
lt = doc.add_table(rows=1, cols=2); setgrid(lt, (5.0, 1.8)); noline(lt)
lcell, rcell = lt.rows[0].cells
lcell.text=""
p = lcell.paragraphs[0]
r = p.add_run("Four New"); r.bold=True; r.font.size=Pt(34); r.font.color.rgb=TEAL
p2 = lcell.add_paragraph()
r2 = p2.add_run("Blog Posts"); r2.bold=True; r2.font.size=Pt(34); r2.font.color.rgb=CYAN
p2.paragraph_format.space_after = Pt(2)
rcell.text=""
rp = rcell.paragraphs[0]; rp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
rp.add_run().add_picture(LOGO, height=Inches(0.95))
para("Gutters · Gutter Guards · Hard Water Spots · Roof Algae", 12.5, True, LIME, before=6, after=10)
para("NOVEMBER 2026  ·  READY TO PUBLISH", 9.5, True, GRAY, after=12)

para("Why these four", 14, True, TEAL, after=4)
para("The blog already covers drones, house washing and windows well. These four posts fill the "
     "gaps customers actually search for and nobody on the site answers: what clogged gutters cost "
     "you, how gutter guards really work, what those cloudy window spots are, and what the black "
     "roof streaks actually are. Each one backs a service we sell and a Did You Know social post "
     "already in the calendar.", 10.5, after=10)

summary = doc.add_table(rows=5, cols=3); summary.autofit=False
setgrid(summary, (0.55, 3.6, 2.65))
hdrs = ("#","Post","Publish")
for i,h in enumerate(hdrs):
    cc = summary.cell(0,i); cc.text=""
    rr = cc.paragraphs[0].add_run(h); rr.bold=True; rr.font.size=Pt(9.5); rr.font.color.rgb=TEAL
    bg(cc, "E8F4F5")
for i,(post, cat) in enumerate(zip(posts, CATS)):
    vals = (str(i+1), post['title'], LINKS[i][1].split('.')[0])
    for j,v in enumerate(vals):
        cc = summary.cell(i+1,j); cc.text=""
        rr = cc.paragraphs[0].add_run(v)
        rr.font.size=Pt(9.5); rr.font.color.rgb=TEAL if j==0 else BODY
        rr.bold = (j==0)
        if i % 2 == 0: bg(cc, "F7FBFB")

doc.add_paragraph().paragraph_format.space_after=Pt(4)
para("Voice check", 14, True, TEAL, before=8, after=4)
para("Plain, local, specific. Short sentences. No keyword stuffing, no filler phrases, no dashes. "
     "Every post scanned and verified before delivery. Words per post: 391 to 425.", 10.5, after=8)

fb = doc.add_table(rows=1, cols=1); setgrid(fb, (6.8,))
fc = fb.cell(0,0); bg(fc, "00303C"); fc.text=""
fp = fc.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = fp.add_run(CONTACT); fr.bold=True; fr.font.size=Pt(9.5); fr.font.color.rgb=RGBColor(0x1C,0xC8,0xD0)

# ============================================================ POST PAGES
for i, post in enumerate(posts):
    sec = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec_margins(sec)
    brand_header(sec); brand_footer(sec)
    # kicker bar
    kt = doc.add_table(rows=1, cols=1); setgrid(kt, (6.8,))
    kc = kt.cell(0,0); bg(kc, "00303C"); kc.text=""
    kr = kc.paragraphs[0].add_run(f"BLOG POST {i+1} OF 4   ·   {CATS[i]}")
    kr.bold=True; kr.font.size=Pt(9.5); kr.font.color.rgb=RGBColor(0x90,0xD0,0x00)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    para(post['title'], 20, True, TEAL, after=6)
    # url/meta block
    mt = doc.add_table(rows=2, cols=1); setgrid(mt, (6.8,))
    m0 = mt.cell(0,0); m0.text=""
    rr = m0.paragraphs[0].add_run("URL:   sprucepro.com/" + post['slug'] + "/")
    rr.font.size=Pt(9); rr.bold=True; rr.font.color.rgb=CYAN
    m1 = mt.cell(1,0); m1.text=""
    rr = m1.paragraphs[0].add_run("META:   " + post['meta'])
    rr.font.size=Pt(9); rr.font.color.rgb=GRAY
    bg(m0, "E8F4F5"); bg(m1, "E8F4F5")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    # body with bullet detection
    chunks = [c.strip() for c in post['body'].split('\n\n') if c.strip()]
    pending = False
    for chunk in chunks:
        if pending and len(chunk) < 110:
            p = doc.add_paragraph()
            r1 = p.add_run("•  "); r1.bold=True; r1.font.size=Pt(11); r1.font.color.rgb=LIME
            r2 = p.add_run(chunk)
            r2.font.size=Pt(10.5); r2.font.color.rgb=BODY
            p.paragraph_format.space_after=Pt(3); p.paragraph_format.line_spacing=1.1
            p.paragraph_format.left_indent=Inches(0.18)
            continue
        pending = chunk.endswith(':')
        p = doc.add_paragraph(); r = p.add_run(chunk)
        r.font.size=Pt(10.5); r.font.color.rgb=BODY
        p.paragraph_format.space_after=Pt(6); p.paragraph_format.line_spacing=1.12
    # publish notes box
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    nt = doc.add_table(rows=1, cols=1); setgrid(nt, (6.8,))
    nc = nt.cell(0,0); bg(nc, "F1F7E4"); nc.text=""
    nr = nc.paragraphs[0].add_run(LINKS[i][0] + "   ")
    nr.bold=True; nr.font.size=Pt(8.5); nr.font.color.rgb=LIME
    nr2 = nc.paragraphs[0].add_run(LINKS[i][1])
    nr2.font.size=Pt(8.5); nr2.font.color.rgb=BODY

doc.save('/home/user/SP_Blog_Posts_Nov2026.docx')
print('saved branded blog doc')
