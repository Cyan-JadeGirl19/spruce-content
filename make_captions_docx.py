#!/usr/bin/env python3
"""Spruce Lights content pack v2: Word doc with thumbnails + 3/week visual calendar."""
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
TH = "/tmp/thumbs"

doc = Document()
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(11); st.font.color.rgb = BODY
for sec in doc.sections:
    sec.left_margin = sec.right_margin = Inches(0.7)
    sec.top_margin = Inches(0.7); sec.bottom_margin = Inches(0.7)

def para(text="", size=11, bold=False, color=BODY, align=None, after=6, before=0, italic=False):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic; r.font.color.rgb = color
    if align: p.alignment = align
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    return p

def h2(text, before=14):
    p = doc.add_paragraph()
    r = p.add_run(text); r.bold = True; r.font.size = Pt(15); r.font.color.rgb = PINE
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(6)
    return p

def cell_bg(cell, hexfill):
    el = OxmlElement('w:shd'); el.set(qn('w:val'), 'clear'); el.set(qn('w:fill'), hexfill)
    cell._tc.get_or_add_tcPr().append(el)

def bar(color_hex="7AB02E"):
    t = doc.add_table(rows=1, cols=1)
    c = t.cell(0,0); cell_bg(c, color_hex)
    c.paragraphs[0].add_run("").font.size = Pt(1)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def set_cell_w(cell, inches):
    cell.width = Inches(inches)

# ---------------------------------------------------------------- cover
bar()
para("SPRUCE HOLIDAY LIGHTING & EVENTS", 12, True, LIME, after=2)
p = doc.add_paragraph()
r = p.add_run("October 2026 Content Pack"); r.bold = True; r.font.size = Pt(26); r.font.color.rgb = PINE
p.paragraph_format.space_after = Pt(4)
para("Captions, hashtags and a visual posting calendar for all 30 posts", 13, False, GOLD, after=10)
para("Prepared by your social media team  ·  October 8, 2026", 10, False, GRAY, after=2)
para("Three posts a week, Monday Wednesday Friday, with the Halloween moments locked to their exact days. The calendar now runs the full season, closing with five real customer installs we shot on site.", 10.5, False, BODY, after=10)

h2("A quick hello")
para("Hi Spruce team! In this pack you'll find everything needed to run the season without writing a single "
     "caption yourself: a calendar showing exactly which graphic goes up on which day (with a little preview "
     "of each one so you always know what you're posting), a ready to paste caption and hashtag set for every "
     "post, and a few habits that make the whole thing perform.")
para("The graphics already show your phone, website and handle, so captions stay conversational instead of "
     "repeating them. Tweak any line that doesn't sound like you. That's allowed and encouraged.")

# ---------------------------------------------------------------- calendar
doc.add_page_break()
h2("The calendar at a glance", before=0)
para("Three posts a week. The one exception is Halloween week, which gets two bonus posts because the moment "
     "only comes once a year. Each row shows the actual graphic so there's no guessing which is which.",
     10, False, GRAY, after=8)

