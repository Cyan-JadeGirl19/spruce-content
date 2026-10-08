"""Spruce Pro statics v4 — PHOTO-FIRST (client: no blocks, minimal writing)."""
import sys; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (0, 48, 60, 255); _K.TEAL_D = (0, 33, 42, 255); _K.TEAL_L = (10, 74, 88, 255)
_K.SCRIM_COLOR = (0, 20, 26); _K.FOOT_DARK = (0, 26, 33); _K.CINE_SHADOW = (0.0, 0.10, 0.13)
from templates_photo import *
from spruce_kit import *

P = f'{ROOT}/assets/photos/sp_real2'
SPO = f'{ROOT}/assets/photos/sp_real'
OUT = f'{ROOT}/deliverables/spruce_pro'

def both(name, fn_sq, fn_st):
    save(fn_sq, f'{OUT}/feed/{name}_feed.jpg')
    save(fn_st, f'{OUT}/story/{name}_story.jpg')
    print('ok', name)

both('SP_01_pressure_wash',
     photo_post(SP, SQ, f'{P}/sp_02_hq.jpg', 'Pressure Washing That Transforms', kicker='Driveways • Siding • Patios'),
     photo_post(SP, ST, f'{P}/sp_02_hq.jpg', 'Pressure Washing That Transforms', kicker='Driveways • Siding • Patios'))

