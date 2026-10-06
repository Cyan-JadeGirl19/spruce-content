"""Spruce Pro statics v4 — PHOTO FIRST (client: no blocks, no heavy writing)."""
import sys; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (0, 48, 60, 255); _K.TEAL_D = (0, 33, 42, 255); _K.TEAL_L = (10, 74, 88, 255)
_K.SCRIM_COLOR = (0, 20, 26); _K.FOOT_DARK = (0, 26, 33); _K.CINE_SHADOW = (0.00, 0.10, 0.13)
import templates_min as _T
for _n in ('TEAL', 'TEAL_D', 'TEAL_L'):
    setattr(_T, _n, getattr(_K, _n))
from templates_min import *
from spruce_kit import *

P = f'{ROOT}/assets/photos/sp_real2'
PP = f'{ROOT}/assets/photos/sp_real'
OUT = f'{ROOT}/deliverables/spruce_pro'

def both(name, fn_sq, fn_st):
    save(fn_sq, f'{OUT}/feed/{name}_feed.jpg')
    save(fn_st, f'{OUT}/story/{name}_story.jpg')
    print('ok', name)

both('SP_01_fall_refresh',
    hero(SP, SQ, f'{P}/sp_13_olutions-residential-background-190.jpg', 'Bring Your Home Back to *New*'),
    hero(SP, ST, f'{P}/sp_13_olutions-residential-background-190.jpg', 'Bring Your Home Back to *New*'))

both('SP_02_pressure_wash',
    hero(SP, SQ, f'{P}/sp_20_solutions-square-pressure-washing-2.jpg', 'The Clean Slate *Effect*'),
    hero(SP, ST, f'{P}/sp_20_solutions-square-pressure-washing-2.jpg', 'The Clean Slate *Effect*'))