sched = [
 ("SL_01","Fri Oct 9","Campaign launch, the mansion hero"),
 ("SL_06","Mon Oct 12","Homes, businesses and towns"),
 ("SL_14","Wed Oct 14","Why book in October"),
 ("SL_02","Fri Oct 16","Michelle review"),
 ("SL_04","Mon Oct 19","Free service calls"),
 ("SL_05","Wed Oct 21","The process"),
 ("SL_07","Fri Oct 23","Poll, which look wins"),
 ("SL_24","Mon Oct 26","Year round, cafe patio"),
 ("SL_25","Wed Oct 28","Year round, backyard pergola"),
 ("SL_08","Fri Oct 30","Halloween crossover, day before"),
 ("SL_30","Sat Oct 31, morning","Halloween porch"),
 ("SL_20","Sat Oct 31, evening","Happy Halloween Greenville"),
 ("SL_29","Mon Nov 2","Christmas begins, reindeer and sleigh"),
 ("SL_12","Wed Nov 4","Countdown to install season"),
 ("SL_09","Fri Nov 6","Why professional installs"),
 ("SL_10","Mon Nov 9","Randy review"),
 ("SL_16","Wed Nov 11","Stag light trail, showstopper"),
 ("SL_17","Fri Nov 13","Jan review"),
 ("SL_21","Mon Nov 16","Before and after, mansion"),
 ("SL_03","Wed Nov 18","Before and after, classic"),
 ("SL_22","Fri Nov 20","Overnight street transformation"),
 ("SL_13","Mon Nov 23","HOA and municipal programs"),
 ("SL_18","Wed Nov 25","Slots almost gone"),
 ("SL_27","Fri Nov 27","Showstopper tree wrap"),
 ("SL_28","Mon Nov 30","Lake life"),
 ("SL_23","Wed Dec 2","Your town aglow"),
 ("SL_26","Fri Dec 4","Year round, bistro"),
 ("SL_15","Mon Dec 7","Poll, ladder or cocoa"),
 ("SL_11","Wed Dec 9","Be the favorite house"),
 ("SL_19","Fri Dec 11","Direct call to action"),
]
tbl = doc.add_table(rows=1, cols=3)
tbl.autofit = False
hdr = tbl.rows[0].cells
labels = ("Preview","Date","Post and angle")
for i, t in enumerate(labels):
    hdr[i].text = ""
    r = hdr[i].paragraphs[0].add_run(t); r.bold = True; r.font.size = Pt(10); r.font.color.rgb = PINE
    cell_bg(hdr[i], LIGHT); set_cell_w(hdr[i], (1.2, 1.35, 4.35)[i])
for pid, date, angle in sched:
    row = tbl.add_row().cells
    set_cell_w(row[0], 1.2); set_cell_w(row[1], 1.35); set_cell_w(row[2], 4.35)
    # thumbnail
    pb = row[0].paragraphs[0].add_run().add_picture(f"{TH}/{pid}.jpg", width=Inches(1.05))
    # date
    row[1].text = ""
    dr = row[1].paragraphs[0].add_run(date); dr.font.size = Pt(9.5); dr.font.color.rgb = GRAY; dr.bold = True
    # post id + angle
    row[2].text = ""
    pr = row[2].paragraphs[0].add_run(f"{pid}  "); pr.bold = True; pr.font.size = Pt(9.5); pr.font.color.rgb = GOLD
    ar = row[2].paragraphs[0].add_run(angle); ar.font.size = Pt(9.5)
    if pid in ("SL_20","SL_30"):
        cell_bg(row[1], LIGHT); cell_bg(row[2], LIGHT)

para("The green highlighted rows are your Halloween day posts. Post SL_30 with your morning coffee and SL_20 "
     "right around trick or treat time.", 9.5, False, GRAY, before=6)

# ---------------------------------------------------------------- captions
doc.add_page_break()
h2("Captions and hashtags, post by post", before=0)
para("Copy the caption into the post, drop the hashtags in as the first comment to keep everything looking "
     "clean. Feed and story versions of a graphic share the same caption.", 10, False, GRAY, after=10)

