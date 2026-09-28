"""Spruce Pro statics v3 — UNIQUE real photo per card, cinematic frosted blend."""
import sys; sys.path.insert(0, '/home/user/spruce')
from templates import *
from spruce_kit import *
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os

P = f'{ROOT}/assets/photos/sp_real2'
PP = f'{ROOT}/assets/photos/sp_real'
OUT = f'{ROOT}/deliverables/spruce_pro'

def grime(im):
    """convincing 'dirty' version: desaturate, darken, algae tint, streaks"""
    im = im.convert('RGBA')
    im = ImageEnhance.Color(im).enhance(0.5)
    im = ImageEnhance.Brightness(im).enhance(0.74)
    im = ImageEnhance.Contrast(im).enhance(0.9)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    w, h = im.size
    for y in range(h):
        t = y / h
        a = int(70 * (0.5 + 0.5 * abs(t - 0.42) * 1.7))
        d.line([(0, y), (w, y)], fill=(96, 110, 48, a))
    import random
    rnd = random.Random(5)
    for _ in range(60):
        x = rnd.randint(0, w)
        ln = rnd.randint(h // 6, h // 2)
        y0 = rnd.choice([0, rnd.randint(0, h // 3)])
        wd = rnd.randint(2, 10)
        d.line([(x, y0), (x - rnd.randint(-30, 30), y0 + ln)], fill=(62, 72, 32, rnd.randint(30, 66)), width=wd)
    ov = ov.filter(ImageFilter.GaussianBlur(3))
    return Image.alpha_composite(im, ov)

if not os.path.exists(f'{PP}/before_grime.jpg'):
    grime(Image.open(f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg')).convert('RGB').save(f'{PP}/before_grime.jpg', quality=92)
    print('grime before created')

def both(name, fn_sq, fn_st):
    save(fn_sq, f'{OUT}/feed/{name}_feed.jpg')
    save(fn_st, f'{OUT}/story/{name}_story.jpg')
    print('ok', name)

# 01 — white porch home
both('SP_01_fall_refresh',
    hero(SP, SQ, f'{P}/sp_13_olutions-residential-background-190.jpg', 'Fall Reset Season', 'Bring Your Home Back to New', 'House wash • Windows • Gutters • Concrete — one trusted crew'),
    hero(SP, ST, f'{P}/sp_13_olutions-residential-background-190.jpg', 'Fall Reset Season', 'Bring Your Home Back to New', 'House wash • Windows • Gutters • Concrete — one trusted local crew', badge='Free Quotes'))

# 02 — orange-vest surface clean
both('SP_02_pressure_wash',
    hero(SP, SQ, f'{P}/sp_20_solutions-square-pressure-washing-2.jpg', 'Pressure Washing', 'The Clean Slate Effect', 'Driveways, walkways & patios — restored without damage'),
    hero(SP, ST, f'{P}/sp_20_solutions-square-pressure-washing-2.jpg', 'Pressure Washing', 'The Clean Slate Effect', 'Driveways, walkways & patios — restored the safe way', badge='Satisfying'))

# 03 — before/after pair
both('SP_03_before_after',
    before_after(SP, SQ, f'{PP}/before_grime.jpg', f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', 'The Spruce Difference', 'One Afternoon. Total Renewal.', focus=0.72),
    before_after(SP, ST, f'{PP}/before_grime.jpg', f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', 'The Spruce Difference', 'One Afternoon. Total Renewal.', focus=0.72))

# 04 — truck at estate (heritage)
both('SP_04_serving_since',
    stat(SP, SQ, 'Serving the Carolinas', '2006', 'Ever Since', 'Family-run, licensed & insured, 5-star rated. We protect your biggest investment like it’s our own.', bg_path=f'{P}/sp_23_sure-washing-services-greenville-sc.jpg', cta=True),
    stat(SP, ST, 'Serving the Carolinas', '2006', 'Ever Since', 'Family-run, licensed & insured, 5-star rated. We protect your biggest investment like it’s our own.', bg_path=f'{P}/sp_23_sure-washing-services-greenville-sc.jpg', cta=True))

# 05 — crew portrait w/ wand
both('SP_05_poll',
    poll(SP, SQ, 'Vote below', 'Most satisfying job to watch?', ['Driveway Surface Clean', 'House Soft Wash', 'Window Squeegee', 'Gutter Cleanout'], bg_path=f'{P}/sp_03_Spruce38-scaled-1.jpg'),
    poll(SP, ST, 'Vote below', 'Most satisfying job to watch?', ['Driveway Surface Clean', 'House Soft Wash', 'Window Squeegee', 'Gutter Cleanout'], bg_path=f'{P}/sp_03_Spruce38-scaled-1.jpg'))

# 06 — squeegee macro
both('SP_06_window',
    hero(SP, SQ, f'{P}/sp_21_-solutions-square-window-cleaning-2.jpg', 'Window Cleaning', 'Glass That Disappears', 'Streak-free inside & out — enjoy the fall colors in HD', cta=True),
    hero(SP, ST, f'{P}/sp_21_-solutions-square-window-cleaning-2.jpg', 'Window Cleaning', 'Glass That Disappears', 'Streak-free inside & out — enjoy the fall colors in high definition', cta=True))

# 07 — hand scooping gutter
both('SP_07_gutter',
    hero(SP, SQ, f'{P}/sp_18_-solutions-square-gutter-cleaning-1.jpg', 'Gutter Season Is Here', 'Clear Before the Rain', 'Scoop • Flush • Check — protect your foundation this fall'),
    hero(SP, ST, f'{P}/sp_18_-solutions-square-gutter-cleaning-1.jpg', 'Gutter Season Is Here', 'Clear Before the Rain', 'Scoop • Flush • Check — protect your home before winter weather hits', badge='Fall Priority'))

# 08 — patio wash action (5.0 stars)
both('SP_08_review',
    stat(SP, SQ, 'Top-Rated in Greenville', '5.0', 'Stars on Google', 'On time. On budget. On every detail. See why the Carolinas keeps choosing Spruce — then experience it yourself.', bg_path=f'{P}/sp_12_olutions-residential-background-175.jpg'),
    stat(SP, ST, 'Top-Rated in Greenville', '5.0', 'Stars on Google', 'On time. On budget. On every detail. See why the Carolinas keeps choosing Spruce — then experience it yourself.', bg_path=f'{P}/sp_12_olutions-residential-background-175.jpg'))

# 09 — deck soft wash at lake
both('SP_09_science',
    tip(SP, SQ, 'Pro Knowledge', 'Soft Wash vs. Pressure Wash', 'High pressure on siding forces water behind it and causes damage. Soft washing uses specialized algicides to safely kill algae at the root — the right method for the right surface, every time.', bg_path=f'{P}/sp_06_Spruce58-scaled-1.jpg'),
    tip(SP, ST, 'Pro Knowledge', 'Soft Wash vs. Pressure Wash', 'High pressure on siding forces water behind it and causes permanent damage. Soft washing uses specialized algicides to safely eliminate algae at the root — the right method for the right surface, every single time.', bg_path=f'{P}/sp_06_Spruce58-scaled-1.jpg'))

# 10 — gutter guard install on roof
both('SP_10_gutter_guards',
    hero(SP, SQ, f'{P}/sp_16_s-residential-gutter-installation-1.jpg', 'Buy Once, Never Scoop Again', 'Gutter Guards, Done Right', 'No more ladders, clogs or overflow — professionally fitted'),
    hero(SP, ST, f'{P}/sp_16_s-residential-gutter-installation-1.jpg', 'Buy Once, Never Scoop Again', 'Gutter Guards, Done Right', 'No more ladders, clogs or overflow — professionally fitted to your home', badge='This Month'))

# 11 — tech + truck at stone house
both('SP_11_holiday_prep',
    hero(SP, SQ, f'{P}/sp_04_Spruce56-1.jpg', 'Holiday Guest-Ready', 'Photo-Ready Before They Arrive', 'House wash + windows + walkway = the homecoming your home deserves', cta=True),
    hero(SP, ST, f'{P}/sp_04_Spruce56-1.jpg', 'Holiday Guest-Ready', 'Photo-Ready Before They Arrive', 'House wash + windows + walkway = the homecoming your home deserves', cta=True))

# 12 — commercial glass (BMW Zentrum)
both('SP_12_commercial',
    hero(SP, SQ, f'{P}/sp_10_s-commercial-background-BMW-Zentrum.jpg', 'Property Managers & Owners', 'First Impressions Are Revenue', 'Storefronts • Restaurants • Complexes — scheduled around YOUR hours', cta=True),
    hero(SP, ST, f'{P}/sp_10_s-commercial-background-BMW-Zentrum.jpg', 'Property Managers & Owners', 'First Impressions Are Revenue', 'Storefronts • Restaurants • Complexes — we schedule around YOUR business hours', cta=True))

# 13 — aerial estate roof
both('SP_13_roof',
    tip(SP, SQ, 'Look Up', 'Those Streaks Aren’t Dirt', 'Black roof streaks are algae feeding on your shingles. Our soft-wash roof cleaning removes them safely — adding years to your roof’s life and Instant curb appeal.', bg_path=f'{P}/sp_08_Spruce66-scaled-1.jpg'),
    tip(SP, ST, 'Look Up', 'Those Streaks Aren’t Dirt', 'Black roof streaks are living algae feeding on your shingles. Our soft-wash roof cleaning removes them safely — adding years to your roof’s life and instant curb appeal.', bg_path=f'{P}/sp_08_Spruce66-scaled-1.jpg'))

# 14 — greenville street
both('SP_14_greenville',
    services(SP, SQ, 'Local & Proud', 'We Serve Your Town', ['Greenville • Greer', 'Simpsonville • Mauldin', 'Asheville & Hendersonville NC', 'Charleston & the Grand Strand'], bg_path=f'{P}/sp_17_aning-covid-19-greenville-sc-square.jpg', cta=True),
    services(SP, ST, 'Local & Proud', 'We Serve Your Town', ['Greenville • Greer • Travelers Rest', 'Simpsonville • Mauldin • Powdersville', 'Asheville & Hendersonville, NC', 'Charleston & the Grand Strand, SC'], bg_path=f'{P}/sp_17_aning-covid-19-greenville-sc-square.jpg', cta=True))

# 15 — aerial lake forest
both('SP_15_why_fall',
    tip(SP, SQ, 'Smart Timing', 'Why Wash in the Fall?', 'Mild temperatures are perfect for cleaning solutions. Removing fall mold and pollen NOW prevents winter staining. And your home is guest-ready before the holidays. Win, win, win.', bg_path=f'{P}/sp_14_Spruce64-1-scaled-1.jpg'),
    tip(SP, ST, 'Smart Timing', 'Why Wash in the Fall?', 'Mild temperatures make cleaning solutions work best. Removing fall mold and pollen NOW prevents permanent winter staining. And your home is guest-ready before the holidays. Win, win, win.', bg_path=f'{P}/sp_14_Spruce64-1-scaled-1.jpg'))

# 16 — woman cleaning window
both('SP_16_streak',
    hero(SP, SQ, f'{P}/sp_11_olutions-residential-background-114.jpg', 'We Leave One Streak Only', 'The Clean One Behind the Squeegee', 'Window cleaning so satisfying it should be illegal', cta=True),
    hero(SP, ST, f'{P}/sp_11_olutions-residential-background-114.jpg', 'We Leave One Streak Only', 'The Clean One Behind the Squeegee', 'Window cleaning so satisfying it should be illegal — book yours today', cta=True))

# 17 — crew on commercial glass
both('SP_17_cta',
    cta_card(SP, SQ, 'Let’s Make It Shine', 'Free quotes • Licensed & insured • 18+ years of 5-star service', bg_path=f'{P}/sp_09_-solutions-commercial-background-14.jpg'),
    cta_card(SP, ST, 'Let’s Make It Shine', 'Free quotes • Licensed & insured • 18+ years of 5-star service', bg_path=f'{P}/sp_09_-solutions-commercial-background-14.jpg'))

# 18 — house wash action
both('SP_18_november',
    hero(SP, SQ, f'{P}/sp_22_house-washing-greenville-sc.jpg', 'Hello, November', 'Gutter Season Official', 'October’s leaves are down — make sure they’re not in your gutters', cta=True),
    hero(SP, ST, f'{P}/sp_22_house-washing-greenville-sc.jpg', 'Hello, November', 'Gutter Season Official', 'October’s leaves are down — make sure they’re not sitting in your gutters', cta=True))

# 19 — aerial neighborhood (insured)
both('SP_19_insured',
    stat(SP, SQ, 'Peace of Mind, Built In', '100%', 'Licensed & Insured', 'Every tech trained, every job insured, every surface treated with the right method. Your home is in the safest hands in the Carolinas.', bg_path=f'{P}/sp_02_IMG_0426-scaled-1.jpeg', badge='Zero Risk'),
    stat(SP, ST, 'Peace of Mind, Built In', '100%', 'Licensed & Insured', 'Every tech trained, every job insured, every surface treated with the right method. Your home is in the safest hands in the Carolinas.', bg_path=f'{P}/sp_02_IMG_0426-scaled-1.jpeg', badge='Zero Risk'))

# 20 — balcony house wash (checklist)
both('SP_20_fall_checklist',
    services(SP, SQ, 'The Fall Exterior Checklist', 'Done by Thanksgiving', ['Gutter clean-out & flush', 'House soft wash', 'Windows, inside & out', 'Driveway & walkway restore'], bg_path=f'{P}/sp_05_Spruce57-scaled-1.jpg'),
    services(SP, ST, 'The Fall Exterior Checklist', 'Done by Thanksgiving', ['Gutter clean-out & flush', 'House soft wash', 'Windows, inside & out', 'Driveway & walkway restore', 'Roof streak treatment'], bg_path=f'{P}/sp_05_Spruce57-scaled-1.jpg'))

print('ALL SPRUCE PRO STATIC DONE (v3, unique images)')
