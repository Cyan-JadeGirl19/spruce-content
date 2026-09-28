"""Builds: 30-day content calendar + master download gallery (single-file HTML, inline styles)."""
import os, base64, urllib.parse

ROOT = '/home/user/spruce'
OUT = f'{ROOT}/deliverables'

TEAL = '#00303C'; TEALD = '#002128'; CYAN = '#1CC8D0'; LIME = '#90D000'; RED = '#C82028'; CREAM = '#FAF7F0'

# ------------------------------------------------ content plan (Oct 1–31)
SL_PLAN = [
 (1,  'SL_01_booking_launch',  'Feed + Story',  '🎬 LAUNCH: October booking season is officially OPEN. Custom design, professional install, and we store your lights till next year. Prime slots go first — claim yours today! 🎄', 'Booking / Demand', '9:00 AM'),
 (2,  'SL_03_before_after',    'Reel + Feed',   'POV: You quit renting a ladder and hired Spruce. ✨ Same house. Same zip code. Different universe. Drop a ✨ if you’d come home to this.', 'Transformation', '6:30 PM'),
 (3,  'SL_04_free_service_calls','Feed + Story','Burnt bulb? Weather damage? Not your problem — ever. Every Spruce install includes FREE season-long service calls. Our elves are on standby. 🧑‍🔧', 'Differentiator', '11:00 AM'),
 (4,  'SL_05_process',         'Feed + Story',  'Design ➜ Install ➜ Takedown ➜ Storage. You make one call. We do literally everything else. Here’s the effortless Spruce process. 🌲', 'Education / Process', '10:00 AM'),
 (5,  'SL_07_poll',            'Feed + Story',  'SETTLE IT IN THE COMMENTS 👇 Which lit look wins: roofline glow, wrapped trees, or walkway magic? (Best answer might win a design… 😉)', 'Engagement', '12:00 PM'),
 (6,  'SL_06_services',        'Feed + Story',  'Homes. HOAs. Storefronts. Whole town squares. If it stands still, we’ll make it glow. One call does it all. 🎄✨', 'Service Awareness', '9:30 AM'),
 (7,  'SL_02_review_michelle', 'Feed + Story',  '“Made our house look magical throughout Christmas and New Years.” — Michelle B. ⭐⭐⭐⭐⭐ Thank you for letting us light up your season!', 'Social Proof', '7:00 PM'),
 (8,  'SL_08_halloween_crossover','Story',      'Real ones know: the smartest households book Christmas lights during Halloween week. 🎃➜🎄 Beat the November rush — link in bio.', 'Urgency', '5:00 PM'),
 (9,  'SL_09_why_pro',         'Feed + Story',  'Commercial-grade C7 & C9 lights. Custom-cut for YOUR roofline. Zero ladder tumbles, zero tangled bins, zero half-lit strands. That’s the Spruce standard. 🔧', 'Education', '10:30 AM'),
 (10, 'SL_promo_reel',         'REEL 🎥',       'The house everyone slows down for? Yeah — that can be yours. Full-service holiday lighting: design, install, maintenance, takedown & storage. 🎬 Now booking October.', 'Hero Reel', '6:00 PM'),
 (11, 'SL_10_review_randy',    'Feed + Story',  '“Great team. Showed up and did excellent work. Highly recommend.” — Randy T. ⭐⭐⭐⭐⭐ We treat every home like it’s ours.', 'Social Proof', '1:00 PM'),
 (12, 'SL_12_countdown_nov1',  'Feed + Story',  '📅 PSA: Our November install calendar is already filling. October bookings get first pick of design slots. Don’t spend December on a ladder — spend it by the fire.', 'Urgency', '9:00 AM'),
 (13, 'SL_13_hoa_streets',     'Feed + Story',  'HOA boards & property managers: imagine your whole community glowing this season. 🏘️ Bulk programs = better per-home pricing. DM us for a community quote.', 'B2B', '11:30 AM'),
 (14, 'SL_14_why_october',     'Feed + Story',  'Why book in October? 1️⃣ First pick of dates 2️⃣ Up before family arrives 3️⃣ Zero December scramble. Same price — better spot in line. 💡', 'Education', '9:00 AM'),
 (15, 'SL_15_poll_ladder',     'Feed + Story',  'Honest poll: This December will you be A) on a ladder untangling lights, or B) on the couch with cocoa? ☕ There’s a right answer. 🎄', 'Engagement', '12:00 PM'),
 (16, 'SL_16_tree_wraps',      'Feed + Story',  'Trees that stop traffic. 🌳✨ Our signature trunk-and-branch wrapping turns your yard into the landmark of the block. Ask about tree wraps!', 'Service Feature', '6:30 PM'),
 (17, 'SL_17_review_jan',      'Feed + Story',  '“My trees wrapped in Christmas lights look amazing!! Spruce is awesome — highly, highly recommend!” — Jan H. ⭐⭐⭐⭐⭐', 'Social Proof', '2:00 PM'),
 (18, 'SL_18_october_filling', 'Feed + Story',  '⏳ Booking update: prime October install slots close at month-end. After that it’s November scheduling and a tighter design calendar. Lock yours in now.', 'Urgency', '10:00 AM'),
 (19, 'SL_before_after_reel',  'REEL 🎥',       'Slide into the season ➡️ From everyday to enchanting in one professional install. Tag someone whose house needs this. 👇', 'Hero Reel', '7:00 PM'),
 (20, 'SL_20_halloween_day',   'Feed + Story',  'Happy Halloween, Greenville! 🎃 Candy tonight, twinkle soon. While you hand out Snickers, we’ll be penciling in light designs. Claim your slot!', 'Holiday Moment', '4:00 PM'),
 (21, 'SL_11_griswold',        'Feed + Story',  'Be the favorite neighbor. All the envy, none of the tangles. 😎 We handle every glowing detail — you take the compliments.', 'Fun / Brand', '11:00 AM'),
 (22, 'SL_01_booking_launch',  'Story (re-run)','One month of October left = the best design slots are going fast. This is your sign. 🎄 DM “LIGHTS” and we’ll take it from there.', 'Urgency Re-run', '5:30 PM'),
 (23, 'SL_05_process',         'Story (re-run)','Quick reminder of how easy this is: you call, we design, install, maintain, remove & store. You just… enjoy it. ✨', 'Process Re-run', '9:00 AM'),
 (24, 'SL_06_services',        'Story (re-run)','Residential • Commercial • Municipal • Garland • Wreaths • Decor — if it’s holiday, we hang it. 🎄', 'Services Re-run', '1:00 PM'),
 (25, 'SL_04_free_service_calls','Story (re-run)','Mid-season bulb outage on Dec 20? Our elves fix it FREE. That’s the Spruce promise. 🧑‍🔧✨', 'Promise Re-run', '3:00 PM'),
 (26, 'SL_promo_feed',         'Feed video 🎥',  'Untangled. Undimmed. Done for you. 🎬 The all-inclusive Spruce holiday lighting experience — now booking.', 'Brand Video', '6:30 PM'),
 (27, 'SL_02_review_michelle', 'Story (re-run)','Magical. That’s the word they use. ⭐⭐⭐⭐⭐ Book your magical at the link in bio.', 'Social Proof', '7:00 PM'),
 (28, 'SL_12_countdown_nov1',  'Feed + Story',  '3 days left in October. ⏱️ The difference between “lit up by Thanksgiving” and “we’ll squeeze you in December” is one quick call.', 'Urgency', '9:30 AM'),
 (29, 'SL_19_cta',             'Feed + Story',  'Last call for October slots! 📞 (864) 288-2459 • Free design consult • Free service calls • Install, removal & storage included.', 'Final Push', '10:00 AM'),
 (30, 'SL_19_cta',             'Story (re-run)','THIS IS IT — October closes tonight. 🎃➜🎄 Secure the season’s best install slots before the calendar flips. Link in bio.', 'Final Push', '6:00 PM'),
 (31, 'SL_18_october_filling', 'Feed + Story',  'Hello November! 👋 For everyone who booked early: your design slot is locked and your crew is scheduled. For everyone else — we’ve got you, just with a tighter calendar. 😉', 'Community', '9:00 AM'),
]