posts = [
("SL_01","Booking launch (mansion)",
"You know that one house in your neighborhood that everyone slows down for? That could be yours this year. We design every roofline, install every bulb, and you never climb a single ladder. October install weeks are open right now and the good ones go fast.",
"#SpruceLights #ChristmasLightInstallation #HolidayLighting #GreenvilleSC #YeahThatGreenville #UpstateSC #ChristmasIsComing #LightUpTheHolidays #OctoberBooking #HouseGoals"),
("SL_02","Review from Michelle",
"\"Made our house look magical.\" That's Michelle B. from right here in Greenville, and her five star review means the world to us. We've got over 55 of them on Google now, and every single job gets that same treatment.",
"#SpruceLights #GoogleReview #FiveStars #GreenvilleSC #UpstateSC #HolidayLighting #ChristmasLights #CustomerLove #ShopLocal #MagicalHomes"),
("SL_03","Before and after (classic)",
"Same house. Same evening. The only difference is what happened at 2pm while you were at work. Professional design and install really does change everything, and honestly the photos don't even do it justice.",
"#SpruceLights #BeforeAndAfter #GlowUp #ChristmasLightInstallation #GreenvilleSC #UpstateSC #HolidayLighting #ChristmasMagic #InstalledRight #Transformation"),
("SL_04","Free service calls",
"Here's something nobody else does: if a bulb goes out or a strand acts up anytime this season, we come fix it. Free. You literally call, we show up, done. That's the Spruce promise and it comes with every single install.",
"#SpruceLights #FreeServiceCalls #NoWorries #HolidayLighting #GreenvilleSC #UpstateSC #ChristmasLights #StressFreeSeason #LocalAndTrusted #TheSprucePromise"),
("SL_05","The process",
"People ask what \"full service\" actually means. It means we design the display with you, install every strand, take it all down after the holidays, and store the lights in our warehouse until next year. You never touch a ladder. You just come home to a glowing house.",
"#SpruceLights #FullService #DesignInstallStore #ZeroLadders #GreenvilleSC #YeahThatGreenville #UpstateSC #ChristmasLightInstallation #EasySeason #DoneForYou"),
("SL_06","Homes, businesses, towns",
"One porch or one whole street, we do both. If you run a business or you're on an HOA board, ask about our commercial and municipal programs. Bulk pricing, unified designs, one crew that shows up on time.",
"#SpruceLights #CommercialLighting #MunicipalLighting #HOALighting #GreenvilleSC #UpstateSC #HolidayLighting #MainStreetMagic #LightItUp #AllInclusive"),
("SL_07","Poll: which look wins?",
"Rooflines, trees, or walkways? Everyone has a favorite and people get weirdly passionate about this. Drop yours in the comments. Bonus points if you tag a neighbor who desperately needs the walkway treatment.",
"#SpruceLights #ThisOrThat #ChristmasPoll #CommentBelow #GreenvilleSC #UpstateSC #HolidayLighting #ChristmasDecor #NeighborhoodGoals #LightDesign"),
("SL_08","Halloween crossover",
"The pumpkins are still on the porch but guess what, December is coming whether we like it or not. Book your Christmas install now while there's still room on the calendar. Future you will be very grateful.",
"#SpruceLights #HalloweenToChristmas #BookEarly #GreenvilleSC #UpstateSC #HolidayLighting #PumpkinSeason #PlanAhead #FallInGreenville #ChristmasIsComing"),
("SL_09","Why professional installs (light arch trail)",
"This is what commercial grade looks like. Real hardware, real strands built for winter weather, and a crew that knows what they're doing on a ladder. It holds up through storms and it looks like this every single night.",
"#SpruceLights #CommercialGrade #ProInstalled #HolidayLighting #LightTrail #GreenvilleSC #UpstateSC #EventLighting #DoItRight #BuiltToLast"),
("SL_10","Review from Randy",
"\"Great team. Excellent work.\" Randy kept it short and sweet and honestly that's all we need. On time, uniformed crews, and when we leave you'd never know we were there. Except after dark of course.",
"#SpruceLights #FiveStarReview #GreatTeam #GreenvilleSC #UpstateSC #HolidayLighting #CustomerFirst #ChristmasLights #TrustedLocal #ShopSmall"),
("SL_11","Be the favorite house (reindeer and sleigh)",
"There's always one house. The one kids beg to walk past, the one that ends up in seventeen family Christmas photos. Might as well make it yours this year. The reindeer and sleigh setup is available and yes, it's as good as it looks.",
"#SpruceLights #FavoriteHouse #SleighSeason #ReindeerLights #GreenvilleSC #UpstateSC #HolidayLighting #FrontYardGoals #ChristmasEnvy #TangleFree"),
("SL_12","Countdown to install season",
"The calendar is the real Grinch here. Every November we get calls from folks who want the first week and by then it's gone. Lock your week now and skip the panic entirely.",
"#SpruceLights #BookNow #InstallSeason #GreenvilleSC #YeahThatGreenville #UpstateSC #HolidayLighting #DontWait #ChristmasCountdown #PlanAhead"),
("SL_13","HOAs, businesses and towns",
"Want the whole street glowing? We handle full neighborhood and HOA displays with unified designs and bulk rates. One point of contact, one invoice, zero headaches for your board. 2026 proposals are open.",
"#SpruceLights #HOALighting #CommunityChristmas #MunicipalLighting #GreenvilleSC #UpstateSC #HolidayLighting #LightUpTheNeighborhood #TownSquare #ProposalSeason"),
("SL_14","Why October (golden farmhouse)",
"Simple math really. Book in October and you get first pick of install weeks, nicer weather for the crew, and lights that are ready before the first cold snap. Same price as always. Just a better spot in line.",
"#SpruceLights #ProTip #BookInOctober #GreenvilleSC #UpstateSC #HolidayLighting #FallInGreenville #SmartHomeowner #GoldenHour #BetterSlot"),
("SL_15","Poll: ladder this weekend or cocoa?",
"Be honest with us. Is that ladder actually happening this weekend, or are you staying in your pajamas with cocoa like a responsible adult? There's a third option by the way. It involves us doing the whole thing for you.",
"#SpruceLights #HonestPoll #TeamCocoa #NeverTouchALadder #GreenvilleSC #UpstateSC #HolidayLighting #CommentBelow #FridayFunny #ChristmasPrep"),
("SL_16","Trees that stop traffic (stag light trail)",
"Some displays make people pull over. That's the bar we set for tree wraps and event style lighting, and this one's our favorite so far this year. Imagine this on your property.",
"#SpruceLights #TreeWraps #LightTrail #Showstopper #GreenvilleSC #UpstateSC #HolidayLighting #YardOfTheYear #ChristmasDestination #SignatureService"),
("SL_17","Review from Jan",
"\"My wrapped trees look amazing!!\" Jan gets it. Tree wraps are the upgrade everyone asks about once they see one in person. If you've got a big oak or a row of crepe myrtles, we can make them the stars of the street.",
"#SpruceLights #FiveStarReview #TreeWraps #CustomerLove #GreenvilleSC #UpstateSC #HolidayLighting #WrappedTrees #LocalFavorite #AmazingResults"),
("SL_18","Slots almost gone",
"Real talk: the first two weeks of November are almost full. If you want your lights up before Thanksgiving, this is the week to call. After that we're into December dates and nobody wants that.",
"#SpruceLights #LastCall #SlotsFillingFast #BookNow #GreenvilleSC #YeahThatGreenville #UpstateSC #HolidayLighting #ThanksgivingReady #TimeSensitive"),
("SL_19","Closing call to action",
"One call and the whole season handles itself. Design, install, maintenance all season, takedown in January, storage until next year. Give us a ring at (864) 288-2459. A real person picks up.",
"#SpruceLights #NowBooking #HolidayLighting #GreenvilleSC #UpstateSC #OneCallDoesItAll #ChristmasLights #StressFreeHolidays #CallToday #LocalBusiness"),
("SL_20","Happy Halloween Greenville",
"Candy tonight, twinkle soon. While you're out walking the neighborhood tonight, keep an eye on the rooflines. A few of them already sparkle, and those are our folks. Yours can join them next year.",
"#SpruceLights #HappyHalloween #GreenvilleSC #YeahThatGreenville #UpstateSC #TrickOrTreat #CandyTonight #TwinkleSoon #FallFun #ChristmasNext"),
("SL_21","Before and after (mansion)",
"On the left, a perfectly nice stone house on a Tuesday in November. On the right, the same house making the whole street better. Design matters. Warm white on stone with glowing ridge lines never misses.",
"#SpruceLights #BeforeAndAfter #LuxuryLighting #CurbAppeal #GreenvilleSC #UpstateSC #HolidayLighting #EstateLighting #GlowUp #DreamHome"),
("SL_22","Overnight transformation (street)",
"Here's how it works for business districts. Plain street at closing time. Glowing boulevard by the next morning. Your customers show up and the whole block feels like a Hallmark set. Ask about commercial installs.",
"#SpruceLights #CommercialLighting #MainStreet #BeforeAndAfter #GreenvilleSC #UpstateSC #HolidayLighting #ShopLocal #DistrictGlow #OvernightMagic"),
("SL_23","Your town aglow",
"Small towns do Christmas better and we love being part of it. Municipal programs come with unified designs, bulk rates, and zero extra work for your public works crew. Get your town on the 2026 schedule.",
"#SpruceLights #MunicipalLighting #TownSquare #SmallTownChristmas #GreenvilleSC #UpstateSC #HolidayLighting #CommunityFirst #TreeLighting #PublicSpaces"),
("SL_24","Year round lighting (cafe patio)",
"These lights stay up all year and honestly that's the point. Warm string lights over a patio keep tables full in October and April alike. Restaurant owners, this is the cheapest seat upgrade you'll ever make.",
"#SpruceLights #YearRoundLighting #CafeLights #PatioSeason #GreenvilleSC #UpstateSC #OutdoorDining #RestaurantLife #Ambiance #HospitalityDesign"),
("SL_25","Year round lighting (pergola)",
"Tuesday night dinner hits different under string lights. Pergola weaves, fence lines, lantern glow. Your backyard becomes the place everyone wants to be, twelve months a year.",
"#SpruceLights #YearRoundLighting #PergolaLights #BackyardGoals #GreenvilleSC #UpstateSC #OutdoorLiving #HomeUpgrade #CozyVibes #TuesdayNights"),
("SL_26","Year round lighting (bistro)",
"Restaurants ask us if permanent lighting is worth it. Then they watch their evening covers climb and stop asking. Roofline plus patio string lights, and suddenly every guest is taking photos of your venue. Free marketing.",
"#SpruceLights #YearRoundLighting #PermanentLighting #RestaurantOwners #ROI #GreenvilleSC #UpstateSC #VenueLighting #BistroVibes #BusinessUpgrade"),
("SL_27","The showstopper tree wrap",
"One oak tree. Hundreds of strands, thousands of bulbs. Every year the first wrapped tree on the block becomes the one everyone photographs. Pricing is by tree size, message us for a same week quote.",
"#SpruceLights #TreeWrap #Showstopper #GreenvilleSC #UpstateSC #HolidayLighting #BiggerIsBrighter #YardGoals #QuoteToday #SignatureService"),
("SL_28","Lake life, lit up",
"Docks, boathouses, lakeside porches. If your home faces the water, the reflection does half the work for you. Lake installs book earliest every year so grab your week while they're open.",
"#SpruceLights #LakeLife #DockLighting #LakesideLiving #GreenvilleSC #UpstateSC #HolidayLighting #WaterViewGlow #LakeHome #BookEarly"),
("SL_29","Classic reindeer and sleigh",
"The classic lawn tableau, done properly. Reindeer out front, sleigh behind, and a roofline dressed in warm white to tie it together. Front yard fame starts with one phone call.",
"#SpruceLights #ClassicChristmas #ReindeerAndSleigh #FavoriteHouse #GreenvilleSC #UpstateSC #HolidayLighting #FrontYardFame #ChristmasTradition #YardEnvy"),
("SL_30","Halloween porch, Christmas next",
"This porch does both seasons right. Garland on the columns for October, warm twinkle for December, pumpkins optional but encouraged. Book now and yours is the porch everyone photographs next year.",
"#SpruceLights #HalloweenToChristmas #PorchGoals #GarlandAndLights #GreenvilleSC #YeahThatGreenville #UpstateSC #HolidayLighting #MostPinned #BookForChristmas"),
]

