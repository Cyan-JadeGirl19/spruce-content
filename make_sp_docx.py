"""SP_Post_Captions_and_Hashtags.docx — Spruce Pro, all 28 posts (SP_01-28).
Layout matches the approved Authentic Series doc: caption cards first (large
thumbs), calendar after, locked column grids, dash-free captions."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEAL  = RGBColor(0x00, 0x30, 0x3C)
CYAN  = RGBColor(0x0E, 0x9A, 0xA0)
LIME  = RGBColor(0x7A, 0xB0, 0x2E)
GOLD  = RGBColor(0xB8, 0x86, 0x0B)
GRAY  = RGBColor(0x66, 0x66, 0x66)
BODY  = RGBColor(0x33, 0x33, 0x33)
LIGHT = "E8F4F5"
CREAM = "FAF7F0"
DYKBG = "F1F7E4"
COMBG = "FBF3DF"
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
    r = p.add_run(text); r.bold = True; r.font.size = Pt(15); r.font.color.rgb = TEAL
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(6)
    return p

def set_grid(tbl, inches):
    grid = tbl._tbl.find(qn('w:tblGrid'))
    for c, w in zip(grid.findall(qn('w:gridCol')), inches):
        c.set(qn('w:w'), str(int(w*1440)))

def cell_bg(cell, hexfill):
    el = OxmlElement('w:shd'); el.set(qn('w:val'), 'clear'); el.set(qn('w:fill'), hexfill)
    cell._tc.get_or_add_tcPr().append(el)

def bar(color_hex="0E9AA0"):
    t = doc.add_table(rows=1, cols=1); set_grid(t, (7.1,))
    c = t.cell(0,0); cell_bg(c, color_hex)
    c.paragraphs[0].add_run("").font.size = Pt(1)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

import glob as _glob
def th(pid):
    m = _glob.glob(f"{TH}/{pid}_*.jpg") or _glob.glob(f"{TH}/{pid}.jpg")
    return m[0]

# ---------------------------------------------------------------- cover
bar()
para("SPRUCE PRO  ·  EXTERIOR CLEANING", 12, True, CYAN, after=2)
p = doc.add_paragraph()
r = p.add_run("Post Captions & Hashtags"); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = TEAL
p.paragraph_format.space_after = Pt(4)
para("28 posts: 20 signature posts plus 8 Did You Know fact posts", 13, False, GOLD, after=10)
para("October through December 2026 content plan for the Spruce Pro pages", 10.5, False, BODY, after=10)

h2("How to use this pack", before=0)
para("Every post here is already designed and exported in both sizes, square for the feed and vertical "
     "for stories, in the Spruce Pro graphics folder. The caption goes in the post, the hashtags go in "
     "the first comment, and the story version reposts the same day. That rhythm keeps the page active "
     "without ever looking like a poster board.")
para("The eight Did You Know posts are your shareable, saveable, comment bait content. They teach "
     "something a homeowner did not know, which is the kind of post people send to a neighbor. Sprinkle "
     "them between the signature posts exactly as the calendar does. When you boost anything this "
     "season, boost a Did You Know first.")
para("Voice reminders: keep it local and human, reply to every comment, and never promise a result in a "
     "post you would not promise on a job site.")

# ---------------------------------------------------------------- caption cards
doc.add_page_break()
h2("Captions and hashtags", before=0)
para("In posting order for the season. The lime rows on the calendar are the Did You Know posts.",
     10, False, GRAY, after=10)

posts = [
("SP_01","Residential","Fall Refresh, Before the Holidays",
"Fall is the reset button. One visit clears the summer film off your siding, driveway and walkways so the house walks into the holidays looking its best. Fall slots fill first, so claim yours early.",
"#SprucePro #ExteriorCleaning #FallRefresh #PressureWashing #HouseWashing #CurbAppeal #HomeMaintenance #GreenvilleSC #UpstateSC #BookEarly"),
("SP_21","Residential","Did You Know: The 500 Gallon Roof",
"One inch of rain sheds about 500 gallons of water off an average roof. Clean gutters move it away from your foundation. Clogged ones dump it exactly where it does the most damage.",
"#SprucePro #DidYouKnow #GutterCleaning #HomeTips #FoundationCare #HomeMaintenance #GreenvilleSC #UpstateSC #FallHomeCare #ProtectYourHome"),
("SP_02","Residential","Pressure Washing That Transforms",
"Driveways, sidewalks, patios and pool decks. Our surface cleaner leaves even stripes with no zebra marks, and the concrete comes out several shades brighter. This is the before and after your neighbors will ask about.",
"#SprucePro #PressureWashing #ConcreteCleaning #DrivewayMakeover #CurbAppeal #ExteriorCleaning #GreenvilleSC #UpstateSC #HomeUpgrade #SatisfyingClean"),
("SP_03","Residential","The Spruce Difference",
"No filter and no trick lighting, just the difference a proper house wash makes. The left side is what pollen, dust and algae do over one summer. The right side is one afternoon of our work.",
"#SprucePro #BeforeAndAfter #HouseWashing #PressureWashing #ExteriorCleaning #CurbAppeal #RealResults #GreenvilleSC #UpstateSC #Transformation"),
("SP_07","Residential","Clean Gutters Before the Storms",
"Clogged gutters are the quiet destroyer of fascia boards, flower beds and foundations. We clear the trough, flush the downspouts, and haul the debris away. Your gutters never look cleaner or work better.",
"#SprucePro #GutterCleaning #Downspouts #HomeMaintenance #FallMaintenance #StormPrep #GreenvilleSC #UpstateSC #ProtectYourHome #BookEarly"),
("SP_22","Residential","Did You Know: The Roof Streaks Are Alive",
"Those dark streaks are Gloeocapsa magma, a living algae that feeds on the limestone inside your shingles. Rain does not wash it off, it just moves it around. We kill it at the root with SoftWash, never pressure.",
"#SprucePro #DidYouKnow #RoofCleaning #SoftWash #HomeTips #AlgaeStains #RoofCare #GreenvilleSC #UpstateSC #HomeMaintenance"),
("SP_04","Residential","Serving the Upstate Since 2006",
"Almost twenty years, thousands of homes, one standard. Licensed, insured, locally owned, and still answering our own phone. That is the boring reliability people actually want in a service company.",
"#SprucePro #Since2006 #LocallyOwned #LicensedAndInsured #ExteriorCleaning #PressureWashing #GreenvilleSC #UpstateSC #CommunityFirst #TrustLocal"),
("SP_06","Residential","Streak Free Windows, Guaranteed",
"Streak free windows change how a whole room feels. We clean the glass, the sills, the tracks and the screens, and we stand behind the result with a guarantee. You will notice it from inside before you notice it from the street.",
"#SprucePro #WindowCleaning #StreakFree #SillsAndTracks #ScreensToo #HomeMaintenance #GreenvilleSC #UpstateSC #Guaranteed #ViewRevival"),
("SP_23","Residential","Did You Know: Sprinklers Etch Glass",
"Sprinkler water leaves minerals behind, and those spots can permanently etch glass if they sit. The longer they stay, the less any cleaner can touch them. Polishing can still save the pane, so do not wait.",
"#SprucePro #DidYouKnow #HardWaterSpots #WindowCleaning #GlassCare #HomeTips #HomeMaintenance #GreenvilleSC #UpstateSC #ActFast"),
("SP_09","Residential","The Right Pressure, The Right Mix",
"Pressure is one dial and mix is another. Every surface gets its own combination, which is why our soft wash kills the algae and never scares the paint. Doing it right takes longer to set up and lasts far longer too.",
"#SprucePro #SoftWash #ScienceOfClean #PressureWashing #HouseWashing #KnowHow #ExteriorCleaning #GreenvilleSC #UpstateSC #DoneRight"),
("SP_10","Residential","Gutter Guards: Install Once, Never Scoop Again",
"Install once and retire the ladder. Gutter guards keep the debris out and the water moving, and we fit them to your existing gutters. Ask about our clog free guarantee and stop booking cleanings you should never have needed.",
"#SprucePro #GutterGuards #NeverScoopAgain #OneAndDone #HomeUpgrade #GutterCleaning #GreenvilleSC #UpstateSC #SmartHome #Guarantee"),
("SP_25","Residential","Did You Know: The Green Side Of The House",
"The green tint on your siding is algae, and it spreads. Every rain splash moves it to the panels next door, which is why one dirty wall becomes two. Our SoftWash mix kills it at the root and rinses clean, no residue.",
"#SprucePro #DidYouKnow #HouseWashing #AlgaeStains #SoftWash #SidingCare #HomeTips #GreenvilleSC #UpstateSC #CurbAppeal"),
("SP_08","Residential","Maria's Five Star Review",
"Five stars from Maria, who watched Jacob and Christian work through a full window job and wrote about it on Facebook. Real crews, real reviews, real neighbors. Thank you for having us back any time.",
"#SprucePro #FiveStars #CustomerReview #FacebookReview #WindowCleaning #RealReviews #ThankYou #GreenvilleSC #UpstateSC #TeamSpruce"),
("SP_11","Residential","Get Guest Ready Before They Arrive",
"The guests are coming and the driveway knows it. One visit handles the wash, the windows and the gutters before the first casserole lands. Be the house everyone compliments on the way in.",
"#SprucePro #HolidayPrep #GuestReady #PressureWashing #WindowCleaning #GutterCleaning #GreenvilleSC #UpstateSC #HostingSeason #BookEarly"),
("SP_26","Residential","Did You Know: How Gutter Guards Think",
"It looks like magic but it is fluid dynamics. Water clings to the curved nose of the guard and follows it into the gutter while the leaves ride over the top and away. The leaf never touches the water it loses to.",
"#SprucePro #DidYouKnow #GutterGuards #HowItWorks #FluidDynamics #HomeTips #SmartHome #GreenvilleSC #UpstateSC #ScienceOfClean"),
("SP_13","Residential","Roof Cleaning Without the Damage",
"Your roof does not need pressure, it needs the right treatment. Pressure strips granules and shortens shingle life. Our SoftWash kills the algae at the root and keeps roofs clean four to five times longer than water alone.",
"#SprucePro #RoofCleaning #SoftWashOnly #ShingleCare #RoofLife #NoPressure #ExteriorCleaning #GreenvilleSC #UpstateSC #SmartChoice"),
("SP_05","Residential","This Weekend: Driveway or House First?",
"Quick poll for the comment section. If we rolled up to your place this weekend, do we start with the driveway or the house wash? A or B below, and yes, most of you are saying both.",
"#SprucePro #CommentBelow #WeekendPoll #DrivewayOrHouse #PressureWashing #HouseWashing #GreenvilleSC #UpstateSC #Community #PickOne"),
("SP_27","Residential","Did You Know: Concrete Drinks",
"Concrete is porous. Every oil drip, rust streak and grime film sinks in and darkens it year after year. Professional cleaning opens the pores back up and lifts the stains out, and sealing keeps them from settling in again.",
"#SprucePro #DidYouKnow #ConcreteCleaning #PorousSurfaces #DrivewayCleaning #HomeTips #SealingDoneRight #GreenvilleSC #UpstateSC #CurbAppeal"),
("SP_12","Commercial","Commercial Exteriors, Handled",
"Storefronts, campuses, parking decks and fleets. We work early hours, we work around your schedule, and we leave the glass and concrete looking brand new. Property managers, one call covers the whole property.",
"#SprucePro #CommercialCleaning #PropertyManagers #StorefrontClean #ParkingDeck #FleetWashing #GreenvilleSC #UpstateSC #FacilityCare #OneCall"),
("SP_18","Residential","November Slots Open Now",
"The November calendar is open and the good slots go first. If you want the wash, the windows or the gutters done before the holidays hit full speed, this is the week to claim it. Two minutes to book, that is the whole job on your end.",
"#SprucePro #BookingNow #NovemberSlots #FallCleaning #PressureWashing #WindowCleaning #GutterCleaning #GreenvilleSC #UpstateSC #BookEarly"),
("SP_14","Residential","Greenville's Exterior Cleaning Pros",
"Born and raised right here. We wash the homes we grew up riding past, and our name is on every one of them. Local crew, local address, local reputation, and we plan to keep all three spotless.",
"#SprucePro #GreenvilleSC #LocallyOwned #UpstateSC #CommunityProud #ExteriorCleaning #ShopLocal #HomeTown #PressureWashing #OurNeighborhood"),
("SP_16","Residential","Streaks Happen. We Fix Them.",
"Streaky windows happen to everyone, especially after rain drags dirt through the tracks. Our rescue pass clears the glass, the sills and the screens, and the view comes back like someone changed the channel.",
"#SprucePro #WindowRescue #StreakFree #RainSeason #WindowCleaning #SillsAndTracks #ViewRevival #GreenvilleSC #UpstateSC #WeFixThat"),
("SP_15","Residential","Why Late Fall Is Washing Season",
"Cooler air, lower pollen, softer sun. Late fall is the kindest window of the year for a full exterior wash, and everything stays clean longer going into winter. Beat the freeze and book the reset now.",
"#SprucePro #ProTip #WashingSeason #LateFall #HouseWashing #HomeMaintenance #BeatTheFreeze #GreenvilleSC #UpstateSC #BookEarly"),
("SP_28","Commercial","Did You Know: Graffiti Fights Back If You Wait",
"Speed matters with graffiti. Fresh paint lifts in one visit, cured paint can take a second pass and sometimes leaves a shadow. Call the day it happens and we will make the wall forget it ever happened, with before photos for your insurer.",
"#SprucePro #DidYouKnow #GraffitiRemoval #CommercialProperty #FastResponse #AntiGraffiti #PropertyManagers #GreenvilleSC #UpstateSC #Documented"),
("SP_19","Residential","Licensed, Insured, Since 2006",
"Licensed and insured is the boring sentence that saves you thousands. If anyone gets hurt on your property and a company cannot prove coverage, that risk lands on you. Ours is current, verifiable, and nineteen years deep.",
"#SprucePro #LicensedAndInsured #PeaceOfMind #Since2006 #HireRight #HomeMaintenance #GreenvilleSC #UpstateSC #Protected #TrustLocal"),
("SP_24","Residential","Did You Know: Our Drone Cleans Five Stories Up",
"Our drone rig clears gutters and rooflines up to five stories with nobody on a ladder and nobody on your roof. You get video inspection footage with the quote, so you see exactly what we see.",
"#SprucePro #DidYouKnow #DroneCleaning #NoLadders #FiveStories #VideoInspection #InnovationUpstate #GreenvilleSC #UpstateSC #FutureOfClean"),
("SP_20","Residential","Your Fall Exterior Checklist",
"Your fall exterior checklist in one post. Gutters cleared before the storms, house washed before the guests, windows done while the sun still cooperates, concrete sealed before the freeze. Screenshot it and check it off, or hand it to us whole.",
"#SprucePro #FallChecklist #HomeMaintenance #GutterCleaning #HouseWashing #WindowCleaning #ConcreteSealing #GreenvilleSC #UpstateSC #ScreenshotThis"),
("SP_17","Residential","Let's Get Your Home Spruced Up",
"That is the season wrapped. If one of these posts described your house a little too well, the fix is one call. Free quotes, fast scheduling, and a crew that treats your place like the neighborhood is watching, because it is.",
"#SprucePro #FreeQuote #BookNow #SpruceProSeason #ExteriorCleaning #PressureWashing #WindowCleaning #GutterCleaning #GreenvilleSC #UpstateSC"),
]

for pid, typ, name, cap, tags in posts:
    t = doc.add_table(rows=1, cols=2); t.autofit=False
    set_grid(t, (2.35, 4.75))
    left, right = t.rows[0].cells
    left.width=Inches(2.35); right.width=Inches(4.75)
    left.paragraphs[0].add_run().add_picture(th(pid), width=Inches(2.2))
    right.text=""
    hp = right.paragraphs[0]
    hr = hp.add_run(f"{pid}  ·  {name}   "); hr.bold=True; hr.font.size=Pt(11); hr.font.color.rgb=TEAL
    dyk = "Did You Know" in name
    lbl = "DID YOU KNOW" if dyk else typ.upper()
    tr = hp.add_run(lbl); tr.bold=True; tr.font.size=Pt(9)
    tr.font.color.rgb = LIME if dyk else (GOLD if typ=="Commercial" else CYAN)
    hp.paragraph_format.space_after=Pt(3)
    cp = right.add_paragraph(); cr=cp.add_run(cap); cr.font.size=Pt(10.5)
    cp.paragraph_format.space_after=Pt(3)
    tp = right.add_paragraph(); trr=tp.add_run(tags); trr.font.size=Pt(9); trr.font.color.rgb=GRAY
    tp.paragraph_format.space_after=Pt(2)
    cell_bg(right, DYKBG if dyk else (COMBG if typ=="Commercial" else CREAM))
    doc.add_paragraph().paragraph_format.space_after=Pt(0)

# ---------------------------------------------------------------- calendar
doc.add_page_break()
h2("The calendar", before=0)
para("Three posts a week, Mondays, Wednesdays and Fridays, October 5 through December 7. The Did You "
     "Know posts (lime rows) are spread between the signature posts so the page never goes quiet and "
     "never goes repetitive.", 10, False, GRAY, after=8)

sched = [
 ("SP_01","Mon Oct 5","Residential","Fall refresh season opener"),
 ("SP_21","Wed Oct 7","Did You Know","The 500 gallon roof"),
 ("SP_02","Fri Oct 9","Residential","Pressure washing transformation"),
 ("SP_03","Mon Oct 12","Residential","The Spruce difference, before and after"),
 ("SP_07","Wed Oct 14","Residential","Clean gutters before the storms"),
 ("SP_22","Fri Oct 16","Did You Know","Roof streaks are living algae"),
 ("SP_04","Mon Oct 19","Residential","Serving the Upstate since 2006"),
 ("SP_06","Wed Oct 21","Residential","Streak free windows"),
 ("SP_23","Fri Oct 23","Did You Know","Sprinklers etch glass"),
 ("SP_09","Mon Oct 26","Residential","The SoftWash science post"),
 ("SP_10","Wed Oct 28","Residential","Gutter guards, never scoop again"),
 ("SP_25","Fri Oct 30","Did You Know","The green side of the house"),
 ("SP_08","Mon Nov 2","Residential","Maria's five star review"),
 ("SP_11","Wed Nov 4","Residential","Guest ready before the holidays"),
 ("SP_26","Fri Nov 6","Did You Know","How gutter guards think"),
 ("SP_13","Mon Nov 9","Residential","Roof cleaning without damage"),
 ("SP_05","Wed Nov 11","Residential","Poll: driveway or house first"),
 ("SP_27","Fri Nov 13","Did You Know","Concrete drinks, pores and stains"),
 ("SP_12","Mon Nov 16","Commercial","Commercial exteriors, handled"),
 ("SP_18","Wed Nov 18","Residential","November slots open now"),
 ("SP_14","Fri Nov 20","Residential","Greenville's own crew"),
 ("SP_16","Mon Nov 23","Residential","Streaks happen, we fix them"),
 ("SP_15","Wed Nov 25","Residential","Why late fall is washing season"),
 ("SP_28","Fri Nov 27","Did You Know","Graffiti: speed matters (commercial)"),
 ("SP_19","Mon Nov 30","Residential","Licensed and insured since 2006"),
 ("SP_24","Wed Dec 2","Did You Know","Drone cleans five stories up"),
 ("SP_20","Fri Dec 4","Residential","The fall exterior checklist"),
 ("SP_17","Mon Dec 7","Residential","Season close, free quotes"),
]
tbl = doc.add_table(rows=1, cols=4); tbl.autofit = False
set_grid(tbl, (2.35, 1.0, 0.95, 2.8))
hdr = tbl.rows[0].cells
for i,t in enumerate(("Preview","Date","Type","Post and angle")):
    hdr[i].text=""
    r = hdr[i].paragraphs[0].add_run(t); r.bold=True; r.font.size=Pt(10); r.font.color.rgb=TEAL
    cell_bg(hdr[i], LIGHT)
    hdr[i].width = Inches((2.35,1.0,0.95,2.8)[i])
for pid,date,typ,angle in sched:
    row = tbl.add_row().cells
    for i,w in enumerate((2.35,1.0,0.95,2.8)): row[i].width=Inches(w)
    row[0].paragraphs[0].add_run().add_picture(th(pid), width=Inches(2.2))
    row[1].text=""; dr=row[1].paragraphs[0].add_run(date); dr.font.size=Pt(9.5); dr.bold=True; dr.font.color.rgb=GRAY
    row[2].text=""; tr=row[2].paragraphs[0].add_run(typ); tr.font.size=Pt(9.5); tr.bold=True
    if typ=="Did You Know":
        tr.font.color.rgb = LIME
        for ci in (2,3): cell_bg(row[ci], DYKBG)
    elif typ=="Commercial":
        tr.font.color.rgb = GOLD
        for ci in (2,3): cell_bg(row[ci], COMBG)
    else:
        tr.font.color.rgb = CYAN
    row[3].text=""; pr=row[3].paragraphs[0].add_run(f"{pid}  "); pr.bold=True; pr.font.size=Pt(9.5); pr.font.color.rgb=TEAL
    ar=row[3].paragraphs[0].add_run(angle); ar.font.size=Pt(9.5)

para("Lime rows are the Did You Know fact posts. The gold row (SP_12) plus the graffiti post speak to "
     "business owners and property managers, the rest speak to homeowners.", 9.5, False, GRAY, before=6)

# ---------------------------------------------------------------- notes
doc.add_page_break()
h2("Notes for this pack", before=0)
notes = [
 "Post the story version the same day as the feed post. Stories are where the polls and question stickers live, so SP_05 works twice as hard that way.",
 "The Did You Know posts are your ads. When one earns shares or saves, put a small boost behind it within 48 hours while the algorithm is warm.",
 "The commercial posts (SP_12 and SP_28) are conversation starters for property managers. A storefront comment is a lead, reply fast and offer a walkthrough.",
 "SP_17 closes the season on December 7. Right after it, pivot the page to January booking messages, the lights come down and the wash season starts again.",
 "Keep the voice consistent: local, confident, never salesy. If a caption sounds like a flyer, rewrite it like you are telling a neighbor.",
]
for i,tip in enumerate(notes,1):
    p = doc.add_paragraph()
    r = p.add_run(f"{i}.  "); r.bold=True; r.font.color.rgb=LIME; r.font.size=Pt(10.5)
    r2 = p.add_run(tip); r2.font.size=Pt(10.5)
    p.paragraph_format.space_after=Pt(5)

bar("0E9AA0")
para("That's the Spruce Pro season. Twenty signature posts, eight facts worth sharing, one standard on "
     "every job. Here's to a full calendar.", 10.5, False, GRAY)
para("Spruce Pro  ·  (864) 483-4300  ·  sprucepro.com  ·  @spruce_pro",
     9.5, True, CYAN, WD_ALIGN_PARAGRAPH.CENTER)

doc.save('/home/user/SP_Post_Captions_and_Hashtags.docx')
print('saved SP doc')