SP_PLAN = [
 (1,  'SP_01_fall_refresh',    'Feed + Story',  '🍂 October in Greenville: leaves fall, grime builds, pollen sticks. Fall is THE season to reset your home’s exterior. Start with a free quote.', 'Seasonal Launch', '9:00 AM'),
 (2,  'SP_02_pressure_wash',   'Feed + Story',  'That line between clean and dirty? Pure satisfaction. 😮 Our surface-clean prep makes driveways look brand new — no streaks, no zebra stripes.', 'Service Feature', '12:00 PM'),
 (3,  'SP_03_before_after',    'Reel + Feed',   '18 years of “wow, that’s the same house?!” Same siding. Same address. One Spruce soft wash. Tag a neighbor who needs this. 👇', 'Transformation', '6:30 PM'),
 (4,  'SP_04_serving_since',   'Feed + Story',  'Serving the Carolinas since 2006. 🏔️ Family-run, licensed & insured, 5-star rated. We don’t just clean homes — we protect your biggest investment.', 'Trust / Heritage', '10:00 AM'),
 (5,  'SP_05_poll',            'Feed + Story',  'Which job is MOST satisfying to watch? 👇 A) Driveway surface clean B) House soft wash C) Window squeegee D) Gutter cleanout. Wrong answers only… kidding. Vote!', 'Engagement', '12:00 PM'),
 (6,  'SP_06_window',          'Feed + Story',  'Streak-free guaranteed — inside & out. 🪟 Enjoy the fall colors through glass that disappears. Book window cleaning with your house wash and save.', 'Service Feature', '11:00 AM'),
 (7,  'SP_07_gutter',          'Feed + Story',  'Clogged gutters = water in places water should never be. 🍁 Fall is gutter season — clear them BEFORE the winter rain hits. We scoop, flush & check.', 'Seasonal Urgency', '9:30 AM'),
 (8,  'SP_08_review',          'Feed + Story',  '⭐⭐⭐⭐⭐ “On time, professional, and my house looks brand new.” Reviews like this are why we’ve served the Upstate since 2006. Thank you!', 'Social Proof', '7:00 PM'),
 (9,  'SP_09_science',         'Feed + Story',  'Soft wash vs. pressure wash: it’s not one-size-fits-all. High pressure on siding = damage. We match the method to the surface — every time. 🧪', 'Education', '10:30 AM'),
 (10, 'SP_promo_reel',         'REEL 🎥',       'Watch 18 years of know-how in 17 seconds. 🎬 House wash • windows • gutters • concrete — one trusted local crew. Free quotes: sprucepro.com', 'Hero Reel', '6:00 PM'),
 (11, 'SP_10_gutter_guards',   'Feed + Story',  'Never scoop leaves again. 🙌 Gutter guards = forever clean gutters, no more ladder weekends, no more clogs. Ask about install pricing this month.', 'Service Feature', '1:00 PM'),
 (12, 'SP_11_holiday_prep',    'Feed + Story',  'Family arriving for the holidays? 🦃 Get the house photo-ready: wash, windows, walkway. October = done before the guests arrive.', 'Seasonal', '9:00 AM'),
 (13, 'SP_12_commercial',      'Feed + Story',  'Property managers & business owners: first impressions are your revenue. 🏢 Storefront, restaurant, complex — one crew, scheduled around YOUR hours.', 'B2B', '11:30 AM'),
 (14, 'SP_02_pressure_wash',   'Story (re-run)','Concrete so clean your neighbors will ask questions. 😎 Free quotes: (864) 483-4300.', 'Service Re-run', '3:00 PM'),
 (15, 'SP_05_poll',            'Story (re-run)','Yesterday’s poll: driveway cleaning won by a landslide. Y’all love a clean driveway. 🛣️ Book yours — link in bio.', 'Engagement Follow-up', '12:00 PM'),
 (16, 'SP_13_roof',            'Feed + Story',  'Those black streaks on your roof aren’t dirt — they’re algae eating your shingles. 🏠 Soft-wash roof cleaning removes them safely and adds years to your roof.', 'Education', '10:00 AM'),
 (17, 'SP_03_before_after',    'Story (re-run)','The split that broke the internet. 🌊 One wash. Zero grime. Free quote in bio.', 'Transformation', '6:30 PM'),
 (18, 'SP_14_greenville',      'Feed + Story',  'Proudly serving Greenville, Greer, Simpsonville, Mauldin, Asheville + more. 📍 Local crew, local pride, 5-star service everywhere we go. Tag your town!', 'Community', '9:30 AM'),
 (19, 'SP_before_after_reel',  'REEL 🎥',       'Wait for the swipe… 😮‍💨 18 years of grime vs. one afternoon. Which half would you rather come home to?', 'Hero Reel', '7:00 PM'),
 (20, 'SP_08_review',          'Story (re-run)','Five stars aren’t a goal — they’re the standard. ⭐ Book the crew the Carolinas trusts.', 'Social Proof', '2:00 PM'),
 (21, 'SP_15_why_fall',        'Feed + Story',  'Why wash in fall? 1️⃣ Mild temps = perfect cleaning weather 2️⃣ Remove fall mold BEFORE it stains 3️⃣ House is holiday-guest ready. Smart homeowners book now.', 'Education', '11:00 AM'),
 (22, 'SP_06_window',          'Story (re-run)','Crystal views of the fall colors start with crystal windows. 🍂🪟 Who’s due for a squeegee?', 'Service Re-run', '1:00 PM'),
 (23, 'SP_09_science',         'Story (re-run)','Soft wash for siding. Pressure for concrete. Right method, right surface — that’s the Spruce difference. 🧪', 'Education', '10:00 AM'),
 (24, 'SP_04_serving_since',   'Story (re-run)','Since 2006 • Licensed & insured • 5-star rated • Family-run. Your home doesn’t deserve a gamble. 🌲', 'Trust Re-run', '9:30 AM'),
 (25, 'SP_10_gutter_guards',   'Story (re-run)','Gutter guards: the “buy once, never think about it again” home upgrade. Ask us this month. 🙌', 'Service Re-run', '3:00 PM'),
 (26, 'SP_promo_feed',         'Feed video 🎥',  'One call. Every exterior surface. Zero hassle. 🎬 See why the Carolinas has trusted Spruce since 2006.', 'Brand Video', '6:30 PM'),
 (27, 'SP_16_streak',          'Feed + Story',  'The only streaks we allow are the ones we leave BEHIND on purpose. 😏 (That’s a squeegee joke. Book your windows.)', 'Fun / Brand', '12:00 PM'),
 (28, 'SP_11_holiday_prep',    'Feed + Story',  'Thanksgiving countdown: 4 weeks. 🦃 House wash + windows + walkway = photo-ready for the whole family. Slots fill fast pre-holiday.', 'Seasonal Urgency', '9:00 AM'),
 (29, 'SP_17_cta',             'Feed + Story',  'October is ending — and so is prime exterior-cleaning weather. 🍂 Lock in your fall refresh: (864) 483-4300 • sprucepro.com • Free quotes.', 'Final Push', '10:00 AM'),
 (30, 'SP_17_cta',             'Story (re-run)','LAST DAY for October scheduling! ⏰ Free quote takes 2 minutes. Clean home takes us one afternoon.', 'Final Push', '5:30 PM'),
 (31, 'SP_18_november',        'Feed + Story',  'Hello November! 🍁 Gutter season is officially here. If your gutters are still full of October… you know who to call. 😉', 'Seasonal', '9:00 AM'),
]