both('SP_03_before_after',
    before_after(SP, SQ, f'{PP}/before_grime.jpg', f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', 'The Spruce Difference', 'One Afternoon. *Total Renewal.*', focus=0.72),
    before_after(SP, ST, f'{PP}/before_grime.jpg', f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', 'The Spruce Difference', 'One Afternoon. *Total Renewal.*', focus=0.72))

both('SP_04_serving_since',
    stat(SP, SQ, '2006', 'Serving the Carolinas — Family-Run Ever Since', bg_path=f'{P}/sp_23_sure-washing-services-greenville-sc.jpg'),
    stat(SP, ST, '2006', 'Serving the Carolinas — Family-Run Ever Since', bg_path=f'{P}/sp_23_sure-washing-services-greenville-sc.jpg'))

both('SP_05_poll',
    poll(SP, SQ, 'Vote below', 'Most satisfying job to watch?', ['Driveway Clean', 'House Wash', 'Windows', 'Gutters'], bg_path=f'{P}/sp_03_Spruce38-scaled-1.jpg'),
    poll(SP, ST, 'Vote below', 'Most satisfying job to watch?', ['Driveway Clean', 'House Wash', 'Windows', 'Gutters'], bg_path=f'{P}/sp_03_Spruce38-scaled-1.jpg'))

both('SP_06_window',
    hero(SP, SQ, f'{P}/sp_21_-solutions-square-window-cleaning-2.jpg', 'Glass That *Disappears*'),
    hero(SP, ST, f'{P}/sp_21_-solutions-square-window-cleaning-2.jpg', 'Glass That *Disappears*'))

both('SP_07_gutter',
    hero(SP, SQ, f'{P}/sp_18_-solutions-square-gutter-cleaning-1.jpg', 'Clear Before the *Rain*'),
    hero(SP, ST, f'{P}/sp_18_-solutions-square-gutter-cleaning-1.jpg', 'Clear Before the *Rain*'))

both('SP_08_review',
    stat(SP, SQ, '5.0', 'Stars on Google — Top-Rated in Greenville', bg_path=f'{P}/sp_12_olutions-residential-background-175.jpg'),
    stat(SP, ST, '5.0', 'Stars on Google — Top-Rated in Greenville', bg_path=f'{P}/sp_12_olutions-residential-background-175.jpg'))

both('SP_09_science',
    hero(SP, SQ, f'{P}/sp_06_Spruce58-scaled-1.jpg', 'The *Right* Method for Every Surface'),
    hero(SP, ST, f'{P}/sp_06_Spruce58-scaled-1.jpg', 'The *Right* Method for Every Surface'))

both('SP_10_gutter_guards',
    hero(SP, SQ, f'{P}/sp_16_s-residential-gutter-installation-1.jpg', 'Gutter Guards, Done *Right*'),
    hero(SP, ST, f'{P}/sp_16_s-residential-gutter-installation-1.jpg', 'Gutter Guards, Done *Right*'))

both('SP_11_holiday_prep',
    hero(SP, SQ, f'{P}/sp_04_Spruce56-1.jpg', 'Photo-Ready Before They *Arrive*'),
    hero(SP, ST, f'{P}/sp_04_Spruce56-1.jpg', 'Photo-Ready Before They *Arrive*'))

both('SP_12_commercial',
    hero(SP, SQ, f'{P}/sp_10_s-commercial-background-BMW-Zentrum.jpg', 'First Impressions Are *Revenue*'),
    hero(SP, ST, f'{P}/sp_10_s-commercial-background-BMW-Zentrum.jpg', 'First Impressions Are *Revenue*'))

both('SP_13_roof',
    hero(SP, SQ, f'{P}/sp_08_Spruce66-scaled-1.jpg', 'Those Streaks Aren\u2019t *Dirt*'),
    hero(SP, ST, f'{P}/sp_08_Spruce66-scaled-1.jpg', 'Those Streaks Aren\u2019t *Dirt*'))

both('SP_14_greenville',
    hero(SP, SQ, f'{P}/sp_17_aning-covid-19-greenville-sc-square.jpg', 'Local & Proud — *We Serve Your Town*'),
    hero(SP, ST, f'{P}/sp_17_aning-covid-19-greenville-sc-square.jpg', 'Local & Proud — *We Serve Your Town*'))

both('SP_15_why_fall',
    hero(SP, SQ, f'{P}/sp_14_Spruce64-1-scaled-1.jpg', 'Why Smart Owners Wash in *Fall*'),
    hero(SP, ST, f'{P}/sp_14_Spruce64-1-scaled-1.jpg', 'Why Smart Owners Wash in *Fall*'))

both('SP_16_streak',
    hero(SP, SQ, f'{P}/sp_11_olutions-residential-background-114.jpg', 'We Leave One Streak *Only*'),
    hero(SP, ST, f'{P}/sp_11_olutions-residential-background-114.jpg', 'We Leave One Streak *Only*'))

both('SP_17_cta',
    hero(SP, SQ, f'{P}/sp_09_-solutions-commercial-background-14.jpg', 'Let\u2019s Make It *Shine*'),
    hero(SP, ST, f'{P}/sp_09_-solutions-commercial-background-14.jpg', 'Let\u2019s Make It *Shine*'))

both('SP_18_november',
    hero(SP, SQ, f'{P}/sp_22_house-washing-greenville-sc.jpg', 'Hello November — *Gutter Season*'),
    hero(SP, ST, f'{P}/sp_22_house-washing-greenville-sc.jpg', 'Hello November — *Gutter Season*'))

both('SP_19_insured',
    stat(SP, SQ, '100%', 'Licensed & Insured — Every Job, Every Tech', bg_path=f'{P}/sp_02_IMG_0426-scaled-1.jpeg'),
    stat(SP, ST, '100%', 'Licensed & Insured — Every Job, Every Tech', bg_path=f'{P}/sp_02_IMG_0426-scaled-1.jpeg'))

both('SP_20_fall_checklist',
    hero(SP, SQ, f'{P}/sp_05_Spruce57-scaled-1.jpg', 'The Fall Checklist — *Done by Thanksgiving*'),
    hero(SP, ST, f'{P}/sp_05_Spruce57-scaled-1.jpg', 'The Fall Checklist — *Done by Thanksgiving*'))

print('ALL SPRUCE PRO STATIC DONE (v4, photo-first)')