# keep captions in the same order as the calendar for easy cross referencing
order = {pid: i for i, (pid, _, _) in enumerate(sched)}
posts.sort(key=lambda x: order[x[0]])

for pid, name, cap, tags in posts:
    t = doc.add_table(rows=1, cols=2)
    t.autofit = False
    left, right = t.rows[0].cells
    set_cell_w(left, 1.5); set_cell_w(right, 5.4)
    # thumbnail
    left.paragraphs[0].add_run().add_picture(f"{TH}/{pid}.jpg", width=Inches(1.35))
    # right cell: header, caption, tags
    right.text = ""
    hp = right.paragraphs[0]
    hr = hp.add_run(f"{pid}  ·  {name}"); hr.bold = True; hr.font.size = Pt(11); hr.font.color.rgb = PINE
    hp.paragraph_format.space_after = Pt(3)
    cp = right.add_paragraph()
    cr = cp.add_run(cap); cr.font.size = Pt(10.5)
    cp.paragraph_format.space_after = Pt(3)
    tp = right.add_paragraph()
    tr = tp.add_run(tags); tr.font.size = Pt(9); tr.font.color.rgb = GRAY
    tp.paragraph_format.space_after = Pt(2)
    cell_bg(right, CREAM)
    spacer = doc.add_paragraph(); spacer.paragraph_format.space_after = Pt(0)