SL_HAS = '#ChristmasLights #HolidayLighting #GreenvilleSC #ChristmasLightInstallation #UpstateSC #HolidayDecor #LightInstallation #ChristmasIsComing #GVL #ShopLocal'
SP_HAS = '#PressureWashing #HouseWashing #WindowCleaning #GutterCleaning #GreenvilleSC #SoftWash #PowerWashing #CurbAppeal #UpstateSC #ShopLocal'

def b64(path, mime='image/jpeg'):
    with open(path, 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()

def thumb64(path, side=320):
    from PIL import Image
    im = Image.open(path).convert('RGB')
    r = side / max(im.size)
    im = im.resize((int(im.width*r), int(im.height*r)), Image.LANCZOS)
    import io
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=72)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

def pick(day, plan):
    for p in plan:
        if p[0] == day: return p
    return None

def calendar_html():
    rows_sl = ''
    rows_sp = ''
    for day in range(1, 32):
        for brand_key, plan, color, accent in (('sl', SL_PLAN, '#0b4b56', CYAN), ('sp', SP_PLAN, '#123a2a', LIME)):
            p = pick(day, plan)
            if not p: continue
            _, asset, fmt, caption, theme, time = p
            base = ('spruce_lights' if brand_key == 'sl' else 'spruce_pro')
            # find asset file
            img = ''
            for sub in ('story', 'feed'):
                cnd = f'{OUT}/{base}/{sub}/{asset}_{sub}.jpg'
                if os.path.exists(cnd):
                    img = thumb64(cnd, 200); break
            vid = ''
            vdir = f'{ROOT}/videos/{base}'
            if os.path.isdir(vdir):
                for v in sorted(os.listdir(vdir)):
                    if asset.split('_')[0] in v or asset in v: pass
            # simpler: map video assets manually below
            row = f'''
            <tr>
              <td class="day">{day}</td>
              <td><img src="{img}" onerror="this.style.visibility='hidden'"><div class="asset">{asset}</div></td>
              <td><span class="fmt">{fmt}</span></td>
              <td class="cap">{caption}</td>
              <td><span class="theme">{theme}</span></td>
              <td class="time">{time}</td>
            </tr>'''
            if brand_key == 'sl': rows_sl += row
            else: rows_sp += row
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Spruce — October 2026 Content Calendar</title>
    <style>
      body{{margin:0;font-family:Segoe UI,Arial,sans-serif;background:#0a2228;color:#eef4f4}}
      header{{background:linear-gradient(120deg,{TEAL},{TEALD});padding:36px 42px;border-bottom:4px solid {CYAN}}}
      h1{{margin:0;font-size:30px;letter-spacing:.5px}} h1 span{{color:{CYAN}}}
      header p{{color:#9fc3c6;margin:8px 0 0}}
      .wrap{{padding:26px 42px}}
      h2{{margin:38px 0 6px;font-size:22px}} h2.lights{{color:{CYAN}}} h2.pro{{color:{LIME}}}
      .sub{{color:#8fb5b8;font-size:13.5px;margin-bottom:14px}}
      table{{border-collapse:collapse;width:100%;font-size:13px}}
      th{{text-align:left;background:#0e3742;color:#bfe2e4;padding:9px 10px;font-size:12px;text-transform:uppercase;letter-spacing:.8px;position:sticky;top:0}}
      td{{padding:10px;border-bottom:1px solid #12414d;vertical-align:top}}
      td.day{{font-size:20px;font-weight:800;color:{CYAN};width:44px}}
      tr.pro_row td.day{{color:{LIME}}}
      td img{{width:74px;border-radius:8px;display:block;margin-bottom:4px;background:#123}}
      .asset{{font-size:10.5px;color:#7fa9ad;max-width:110px;word-break:break-all}}
      .fmt{{background:#0e3742;padding:3px 9px;border-radius:20px;font-size:11px;color:#cfe9ea;white-space:nowrap}}
      .cap{{max-width:520px;line-height:1.45}}
      .theme{{font-size:11px;color:#9fc3c6;white-space:nowrap}}
      .time{{color:{LIME};font-weight:600;white-space:nowrap}}
      .hashtags{{background:#0e3742;border-left:4px solid {LIME};padding:14px 18px;margin:8px 0 26px;font-size:13px;border-radius:0 10px 10px 0;color:#cfe9ea}}
      .note{{background:#123;padding:14px 18px;border-radius:10px;font-size:13px;color:#bfe2e4;margin:10px 0 30px;border:1px solid #155}}
    </style></head><body>
    <header><h1>🎄 SPRUCE — October 2026 Social Content Calendar</h1>
    <p>Spruce Holiday Lighting &amp; Events • Spruce Services &amp; Solutions — 31 days, 2 brands, every asset designed &amp; delivered.</p></header>
    <div class="wrap">
    <div class="note"><b>Posting strategy:</b> Feed posts 4–5×/week per brand, Stories daily on active days, Reels at 6–7 PM (peak local scroll). Engagement posts (polls) at lunch. All CTAs link to the quote forms on sprucelights.com / sprucepro.com. Assets marked (re-run) reuse an earlier graphic in Stories — free reach, zero extra production.</div>

    <h2 class="lights">Spruce Holiday Lighting &amp; Events — @spruceholidaylighting</h2>
    <div class="hashtags">{SL_HAS}</div>
    <table><tr><th>Date</th><th>Asset</th><th>Format</th><th>Caption</th><th>Purpose</th><th>Time (ET)</th></tr>{rows_sl}</table>

    <h2 class="pro">Spruce Services &amp; Solutions — @spruce_pro</h2>
    <div class="hashtags">{SP_HAS}</div>
    <table><tr><th>Date</th><th>Asset</th><th>Format</th><th>Caption</th><th>Purpose</th><th>Time (ET)</th></tr>{rows_sp}</table>
    </div></body></html>'''

def gallery_html():
    def block(base, brand, title, accent, video_files):
        cards = ''
        d = f'{OUT}/{base}'
        feed = sorted(os.listdir(f'{d}/feed')); story = sorted(os.listdir(f'{d}/story'))
        names = [f.rsplit('_feed', 1)[0] for f in feed]
        for n in names:
            fimg = f'{d}/feed/{n}_feed.jpg'; simg = f'{d}/story/{n}_story.jpg'
            ftag = f'<div class="thumbs"><a href="file://{fimg}" download><img src="{thumb64(fimg,300)}"></a><span>Feed 1080×1080</span></div>'
            stag = ''
            if os.path.exists(simg):
                stag = f'<div class="thumbs"><a href="file://{simg}" download><img src="{thumb64(simg,150)}"></a><span>Story 1080×1920</span></div>'
            cards += f'<div class="card"><h4>{n.replace("_"," ").title().replace("Sl ","SL ").replace("Sp ","SP ")}</h4><div class="pair">{ftag}{stag}</div></div>'
        vids = ''
        for v, label, dur in video_files:
            p = f'{ROOT}/videos/{base}/{v}'
            if os.path.exists(p):
                vids += f'''<div class="vcard"><video controls preload="metadata" poster="">
                  <source src="file://{p}" type="video/mp4"></video>
                  <b>{v}</b><span>{label}</span><span class="dur">{dur}</span></div>'''
        return f'''<h2 style="color:{accent}">{title}</h2><div class="grid">{cards}</div>
        <h3>Videos (fully downloadable MP4 with soundtrack)</h3><div class="vgrid">{vids}</div>'''
    return f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Spruce — Master Asset Gallery</title>
    <style>
      body{{margin:0;font-family:Segoe UI,Arial,sans-serif;background:#081e24;color:#eef4f4;padding-bottom:60px}}
      header{{background:linear-gradient(120deg,{TEAL},{TEALD});padding:36px 42px;border-bottom:4px solid {LIME}}}
      h1{{margin:0;font-size:30px}} h1 span{{color:{LIME}}}
      header p{{color:#9fc3c6;margin:8px 0 0}}
      .wrap{{padding:20px 42px}}
      h2{{margin:30px 0 12px;font-size:22px}} h3{{color:#9fc3c6;margin:34px 0 10px;font-size:16px;text-transform:uppercase;letter-spacing:1px}}
      .grid{{display:flex;flex-wrap:wrap;gap:14px}}
      .card{{background:#0c313a;border:1px solid #14525f;border-radius:14px;padding:12px;width:330px}}
      .card h4{{margin:2px 4px 10px;font-size:13px;color:#bfe2e4;text-transform:capitalize}}
      .pair{{display:flex;gap:10px;align-items:flex-start}}
      .thumbs{{text-align:center}} .thumbs img{{border-radius:8px;display:block}}
      .thumbs span{{font-size:10px;color:#7fa9ad;display:block;margin-top:3px}}
      .vgrid{{display:flex;flex-wrap:wrap;gap:16px}}
      .vcard{{background:#0c313a;border:1px solid #14525f;border-radius:14px;padding:12px;width:300px;display:flex;flex-direction:column;gap:4px;font-size:12px;color:#bfe2e4}}
      .vcard video{{width:100%;border-radius:10px;background:#000}}
      .vcard .dur{{color:{LIME}}}
      .note{{background:#0e3742;padding:14px 18px;border-radius:10px;font-size:13px;margin:14px 0}}
    </style></head><body>
    <header><h1>🎁 SPRUCE — Master Asset <span>Gallery</span></h1>
    <p>Every deliverable: 20 hero designs × 2 formats per brand + 8 motion videos + 31-day calendar. Download anything — everything is production-ready.</p></header>
    <div class="wrap">
    <div class="note">💡 Tip: right-click any image or video → <b>Save as</b> to download at full resolution. Or grab the ZIP packages for everything at once.</div>
    {block('spruce_lights','SL','🎄 Spruce Holiday Lighting &amp; Events', CYAN, [
        ('SL_logo_sting_reel.mp4','Animated logo sting — Reels/Stories intro (5s)','1080×1920 • 5s'),
        ('SL_promo_reel.mp4','Hero promo — Reels/Stories (17s)','1080×1920 • 17s'),
        ('SL_promo_feed.mp4','Hero promo — Feed video (12s)','1080×1080 • 12s'),
        ('SL_before_after_reel.mp4','Before/after wipe reel (8s)','1080×1920 • 8s'),
    ])}
    {block('spruce_pro','SP','🧼 Spruce Services &amp; Solutions', LIME, [
        ('SP_logo_sting_reel.mp4','Animated logo sting — Reels/Stories intro (5s)','1080×1920 • 5s'),
        ('SP_promo_reel.mp4','Hero promo — Reels/Stories (15s)','1080×1920 • 15s'),
        ('SP_promo_feed.mp4','Hero promo — Feed video (11s)','1080×1080 • 11s'),
        ('SP_before_after_reel.mp4','Before/after wipe reel (8s)','1080×1920 • 8s'),
    ])}
    </div></body></html>'''

if __name__ == '__main__':
    with open(f'{OUT}/SPRUCE_Oct2026_Content_Calendar.html', 'w') as f:
        f.write(calendar_html())
    with open(f'{OUT}/SPRUCE_Master_Asset_Gallery.html', 'w') as f:
        f.write(gallery_html())
    print('calendar + gallery written')
