#!/usr/bin/env python3
"""Authentic Install Series: standalone Word doc for SL_31-54 (real customer photos)."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PINE  = RGBColor(0x1E, 0x46, 0x20)
LIME  = RGBColor(0x7A, 0xB0, 0x2E)
GOLD  = RGBColor(0xB8, 0x86, 0x0B)
GRAY  = RGBColor(0x66, 0x66, 0x66)
BODY  = RGBColor(0x33, 0x33, 0x33)
LIGHT = "EFF5E8"
CREAM = "FAF7F0"
GOLDBG= "FBF3DF"
TH = "/tmp/thumbs"

doc = Document()
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(11); st.font.color.rgb = BODY
for sec in doc.sections:
    sec.left_margin = sec.right_margin = Inches(0.7)
    sec.top_margin = Inches(0.7); sec.bottom_margin = Inches(0.7)

def para(text="", size=11, bold=False, color=BODY, align=None, after=6, before=0):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.font.color.rgb = color
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    return p

def h2(text, before=14):
    p = doc.add_paragraph()
    r = p.add_run(text); r.bold = True; r.font.size = Pt(15); r.font.color.rgb = PINE
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(6)
    return p

def set_grid(tbl, inches):
    grid = tbl._tbl.find(qn('w:tblGrid'))
    for c, w in zip(grid.findall(qn('w:gridCol')), inches):
        c.set(qn('w:w'), str(int(w*1440)))

def cell_bg(cell, hexfill):
    el = OxmlElement('w:shd'); el.set(qn('w:val'), 'clear'); el.set(qn('w:fill'), hexfill)
    cell._tc.get_or_add_tcPr().append(el)

def bar(color_hex="B8860B"):
    t = doc.add_table(rows=1, cols=1)
    c = t.cell(0,0); cell_bg(c, color_hex)
    c.paragraphs[0].add_run("").font.size = Pt(1)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ---------------------------------------------------------------- cover
bar()
para("SPRUCE HOLIDAY LIGHTING & EVENTS", 12, True, LIME, after=2)
p = doc.add_paragraph()
r = p.add_run("Authentic Install Series"); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = PINE
p.paragraph_format.space_after = Pt(4)
para("Twenty-four real customer installs, photographed by our own crews", 13, False, GOLD, after=10)
para("A separate mini campaign to run alongside the main content pack", 10.5, False, BODY, after=10)

h2("Why this series exists", before=0)
para("Every image in this pack is a real Spruce install, shot on site by our crews with nothing staged and "
     "nothing rendered. Posts like these are the trust builders. They answer the one question every "
     "homeowner quietly asks, which is simply, do they actually do work like this?")
para("Two things to know before posting. First, the captions and hashtags deliberately skip every city, "
     "street and neighborhood name to protect each homeowner's privacy. Please keep it that way when you "
     "repost. Second, each post is labeled Residential or Commercial so you can pitch both audiences from "
     "the same series.")
para("December dates get the most eyes, so the calendar starts there and rolls into January, where the "
     "message quietly becomes, the lights came down but next season is already booking.")

# ---------------------------------------------------------------- captions
doc.add_page_break()
h2("Captions and hashtags", before=0)
para("Same drill as the main pack. Caption goes in the post, hashtags go in the first comment, story version "
     "reposts the same day. No locations anywhere, in keeping with the privacy rule.", 10, False, GRAY, after=10)

posts = [
("SL_31","Residential","The JOY house",
"This is a real install we finished this season, shot just as we pulled out of the driveway. Warm white on every roofline, lit trees framing the walk, and a JOY sign that sums up the whole thing. No filters, no staging, this is what booking Spruce actually gets you.",
"#SpruceLights #RealInstall #AuthenticChristmas #ChristmasLightInstallation #HolidayLighting #WarmWhiteLights #YardGoals #ChristmasIsComing #RealHomes #LightUpTheHolidays"),
("SL_32","Residential","Snowman and the lit waterfall",
"Somewhere out there is a yard where a glowing snowman stands guard over a waterfall wrapped in blue and gold. That yard is a real customer of ours and this is our own photo from install night. Some jobs you just have to stop and photograph before you leave.",
"#SpruceLights #RealInstall #AuthenticChristmas #HolidayLighting #ChristmasLightInstallation #WaterfallLights #SnowmanSeason #RealHomes #YardGoals #ChristmasMagic"),
("SL_41","Commercial","Blue canopy over the whole block",
"An entire stretch of trees under a waterfall of blue. Displays at this scale are a different sport entirely, weeks of planning, buckets of strand, and a crew that knows what it's doing fifty feet up a pine. Property managers and municipalities, this one's for you.",
"#SpruceLights #CommercialLighting #RealInstall #AuthenticChristmas #MunicipalLighting #HolidayLighting #LargeScaleLighting #BlueChristmas #PropertyManagers #BookEarly"),
("SL_33","Residential","Tiered landscape, porch to creek",
"From the porch down the steps, along the creek and up to the arched walkway, every level of this yard got the treatment. Big installs look complicated but they come down to one thing, a plan. Ours are drawn before a single strand goes up.",
"#SpruceLights #RealInstall #AuthenticChristmas #LandscapeLighting #HolidayLighting #ChristmasLightInstallation #RealHomes #DesignFirst #YardGoals #SeasonProof"),
("SL_42","Commercial","A ceiling of glowing globes",
"Look up. A canopy of glowing globes hung through the trees over the whole property, with the buildings dressed to match. Event style commercial lighting is one of our favorite things to build, and this one stopped traffic for the entire season.",
"#SpruceLights #CommercialLighting #RealInstall #AuthenticChristmas #EventLighting #HolidayLighting #GlobeLights #VenueLighting #CommercialProperty #NextSeason"),
("SL_35","Residential","Three trees and the reindeer family",
"Three blue-lit trees, a family of glowing reindeer and a warm gold border to tie it all together. One of our favorite installs this season, photographed exactly as we left it. Yours could be the yard people slow down for next year.",
"#SpruceLights #RealInstall #AuthenticChristmas #ChristmasLightInstallation #ReindeerLights #HolidayLighting #TreeWraps #RealHomes #YardEnvy #BookNextSeason"),
("SL_36","Residential","Every gable traced in warm white",
"Every gable, every peak, every edge. Stone, shake and brick each catch the light differently, and tracing this roofline was half the fun of the job. Real home, real install, first night live.",
"#SpruceLights #RealInstall #AuthenticChristmas #ChristmasLightInstallation #RooflineLighting #HolidayLighting #WarmWhiteLights #RealHomes #CurbAppeal #Craftsmanship"),
("SL_37","Residential","The deep porch with garland rails",
"A porch this deep deserves garland on every rail and bulbs on every rafter. This one wraps clear around the house, and the owners tell us they've started taking their coffee out there just to sit under it. Even in January.",
"#SpruceLights #RealInstall #AuthenticChristmas #PorchGoals #GarlandAndLights #HolidayLighting #ChristmasLightInstallation #RealHomes #FarmhouseStyle #CozySeason"),
("SL_38","Residential","Warm white on brick, wreaths lit",
"Warm white on brick with lit wreaths on the windows is the look that never goes out of style. Simple from the street, meticulous up close. That's the standard on every install we hang.",
"#SpruceLights #RealInstall #AuthenticChristmas #Wreaths #WarmWhiteLights #HolidayLighting #ChristmasLightInstallation #RealHomes #ClassicChristmas #DetailsMatter"),
("SL_39","Residential","Blue hour on the farmhouse roof",
"There's a ten minute window right after sunset when the sky goes deep blue and every photo sings. We plan install days around catching it, because your lights deserve the same start as the big reveals.",
"#SpruceLights #RealInstall #AuthenticChristmas #BlueHour #FarmhouseChristmas #HolidayLighting #ChristmasLightInstallation #RooflineLighting #RealHomes #GoldenHour"),
("SL_40","Residential","Gables plus a trunk wrap",
"Roofline traced, so we kept going. Tree trunks wrapped to the ground, every gable edged, and the whole front brought together in warm white. The details are what make a display feel finished instead of decorated.",
"#SpruceLights #RealInstall #AuthenticChristmas #TreeWraps #RooflineLighting #HolidayLighting #ChristmasLightInstallation #RealHomes #YardGoals #FinishedLook"),
("SL_34","Residential","The creek that glows blue",
"A quiet backyard creek became a ribbon of blue. This is the kind of detail most companies skip and the kind neighbors remember. Real yard, real install, straight off our crew lead's phone.",
"#SpruceLights #RealInstall #AuthenticChristmas #LandscapeLighting #BlueLights #HolidayLighting #ChristmasLightInstallation #BackyardGoals #RealHomes #DetailsMatter"),
("SL_43","Residential","Classic red and green, done right",
"Classic red and green with soft green uplighting on the oaks. Some houses want modern, some want nostalgia, and both are welcome here. Whatever your style, the install standard stays the same.",
"#SpruceLights #RealInstall #AuthenticChristmas #ClassicChristmas #RedAndGreen #HolidayLighting #ChristmasLightInstallation #Uplighting #RealHomes #Tradition"),
("SL_44","Residential","A Storybook Christmas",
"Storybook cottages were made for this. Two lit dormers, a wreath on the door, and warm white tracing every edge of the roof. This one is a real install from this season, photographed the night we finished and left the lights to do the talking.",
"#SpruceLights #RealInstall #AuthenticChristmas #StorybookChristmas #CottageChristmas #ChristmasLightInstallation #HolidayLighting #DormerLights #RealHomes #CurbAppeal"),
("SL_45","Residential","Snowflakes That Never Melt",
"Full disclosure, we climbed into a very large oak to hang these. A dozen glowing snowflakes now float between the branches like the forecast finally cooperated. Real tree, real install, and yes, they come down just as carefully as they went up.",
"#SpruceLights #RealInstall #AuthenticChristmas #SnowflakeLights #TreeLighting #HolidayLighting #ChristmasLightInstallation #YardGoals #RealHomes #WinterWonderland"),
("SL_46","Residential","Every Arch, Every Column",
"Three dormer windows, three fresh wreaths with red bows, and a roofline traced in warm white over the whole thing. Add the lit tree by the drive and the house reads festive from every direction. Our photo from install night, untouched except for a little polish.",
"#SpruceLights #RealInstall #AuthenticChristmas #DormerGoals #Wreaths #RooflineLighting #HolidayLighting #ChristmasLightInstallation #RealHomes #ClassicChristmas"),
("SL_47","Residential","The Whole Estate, Aglow",
"When the driveway is this long, you know the install was a conversation. Rooflines, columned entry, hedges and mature trees all glowing in the same warm white. Large homes are a specialty, and this real install is the proof.",
"#SpruceLights #RealInstall #AuthenticChristmas #EstateLighting #LuxuryChristmas #HolidayLighting #ChristmasLightInstallation #GrandEntrance #RealHomes #BookNextSeason"),
("SL_48","Residential","Wrapped in Warm White",
"The house got the full trace and the giant oak out front got wrapped to the sky. Warm white from curb to canopy, this whole corner glows now. Real install, real customers, photographed the night we flipped the switch.",
"#SpruceLights #RealInstall #AuthenticChristmas #TreeWrap #WarmWhiteLights #HolidayLighting #ChristmasLightInstallation #RooflineLighting #RealHomes #YardGoals"),
("SL_49","Residential","Bright Gables, Warm Welcome",
"Bright gables up top, a lit wreath at the door, and warm white carrying clean across the whole roofline. White brick and holiday lights are a match made in December. Our photo, our install, first night live.",
"#SpruceLights #RealInstall #AuthenticChristmas #WhiteBrick #GableLights #HolidayLighting #ChristmasLightInstallation #WarmWhiteLights #RealHomes #WelcomeHome"),
("SL_50","Residential","The Modern Farmhouse Glow",
"Black windows, clean lines, and a warm white roofline that softens all of it. Modern farmhouses were practically designed for this look. Caught at blue hour right as the lights came on, which is exactly how we photograph every install we can.",
"#SpruceLights #RealInstall #AuthenticChristmas #ModernFarmhouse #BlueHour #HolidayLighting #ChristmasLightInstallation #RooflineLighting #RealHomes #FarmhouseChristmas"),
("SL_51","Residential","Every Angle Aglow",
"Garages count too. Every pitch and peak of this one got traced, so the whole front of the property glows instead of just the front door. Details like that are the difference between decorated and finished.",
"#SpruceLights #RealInstall #AuthenticChristmas #GarageGoals #EveryAngle #HolidayLighting #ChristmasLightInstallation #RooflineLighting #RealHomes #FinishedLook"),
("SL_52","Residential","The Porch Run, Garland and All",
"A porch run this long deserves backup, so the gables got traced and the rails got garland with warm white woven through. Blue hour, first light on, coffee going cold because nobody wanted to go inside. That is a real install night.",
"#SpruceLights #RealInstall #AuthenticChristmas #PorchGoals #GarlandAndLights #BlueHour #HolidayLighting #ChristmasLightInstallation #RealHomes #FarmhouseStyle"),
("SL_53","Residential","Even the Chimney Dresses Up",
"Tall chimney, every gable traced, hedges glowing below. Some homes ask for a little, this one asked for the full trace and wore it well. Our crews photograph installs like this one the night they go live, straight from the ladder.",
"#SpruceLights #RealInstall #AuthenticChristmas #ChimneyGoals #RooflineLighting #HolidayLighting #ChristmasLightInstallation #WarmWhiteLights #RealHomes #Craftsmanship"),
("SL_54","Residential","Dormers, Twinkling",
"Two lit dormers, a wreath by the walk, and warm white tracing every shingle line. Storybook houses like this one are why we love the small installs as much as the big ones. Real home, real install, straight off our crew lead's phone.",
"#SpruceLights #RealInstall #AuthenticChristmas #CottageChristmas #DormerLights #HolidayLighting #ChristmasLightInstallation #StorybookStyle #RealHomes #CozySeason"),
]

for pid, typ, name, cap, tags in posts:
    t = doc.add_table(rows=1, cols=2); t.autofit=False
    set_grid(t, (2.35, 4.75))
    left, right = t.rows[0].cells
    left.width=Inches(2.35); right.width=Inches(4.75)
    left.paragraphs[0].add_run().add_picture(f"{TH}/{pid}.jpg", width=Inches(2.2))
    right.text=""
    hp = right.paragraphs[0]
    hr = hp.add_run(f"{pid}  ·  {name}   "); hr.bold=True; hr.font.size=Pt(11); hr.font.color.rgb=PINE
    tr = hp.add_run(typ.upper()); tr.bold=True; tr.font.size=Pt(9); tr.font.color.rgb=GOLD if typ=="Commercial" else LIME
    hp.paragraph_format.space_after=Pt(3)
    cp = right.add_paragraph(); cr=cp.add_run(cap); cr.font.size=Pt(10.5)
    cp.paragraph_format.space_after=Pt(3)
    tp = right.add_paragraph(); trr=tp.add_run(tags); trr.font.size=Pt(9); trr.font.color.rgb=GRAY
    tp.paragraph_format.space_after=Pt(2)
    cell_bg(right, CREAM)
    doc.add_paragraph().paragraph_format.space_after=Pt(0)

# ---------------------------------------------------------------- calendar
doc.add_page_break()
h2("The calendar", before=0)
para("Two posts a week, Mondays and Wednesdays or Fridays. The commercial installs are mixed in on high "
     "traffic dates to catch business owners scrolling over the holidays.", 10, False, GRAY, after=8)

sched = [
 ("SL_31","Mon Dec 14","Residential","The JOY house, full roofline"),
 ("SL_32","Wed Dec 16","Residential","Snowman and the lit waterfall"),
 ("SL_41","Fri Dec 18","Commercial","Blue canopy over the whole block"),
 ("SL_33","Mon Dec 21","Residential","Tiered landscape, porch to creek"),
 ("SL_42","Tue Dec 22","Commercial","A ceiling of glowing globes"),
 ("SL_35","Wed Dec 23","Residential","Three trees and the reindeer family"),
 ("SL_36","Mon Dec 28","Residential","Every gable traced in warm white"),
 ("SL_37","Wed Dec 30","Residential","The deep porch with garland rails"),
 ("SL_38","Mon Jan 4","Residential","Warm white on brick, wreaths lit"),
 ("SL_39","Wed Jan 6","Residential","Blue hour on the farmhouse roof"),
 ("SL_40","Fri Jan 8","Residential","Gables plus a trunk wrap"),
 ("SL_34","Mon Jan 11","Residential","The creek that glows blue"),
 ("SL_43","Wed Jan 13","Residential","Classic red and green, done right"),
 ("SL_44","Mon Jan 18","Residential","Storybook cottage, dormers lit"),
 ("SL_45","Wed Jan 20","Residential","Hanging snowflakes in the big oak"),
 ("SL_46","Fri Jan 22","Residential","Dormer wreaths, full roofline trace"),
 ("SL_47","Mon Jan 25","Residential","The estate from the long drive"),
 ("SL_48","Wed Jan 27","Residential","House trace plus the giant oak wrap"),
 ("SL_49","Fri Jan 29","Residential","White brick, bright gables"),
 ("SL_50","Mon Feb 1","Residential","Blue hour on the modern farmhouse"),
 ("SL_51","Wed Feb 3","Residential","Every pitch traced, garage included"),
 ("SL_52","Fri Feb 5","Residential","Porch run with garland rails"),
 ("SL_53","Mon Feb 8","Residential","Tall chimney, full gable trace"),
 ("SL_54","Wed Feb 10","Residential","Cottage dormers, wreath at the door"),
]
tbl = doc.add_table(rows=1, cols=4); tbl.autofit = False
set_grid(tbl, (2.35, 1.0, 0.95, 2.8))
hdr = tbl.rows[0].cells
for i,t in enumerate(("Preview","Date","Type","Post and angle")):
    hdr[i].text=""
    r = hdr[i].paragraphs[0].add_run(t); r.bold=True; r.font.size=Pt(10); r.font.color.rgb=PINE
    cell_bg(hdr[i], LIGHT)
    hdr[i].width = Inches((2.35,1.0,0.95,2.8)[i])
for pid,date,typ,angle in sched:
    row = tbl.add_row().cells
    for i,w in enumerate((2.35,1.0,0.95,2.8)): row[i].width=Inches(w)
    row[0].paragraphs[0].add_run().add_picture(f"{TH}/{pid}.jpg", width=Inches(2.2))
    row[1].text=""; dr=row[1].paragraphs[0].add_run(date); dr.font.size=Pt(9.5); dr.bold=True; dr.font.color.rgb=GRAY
    row[2].text=""; tr=row[2].paragraphs[0].add_run(typ); tr.font.size=Pt(9.5); tr.bold=True
    tr.font.color.rgb = GOLD if typ=="Commercial" else LIME
    row[3].text=""; pr=row[3].paragraphs[0].add_run(f"{pid}  "); pr.bold=True; pr.font.size=Pt(9.5); pr.font.color.rgb=PINE
    ar=row[3].paragraphs[0].add_run(angle); ar.font.size=Pt(9.5)
    if typ=="Commercial":
        cell_bg(row[2], GOLDBG); cell_bg(row[3], GOLDBG)

para("The gold rows are your commercial installs. Those two captions speak to business owners, property "
     "managers and municipalities rather than homeowners.", 9.5, False, GRAY, before=6)

# ---------------------------------------------------------------- notes
doc.add_page_break()
h2("Notes for this series", before=0)
notes = [
 "January posts are not leftovers. The message from January 4 onward is, the lights came down, and October is already booking. Pair those captions with your early bird offer.",
 "The two commercial installs (SL_41 and SL_42) are deliberate conversation starters for business owners. If someone comments about their storefront, that's your lead. Reply fast and offer a walk through.",
 "Keep the privacy rule forever on this series. No addresses, no street signs, no city names in captions, hashtags or comment replies, even if someone asks where a photo was taken.",
 "These are also your best performing ads. When you boost anything this season, boost these twenty-four.",
 "February slots are deliberate. By then every competitor has gone quiet, so these posts carry the booking message alone. Pair them with your early bird offer and answer comments fast.",
]
for i,tip in enumerate(notes,1):
    p = doc.add_paragraph()
    r = p.add_run(f"{i}.  "); r.bold=True; r.font.color.rgb=LIME; r.font.size=Pt(10.5)
    r2 = p.add_run(tip); r2.font.size=Pt(10.5)
    p.paragraph_format.space_after=Pt(5)

bar("B8860B")
para("That's the Authentic Install Series. Real yards, real crews, real results. Here's to the season that "
     "books itself because of posts like these.", 10.5, False, GRAY)
para("Spruce Holiday Lighting & Events  ·  (864) 288-2459  ·  sprucelights.com  ·  @spruceholidaylighting",
     9.5, True, LIME, WD_ALIGN_PARAGRAPH.CENTER)

doc.save('/home/user/SL_Authentic_Install_Series.docx')
print('saved authentic doc')