# ---------------------------------------------------------------- bank + tips
doc.add_page_break()
h2("The hashtag bank", before=0)
para("Every caption already has its ten tags picked. If you want to swap any out, pull from here. One rule we "
     "stick to: always keep three to five Greenville area tags so Instagram and Facebook keep showing you to "
     "local homeowners.", 10, False, GRAY)
bank = [
 ("Brand", "#SpruceLights  #SpruceHolidayLighting  #LightUpTheHolidays"),
 ("Services", "#ChristmasLightInstallation  #HolidayLighting  #OutdoorLighting  #TreeWraps  #PermanentLighting  #FullService  #DesignInstallStore"),
 ("Local", "#GreenvilleSC  #YeahThatGreenville  #UpstateSC  #GreerSC  #MauldinSC  #TaylorsSC  #PowdersvilleSC  #PiedmontSC  #GrandStrand  #WesternNC"),
 ("Seasonal", "#ChristmasIsComing  #FallInGreenville  #HalloweenToChristmas  #BookEarly  #TisTheSeason  #DecemberReady"),
 ("Engagement", "#CommentBelow  #ThisOrThat  #BeforeAndAfter  #NeighborGoals  #YardEnvy"),
]
for k, v in bank:
    p = doc.add_paragraph()
    r = p.add_run(k + ":  "); r.bold = True; r.font.size = Pt(10.5); r.font.color.rgb = PINE
    r2 = p.add_run(v); r2.font.size = Pt(10.5)
    p.paragraph_format.space_after = Pt(5)

