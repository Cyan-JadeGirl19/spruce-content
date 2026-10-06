"""Spruce Lights statics v4 — PHOTO FIRST (client: no blocks, no heavy writing).
Full-bleed photo + small logo/chip + one short headline line + small contact line."""
import sys; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
import templates_min as _T
for _n in ('TEAL', 'TEAL_D', 'TEAL_L'):
    setattr(_T, _n, getattr(_K, _n))
from templates_min import *
from spruce_kit import *

BG = f'{ROOT}/assets/bg'
SLR = f'{ROOT}/assets/photos/sl_real'
OUT = f'{ROOT}/deliverables/spruce_lights'

def both(name, fn_sq, fn_st):
    save(fn_sq, f'{OUT}/feed/{name}_feed.jpg')
    save(fn_st, f'{OUT}/story/{name}_story.jpg')
    print('ok', name)

both('SL_01_booking_launch',
    hero(SL, SQ, f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Your Home, *Aglow All Season Long*'),
    hero(SL, ST, f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Your Home, *Aglow All Season Long*'))

both('SL_02_review_michelle',
    review(SL, SQ, 'Spruce made our house look magical — easy to work with and a unique, natural look.', 'Michelle B. · Google Review', 'Greenville, SC', bg_path=f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg'),
    review(SL, ST, 'Spruce made our house look magical throughout Christmas and New Years. Easy to work with and a unique, natural look.', 'Michelle B. · Google Review', 'Greenville, SC', bg_path=f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg'))

both('SL_03_before_after',
    before_after(SL, SQ, f'{BG}/sl_day.jpg', f'{BG}/sl_night_v2.jpg', 'The Spruce Difference', 'From Everyday to *Enchanting*'),
    before_after(SL, ST, f'{BG}/sl_day.jpg', f'{BG}/sl_night_v2.jpg', 'The Spruce Difference', 'From Everyday to *Enchanting*'))

both('SL_04_free_service_calls',
    stat(SL, SQ, '100%', 'Free Service Calls All Season', bg_path=f'{SLR}/sl_17_hting-installation-municipalities-4.jpg'),
    stat(SL, ST, '100%', 'Free Service Calls All Season', bg_path=f'{SLR}/sl_17_hting-installation-municipalities-4.jpg'))

both('SL_05_process',
    hero(SL, SQ, f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg', 'We Design, Install & Store — *You Just Enjoy*'),
    hero(SL, ST, f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg', 'We Design, Install & Store — *You Just Enjoy*'))

both('SL_06_services',
    hero(SL, SQ, f'{SLR}/sl_16_hting-installation-municipalities-3.jpg', 'One Call Does It *All*'),
    hero(SL, ST, f'{SLR}/sl_16_hting-installation-municipalities-3.jpg', 'One Call Does It *All*'))

both('SL_07_poll',
    poll(SL, SQ, 'Comment below', 'Which lit look wins?', ['Roofline', 'Wrapped Trees', 'Walkway', 'All of it'], bg_path=f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg', note='Tell us — we might design it for you'),
    poll(SL, ST, 'Comment below', 'Which lit look wins?', ['Roofline', 'Wrapped Trees', 'Walkway', 'All of it'], bg_path=f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg', note='Tell us — we might design it for you'))

both('SL_08_halloween_crossover',
    hero(SL, SQ, f'{BG}/sl_halloween.jpg', 'Trick or Treat Tonight. *Twinkle by December.*'),
    hero(SL, ST, f'{BG}/sl_halloween.jpg', 'Trick or Treat Tonight. *Twinkle by December.*'))

both('SL_09_why_pro',
    hero(SL, SQ, f'{BG}/sl_hands.jpg', 'Commercial-Grade Lights. *Zero Ladder Time.*'),
    hero(SL, ST, f'{BG}/sl_hands.jpg', 'Commercial-Grade Lights. *Zero Ladder Time.*'))

both('SL_10_review_randy',
    review(SL, SQ, 'Great team. Showed up and did excellent work. Highly recommend.', 'Randy T. · Google Review', 'Upstate, SC', bg_path=f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg'),
    review(SL, ST, 'Great team. Showed up and did excellent work. Highly recommend.', 'Randy T. · Google Review', 'Upstate, SC', bg_path=f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg'))

both('SL_11_griswold',
    hero(SL, SQ, f'{BG}/sl_sleigh.jpg', 'All the Envy. *None of the Tangles.*'),
    hero(SL, ST, f'{BG}/sl_sleigh.jpg', 'All the Envy. *None of the Tangles.*'))

both('SL_12_countdown_nov1',
    stat(SL, SQ, 'NOV 1', 'Install Calendar Opens — October Books First', bg_path=f'{BG}/sl_macro.jpg'),
    stat(SL, ST, 'NOV 1', 'Install Calendar Opens — October Books First', bg_path=f'{BG}/sl_macro.jpg'))

both('SL_13_hoa_streets',
    hero(SL, SQ, f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'Light Up the *Whole Street*'),
    hero(SL, ST, f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'Light Up the *Whole Street*'))

both('SL_14_why_october',
    hero(SL, SQ, f'{BG}/sl_farmhouse.jpg', 'Smart Homeowners Book in *October*'),
    hero(SL, ST, f'{BG}/sl_farmhouse.jpg', 'Smart Homeowners Book in *October*'))

both('SL_15_poll_ladder',
    poll(SL, SQ, 'Honest poll', 'Ladder or cocoa this December?', ['On a ladder untangling lights', 'On the couch, sipping cocoa'], bg_path=f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', note='There is a right answer'),
    poll(SL, ST, 'Honest poll', 'Ladder or cocoa this December?', ['On a ladder untangling lights', 'On the couch, sipping cocoa'], bg_path=f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', note='There is a right answer'))

both('SL_16_tree_wraps',
    hero(SL, SQ, f'{BG}/sl_tree.jpg', 'Trees That *Stop Traffic*'),
    hero(SL, ST, f'{BG}/sl_tree.jpg', 'Trees That *Stop Traffic*'))

both('SL_17_review_jan',
    review(SL, SQ, 'My trees wrapped in Christmas lights look amazing!! Spruce is awesome.', 'Jan H. · Google Review', 'Greenville, SC', bg_path=f'{SLR}/sl_14_hting-installation-municipalities-1.jpg'),
    review(SL, ST, 'My trees wrapped in Christmas lights look amazing!! Spruce is awesome — highly, highly recommend!', 'Jan H. · Google Review', 'Greenville, SC', bg_path=f'{SLR}/sl_14_hting-installation-municipalities-1.jpg'))

both('SL_18_october_filling',
    stat(SL, SQ, 'OCT 31', 'Prime October Slots Close at Month-End', bg_path=f'{BG}/sl_roofline.jpg'),
    stat(SL, ST, 'OCT 31', 'Prime October Slots Close at Month-End', bg_path=f'{BG}/sl_roofline.jpg'))

both('SL_19_cta',
    hero(SL, SQ, f'{BG}/sl_dock.jpg', 'Let\u2019s Light Up Your *Holidays*'),
    hero(SL, ST, f'{BG}/sl_dock.jpg', 'Let\u2019s Light Up Your *Holidays*'))

both('SL_20_halloween_day',
    hero(SL, SQ, f'{BG}/sl_garland.jpg', 'Candy Tonight. *Twinkle Soon.*'),
    hero(SL, ST, f'{BG}/sl_garland.jpg', 'Candy Tonight. *Twinkle Soon.*'))

print('ALL SPRUCE LIGHTS STATIC DONE (v4, photo-first)')
