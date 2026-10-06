"""Spruce Lights statics v4 — PHOTO-FIRST (client: no blocks, minimal writing)."""
import sys; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
from templates_photo import *
from spruce_kit import *

BG = f'{ROOT}/assets/bg'
SLR = f'{ROOT}/assets/photos/sl_real'
OUT = f'{ROOT}/deliverables/spruce_lights'

def both(name, fn_sq, fn_st):
    save(fn_sq, f'{OUT}/feed/{name}_feed.jpg')
    save(fn_st, f'{OUT}/story/{name}_story.jpg')
    print('ok', name)

both("SL_01_booking_launch", photo_post(SL, SQ, f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Your Home, Aglow All Season Long', kicker='Now Booking October', sub='sprucelights.com'),
     photo_post(SL, ST, f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Your Home, Aglow All Season Long', kicker='Now Booking October', sub='sprucelights.com'))
both('SL_02_review_michelle',
     photo_post(SL, SQ, f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg', '“Made our house look magical”', kicker='★★★★★ Google Review', sub='Michelle B. · Greenville, SC'),
     photo_post(SL, ST, f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg', '“Made our house look magical”', kicker='★★★★★ Google Review', sub='Michelle B. · Greenville, SC'))
both('SL_03_before_after',
     before_after(SL, SQ, f'{BG}/sl_day.jpg', f'{BG}/sl_night_v2.jpg', 'The Spruce Difference', 'From Everyday to Enchanting'),
     before_after(SL, ST, f'{BG}/sl_day.jpg', f'{BG}/sl_night_v2.jpg', 'The Spruce Difference', 'From Everyday to Enchanting'))
both('SL_04_free_service_calls',
     photo_post(SL, SQ, f'{SLR}/sl_17_hting-installation-municipalities-4.jpg', '100% Free Service Calls, All Season', kicker='The Spruce Promise'),
     photo_post(SL, ST, f'{SLR}/sl_17_hting-installation-municipalities-4.jpg', '100% Free Service Calls, All Season', kicker='The Spruce Promise'))
both('SL_05_process',
     photo_post(SL, SQ, f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg', 'Design • Install • Store. You Never Touch a Ladder.', kicker='The Spruce Process'),
     photo_post(SL, ST, f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg', 'Design • Install • Store. You Never Touch a Ladder.', kicker='The Spruce Process'))
both('SL_06_services',
     photo_post(SL, SQ, f'{SLR}/sl_16_hting-installation-municipalities-3.jpg', 'Homes • Businesses • Towns', kicker='All-Inclusive Holiday Lighting'),
     photo_post(SL, ST, f'{SLR}/sl_16_hting-installation-municipalities-3.jpg', 'Homes • Businesses • Towns', kicker='All-Inclusive Holiday Lighting'))
both('SL_07_poll',
     photo_post(SL, SQ, f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg', 'Which Lit Look Wins? Comment Below', kicker='Rooflines • Trees • Walkways'),
     photo_post(SL, ST, f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg', 'Which Lit Look Wins? Comment Below', kicker='Rooflines • Trees • Walkways'))
both('SL_08_halloween_crossover',
     photo_post(SL, SQ, f'{BG}/sl_halloween.jpg', 'Trick or Treat Tonight. Twinkle by December.', kicker='Halloween → Christmas'),
     photo_post(SL, ST, f'{BG}/sl_halloween.jpg', 'Trick or Treat Tonight. Twinkle by December.', kicker='Halloween → Christmas'))
both('SL_09_why_pro',
     photo_post(SL, SQ, f'{BG}/sl_hands.jpg', 'Commercial-Grade Lights. Zero Ladders.', kicker='Good to Know'),
     photo_post(SL, ST, f'{BG}/sl_hands.jpg', 'Commercial-Grade Lights. Zero Ladders.', kicker='Good to Know'))
both('SL_10_review_randy',
     photo_post(SL, SQ, f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg', '“Great team. Excellent work.”', kicker='★★★★★ Google Review', sub='Randy T. · Upstate, SC'),
     photo_post(SL, ST, f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg', '“Great team. Excellent work.”', kicker='★★★★★ Google Review', sub='Randy T. · Upstate, SC'))
both('SL_11_griswold',
     photo_post(SL, SQ, f'{BG}/sl_sleigh.jpg', 'All the Envy. None of the Tangles.', kicker='Be the Favorite House'),
     photo_post(SL, ST, f'{BG}/sl_sleigh.jpg', 'All the Envy. None of the Tangles.', kicker='Be the Favorite House'))
both('SL_12_countdown_nov1',
     photo_post(SL, SQ, f'{SLR}/sl_14_hting-installation-municipalities-1.jpg', 'Prime Slots Fill First — Book October', kicker='Install Calendar'),
     photo_post(SL, ST, f'{SLR}/sl_14_hting-installation-municipalities-1.jpg', 'Prime Slots Fill First — Book October', kicker='Install Calendar'))
both('SL_13_hoa_streets',
     photo_post(SL, SQ, f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'Light Up the Whole Street', kicker='HOAs • Businesses • Towns'),
     photo_post(SL, ST, f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'Light Up the Whole Street', kicker='HOAs • Businesses • Towns'))
both('SL_14_why_october',
     photo_post(SL, SQ, f'{BG}/sl_farmhouse.jpg', 'Smart Homeowners Book in October', kicker='Pro Tip', sub='Same price — better slot'),
     photo_post(SL, ST, f'{BG}/sl_farmhouse.jpg', 'Smart Homeowners Book in October', kicker='Pro Tip', sub='Same price — better slot'))
both('SL_15_poll_ladder',
     photo_post(SL, SQ, f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', 'Ladder This Weekend, or Cocoa? 🎄', kicker='Honest Poll'),
     photo_post(SL, ST, f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', 'Ladder This Weekend, or Cocoa? 🎄', kicker='Honest Poll'))
both('SL_16_tree_wraps',
     photo_post(SL, SQ, f'{BG}/sl_tree.jpg', 'Trees That Stop Traffic', kicker='Signature Spruce Service'),
     photo_post(SL, ST, f'{BG}/sl_tree.jpg', 'Trees That Stop Traffic', kicker='Signature Spruce Service'))
both('SL_17_review_jan',
     photo_post(SL, SQ, f'{SLR}/sl_12_ghting-installation-greenville-sc-3.jpg', '“My wrapped trees look amazing!!”', kicker='★★★★★ Google Review', sub='Jan H. · Greenville, SC'),
     photo_post(SL, ST, f'{SLR}/sl_12_ghting-installation-greenville-sc-3.jpg', '“My wrapped trees look amazing!!”', kicker='★★★★★ Google Review', sub='Jan H. · Greenville, SC'))
both('SL_18_october_filling',
     photo_post(SL, SQ, f'{BG}/sl_roofline.jpg', 'October Slots Almost Gone', kicker='Booking Update'),
     photo_post(SL, ST, f'{BG}/sl_roofline.jpg', 'October Slots Almost Gone', kicker='Booking Update'))
both('SL_19_cta',
     photo_post(SL, SQ, f'{BG}/sl_dock.jpg', 'Let’s Light Up Your Holidays', kicker='Now Booking October', sub='(864) 288-2459'),
     photo_post(SL, ST, f'{BG}/sl_dock.jpg', 'Let’s Light Up Your Holidays', kicker='Now Booking October', sub='(864) 288-2459'))
both('SL_20_halloween_day',
     photo_post(SL, SQ, f'{BG}/sl_garland.jpg', 'Candy Tonight. Twinkle Soon.', kicker='Happy Halloween, Greenville 🎃'),
     photo_post(SL, ST, f'{BG}/sl_garland.jpg', 'Candy Tonight. Twinkle Soon.', kicker='Happy Halloween, Greenville 🎃'))

print('ALL SPRUCE LIGHTS STATIC DONE (v4, photo-first)')