h2("Five habits that make these posts work harder")
tips = [
 "Stick to the Monday Wednesday Friday rhythm. Consistency trains the algorithm and your audience.",
 "Halloween day is the one exception: SL_30 goes up in the morning, SL_20 in the evening, and together they own the whole day.",
 "The review posts (02, 10 and 17) do best Tuesday to Thursday mornings when people are having coffee. On this calendar they already land on Mondays and Fridays, so just aim for the morning window.",
 "The polls (07 and 15) do best Friday afternoons when everyone is winding down. Reply to every comment within the hour, even with just an emoji and a question.",
 "Repost the story version of each graphic on the same day as the feed post. It warms up the algorithm for the feed version.",
]
for i, tip in enumerate(tips, 1):
    p = doc.add_paragraph()
    r = p.add_run(f"{i}.  "); r.bold = True; r.font.color.rgb = LIME; r.font.size = Pt(10.5)
    r2 = p.add_run(tip); r2.font.size = Pt(10.5)
    p.paragraph_format.space_after = Pt(5)

bar("B8860B")
para("That's the whole pack. If a caption doesn't sound quite like you, change that one line and keep the rest. "
     "Consistency beats perfection every time. Here's to your biggest season yet!", 10.5, False, GRAY)
para("Spruce Holiday Lighting & Events  ·  (864) 288-2459  ·  sprucelights.com  ·  @spruceholidaylighting",
     9.5, True, LIME, WD_ALIGN_PARAGRAPH.CENTER)

doc.save('/home/user/SL_Post_Captions_and_Hashtags.docx')
print('saved')