both('SP_02_before_after',
     before_after(SP, SQ, f'{SPO}/before_grime.jpg', f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', 'The Spruce Difference', 'From Grime to Gleaming'),
     before_after(SP, ST, f'{SPO}/before_grime.jpg', f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', 'The Spruce Difference', 'From Grime to Gleaming'))

both('SP_03_review',
     photo_post(SP, SQ, f'{P}/sp_12_olutions-residential-background-175.jpg', '“They Left Everything Spotless”', kicker='★★★★★ Google Review'),
     photo_post(SP, ST, f'{P}/sp_12_olutions-residential-background-175.jpg', '“They Left Everything Spotless”', kicker='★★★★★ Google Review'))

both('SP_04_streak',
     photo_post(SP, SQ, f'{P}/sp_11_olutions-residential-background-114.jpg', 'Streaks Happen. We Fix Them.', kicker='Window Rescue'),
     photo_post(SP, ST, f'{P}/sp_11_olutions-residential-background-114.jpg', 'Streaks Happen. We Fix Them.', kicker='Window Rescue'))

both('SP_05_window',
     photo_post(SP, SQ, f'{P}/sp_06_hq.jpg', 'Streak-Free Windows, Guaranteed', kicker='Window Cleaning'),
     photo_post(SP, ST, f'{P}/sp_06_hq.jpg', 'Streak-Free Windows, Guaranteed', kicker='Window Cleaning'))

both('SP_06_gutter',
     photo_post(SP, SQ, f'{P}/sp_07_hq.jpg', 'Clean Gutters Before the Storms', kicker='Gutter Cleaning'),
     photo_post(SP, ST, f'{P}/sp_07_hq.jpg', 'Clean Gutters Before the Storms', kicker='Gutter Cleaning'))

both('SP_07_gutter_guards',
     photo_post(SP, SQ, f'{P}/sp_16_s-residential-gutter-installation-1.jpg', 'Gutter Guards: Clean Forever', kicker='One Install. Zero Scooping.'),
     photo_post(SP, ST, f'{P}/sp_16_s-residential-gutter-installation-1.jpg', 'Gutter Guards: Clean Forever', kicker='One Install. Zero Scooping.'))

both('SP_08_roof',
     photo_post(SP, SQ, f'{P}/sp_08_Spruce66-scaled-1.jpg', 'Roof Cleaning Without the Damage', kicker='SoftWash Only'),
     photo_post(SP, ST, f'{P}/sp_08_Spruce66-scaled-1.jpg', 'Roof Cleaning Without the Damage', kicker='SoftWash Only'))

both('SP_09_fall_refresh',
     photo_post(SP, SQ, f'{P}/sp_13_olutions-residential-background-190.jpg', 'Fall Refresh — Before the Holidays', kicker='Exterior Cleaning'),
     photo_post(SP, ST, f'{P}/sp_13_olutions-residential-background-190.jpg', 'Fall Refresh — Before the Holidays', kicker='Exterior Cleaning'))

both('SP_10_commercial',
     photo_post(SP, SQ, f'{P}/sp_10_s-commercial-background-BMW-Zentrum.jpg', 'Commercial Exteriors, Handled', kicker='Storefronts • Campus • Fleet'),
     photo_post(SP, ST, f'{P}/sp_10_s-commercial-background-BMW-Zentrum.jpg', 'Commercial Exteriors, Handled', kicker='Storefronts • Campus • Fleet'))

both('SP_11_serving_since',
     photo_post(SP, SQ, f'{P}/sp_23_sure-washing-services-greenville-sc.jpg', 'Serving the Upstate Since 2006', kicker='Licensed & Insured'),
     photo_post(SP, ST, f'{P}/sp_23_sure-washing-services-greenville-sc.jpg', 'Serving the Upstate Since 2006', kicker='Licensed & Insured'))

both('SP_12_insured',
     photo_post(SP, SQ, f'{P}/sp_02_IMG_0426-scaled-1.jpeg', 'Licensed, Insured, Since 2006', kicker='Peace of Mind'),
     photo_post(SP, ST, f'{P}/sp_02_IMG_0426-scaled-1.jpeg', 'Licensed, Insured, Since 2006', kicker='Peace of Mind'))

both('SP_13_science',
     photo_post(SP, SQ, f'{P}/sp_06_Spruce58-scaled-1.jpg', 'The Right Pressure. The Right Mix.', kicker='SoftWash Science'),
     photo_post(SP, ST, f'{P}/sp_06_Spruce58-scaled-1.jpg', 'The Right Pressure. The Right Mix.', kicker='SoftWash Science'))

both('SP_14_greenville',
     photo_post(SP, SQ, f'{P}/sp_01_Copy-of-IMG_51831-conv-scaled-1.jpeg', 'Greenville’s Exterior Cleaning Pros', kicker='Locally Owned'),
     photo_post(SP, ST, f'{P}/sp_01_Copy-of-IMG_51831-conv-scaled-1.jpeg', 'Greenville’s Exterior Cleaning Pros', kicker='Locally Owned'))

both('SP_15_why_fall',
     photo_post(SP, SQ, f'{P}/sp_14_Spruce64-1-scaled-1.jpg', 'Why Fall Is Washing Season', kicker='Pro Tip', sub='Beat the winter grime'),
     photo_post(SP, ST, f'{P}/sp_14_Spruce64-1-scaled-1.jpg', 'Why Fall Is Washing Season', kicker='Pro Tip', sub='Beat the winter grime'))

both('SP_16_fall_checklist',
     photo_post(SP, SQ, f'{P}/sp_05_Spruce57-scaled-1.jpg', 'Your Fall Exterior Checklist', kicker='Wash • Windows • Gutters'),
     photo_post(SP, ST, f'{P}/sp_05_Spruce57-scaled-1.jpg', 'Your Fall Exterior Checklist', kicker='Wash • Windows • Gutters'))

both('SP_17_november',
     photo_post(SP, SQ, f'{P}/sp_22_house-washing-greenville-sc.jpg', 'November Slots Open Now', kicker='Booking Update'),
     photo_post(SP, ST, f'{P}/sp_22_house-washing-greenville-sc.jpg', 'November Slots Open Now', kicker='Booking Update'))

both('SP_18_holiday_prep',
     photo_post(SP, SQ, f'{P}/sp_04_Spruce56-1.jpg', 'Get Guest-Ready Before They Arrive', kicker='Holiday Prep'),
     photo_post(SP, ST, f'{P}/sp_04_Spruce56-1.jpg', 'Get Guest-Ready Before They Arrive', kicker='Holiday Prep'))

both('SP_19_poll',
     photo_post(SP, SQ, f'{P}/sp_03_Spruce38-scaled-1.jpg', 'Driveway or House First? Comment Below', kicker='This Weekend'),
     photo_post(SP, ST, f'{P}/sp_03_Spruce38-scaled-1.jpg', 'Driveway or House First? Comment Below', kicker='This Weekend'))

both('SP_20_cta',
     photo_post(SP, SQ, f'{P}/sp_09_-solutions-commercial-background-14.jpg', 'Let’s Get Your Home Spruced Up', kicker='Free Quotes', sub='(864) 483-4300'),
     photo_post(SP, ST, f'{P}/sp_09_-solutions-commercial-background-14.jpg', 'Let’s Get Your Home Spruced Up', kicker='Free Quotes', sub='(864) 483-4300'))

print('ALL SPRUCE PRO STATIC DONE (v4, photo-first)')
