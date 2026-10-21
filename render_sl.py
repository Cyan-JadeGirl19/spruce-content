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

both("SL_01_booking_launch", photo_post(SL, SQ, f'{BG}/sl_mansion_sq.jpg', 'Your Home, Aglow All Season Long', kicker='Now Booking October', sub='sprucelights.com'),
     photo_post(SL, ST, f'{BG}/sl_mansion_sq.jpg', 'Your Home, Aglow All Season Long', kicker='Now Booking October', sub='sprucelights.com'))
both('SL_02_review_michelle',
     photo_post(SL, SQ, f'{SLR}/sl_10_v2.jpg', '“Made our house look magical”', kicker='★★★★★ Google Review', sub='Michelle B. · Greenville, SC'),
     photo_post(SL, ST, f'{SLR}/sl_10_v2.jpg', '“Made our house look magical”', kicker='★★★★★ Google Review', sub='Michelle B. · Greenville, SC'))
both('SL_03_before_after',
     before_after(SL, SQ, f'{BG}/sl_day.jpg', f'{BG}/sl_night_v3.jpg', 'The Spruce Difference', 'From Everyday to Enchanting'),
     before_after(SL, ST, f'{BG}/sl_day.jpg', f'{BG}/sl_night_v3.jpg', 'The Spruce Difference', 'From Everyday to Enchanting'))
both('SL_04_free_service_calls',
     photo_post(SL, SQ, f'{SLR}/sl_04_corner_sq.jpg', '100% Free Service Calls, All Season', kicker='The Spruce Promise'),
     photo_post(SL, ST, f'{SLR}/sl_04_corner_sq.jpg', '100% Free Service Calls, All Season', kicker='The Spruce Promise'))
both('SL_05_process',
     photo_post(SL, SQ, f'{SLR}/sl_05_installer_sq.jpg', 'Design • Install • Store. You Never Touch a Ladder.', kicker='The Spruce Process'),
     photo_post(SL, ST, f'{SLR}/sl_05_installer_sq.jpg', 'Design • Install • Store. You Never Touch a Ladder.', kicker='The Spruce Process'))
both('SL_06_services',
     photo_post(SL, SQ, f'{BG}/sl_06_street_sq.jpg', 'Homes • Businesses • Towns', kicker='All-Inclusive Holiday Lighting'),
     photo_post(SL, ST, f'{BG}/sl_06_street_sq.jpg', 'Homes • Businesses • Towns', kicker='All-Inclusive Holiday Lighting'))
both('SL_07_poll',
     photo_post(SL, SQ, f'{SLR}/sl_06_v2.jpg', 'Which Lit Look Wins? Comment Below', kicker='Rooflines • Trees • Walkways'),
     photo_post(SL, ST, f'{SLR}/sl_06_v2.jpg', 'Which Lit Look Wins? Comment Below', kicker='Rooflines • Trees • Walkways'))
both('SL_08_halloween_crossover',
     photo_post(SL, SQ, f'{BG}/sl_halloween_sq.jpg', 'Trick or Treat Tonight. Twinkle by December.', kicker='Halloween → Christmas'),
     photo_post(SL, ST, f'{BG}/sl_halloween_sq.jpg', 'Trick or Treat Tonight. Twinkle by December.', kicker='Halloween → Christmas'))
both('SL_09_why_pro',
     photo_post(SL, SQ, f'{BG}/sl_tunnel_mc.jpg', 'Commercial-Grade Lights. Zero Ladders.', kicker='Good to Know'),
     photo_post(SL, ST, f'{BG}/sl_tunnel_mc.jpg', 'Commercial-Grade Lights. Zero Ladders.', kicker='Good to Know'))
both('SL_10_review_randy',
     photo_post(SL, SQ, f'{SLR}/sl_10_randy_sq.jpg', '“Great team. Excellent work.”', kicker='★★★★★ Google Review', sub='Randy T. · Upstate, SC'),
     photo_post(SL, ST, f'{SLR}/sl_10_randy_sq.jpg', '“Great team. Excellent work.”', kicker='★★★★★ Google Review', sub='Randy T. · Upstate, SC'))
both('SL_11_griswold',
     photo_post(SL, SQ, f'{BG}/sl_11_sleigh_sq.jpg', 'All the Envy. None of the Tangles.', kicker='Be the Favorite House'),
     photo_post(SL, ST, f'{BG}/sl_11_sleigh_sq.jpg', 'All the Envy. None of the Tangles.', kicker='Be the Favorite House'))
both('SL_12_countdown_nov1',
     photo_post(SL, SQ, f'{SLR}/sl_14_hting-installation-municipalities-1.jpg', 'Prime Slots Fill First — Book October', kicker='Install Calendar'),
     photo_post(SL, ST, f'{SLR}/sl_14_hting-installation-municipalities-1.jpg', 'Prime Slots Fill First — Book October', kicker='Install Calendar'))
both('SL_13_hoa_streets',
     photo_post(SL, SQ, f'{BG}/sl_13_gazebo_sq.jpg', 'Light Up the Whole Street', kicker='HOAs • Businesses • Towns'),
     photo_post(SL, ST, f'{BG}/sl_13_gazebo_sq.jpg', 'Light Up the Whole Street', kicker='HOAs • Businesses • Towns'))
both('SL_14_why_october',
     photo_post(SL, SQ, f'{BG}/sl_farmhouse_v2.jpg', 'Smart Homeowners Book in October', kicker='Pro Tip', sub='Same price — better slot'),
     photo_post(SL, ST, f'{BG}/sl_farmhouse_v2.jpg', 'Smart Homeowners Book in October', kicker='Pro Tip', sub='Same price — better slot'))
both('SL_15_poll_ladder',
     photo_post(SL, SQ, f'{SLR}/sl_03_v2.jpg', 'Ladder This Weekend, or Cocoa? 🎄', kicker='Honest Poll'),
     photo_post(SL, ST, f'{SLR}/sl_03_v2.jpg', 'Ladder This Weekend, or Cocoa? 🎄', kicker='Honest Poll'))
both('SL_16_tree_wraps',
     photo_post(SL, SQ, f'{BG}/sl_16_stag_sq.jpg', 'Trees That Stop Traffic', kicker='Signature Spruce Service'),
     photo_post(SL, ST, f'{BG}/sl_16_stag_sq.jpg', 'Trees That Stop Traffic', kicker='Signature Spruce Service'))
both('SL_17_review_jan',
     photo_post(SL, SQ, f'{SLR}/sl_12_ghting-installation-greenville-sc-3.jpg', '“My wrapped trees look amazing!!”', kicker='★★★★★ Google Review', sub='Jan H. · Greenville, SC'),
     photo_post(SL, ST, f'{SLR}/sl_12_ghting-installation-greenville-sc-3.jpg', '“My wrapped trees look amazing!!”', kicker='★★★★★ Google Review', sub='Jan H. · Greenville, SC'))
both('SL_18_october_filling',
     photo_post(SL, SQ, f'{BG}/sl_roofline.jpg', 'October Slots Almost Gone', kicker='Booking Update'),
     photo_post(SL, ST, f'{BG}/sl_roofline.jpg', 'October Slots Almost Gone', kicker='Booking Update'))
both('SL_19_cta',
     photo_post(SL, SQ, f'{BG}/sl_gifts_mc.jpg', 'Let’s Light Up Your Holidays', kicker='Now Booking October', sub='(864) 288-2459'),
     photo_post(SL, ST, f'{BG}/sl_gifts_mc.jpg', 'Let’s Light Up Your Holidays', kicker='Now Booking October', sub='(864) 288-2459'))
both('SL_20_halloween_day',
     photo_post(SL, SQ, f'{BG}/sl_garland.jpg', 'Candy Tonight. Twinkle Soon.', kicker='Happy Halloween, Greenville 🎃'),
     photo_post(SL, ST, f'{BG}/sl_garland.jpg', 'Candy Tonight. Twinkle Soon.', kicker='Happy Halloween, Greenville 🎃'))
both('SL_21_before_after_mansion',
     before_after(SL, SQ, f'{BG}/sl_mansion_day.jpg', f'{BG}/sl_mansion_hero.jpg', 'The Spruce Touch', 'From Ordinary to Extraordinary'),
     before_after(SL, ST, f'{BG}/sl_mansion_day.jpg', f'{BG}/sl_mansion_hero.jpg', 'The Spruce Touch', 'From Ordinary to Extraordinary'))
both('SL_22_before_after_street',
     before_after(SL, SQ, f'{BG}/sl_street_day.jpg', f'{BG}/sl_commercial_mc.jpg', 'Installed Overnight', 'Glow by Morning'),
     before_after(SL, ST, f'{BG}/sl_street_day.jpg', f'{BG}/sl_commercial_mc.jpg', 'Installed Overnight', 'Glow by Morning'))
both('SL_23_before_after_town',
     before_after(SL, SQ, f'{BG}/sl_gazebo_day.jpg', f'{BG}/sl_municipal_mc.jpg', 'Municipal Lighting', 'Your Town, Aglow'),
     before_after(SL, ST, f'{BG}/sl_gazebo_day.jpg', f'{BG}/sl_municipal_mc.jpg', 'Municipal Lighting', 'Your Town, Aglow'))

both('SL_24_yearround_patio',
     photo_post(SL, SQ, f'{BG}/sl_24_patio_sq.jpg', 'Lighting for Every Season', kicker='Year-Round Lighting'),
     photo_post(SL, ST, f'{BG}/sl_24_patio_sq.jpg', 'Lighting for Every Season', kicker='Year-Round Lighting'))
both('SL_25_yearround_pergola',
     photo_post(SL, SQ, f'{BG}/sl_yr_pergola.jpg', 'Your Backyard, All Year Long', kicker='Year-Round Lighting'),
     photo_post(SL, ST, f'{BG}/sl_yr_pergola.jpg', 'Your Backyard, All Year Long', kicker='Year-Round Lighting'))
both('SL_26_yearround_bistro',
     photo_post(SL, SQ, f'{BG}/sl_26_bistro_sq.jpg', 'Ambiance That Pays for Itself', kicker='Year-Round Lighting'),
     photo_post(SL, ST, f'{BG}/sl_26_bistro_sq.jpg', 'Ambiance That Pays for Itself', kicker='Year-Round Lighting'))

both('SL_27_classic_tree_wrap',
     photo_post(SL, SQ, f'{BG}/sl_tree.jpg', 'The Showstopper Tree Wrap', kicker='Signature Spruce Service'),
     photo_post(SL, ST, f'{BG}/sl_tree.jpg', 'The Showstopper Tree Wrap', kicker='Signature Spruce Service'))
both('SL_28_dock_cta',
     photo_post(SL, SQ, f'{BG}/sl_dock.jpg', 'Lake Life, Lit Up', kicker='Now Booking October', sub='(864) 288-2459'),
     photo_post(SL, ST, f'{BG}/sl_dock.jpg', 'Lake Life, Lit Up', kicker='Now Booking October', sub='(864) 288-2459'))

both('SL_29_classic_sleigh',
     photo_post(SL, SQ, f'{BG}/sl_sleigh_v2_sq.jpg', 'All the Envy. None of the Tangles.', kicker='Be the Favorite House'),
     photo_post(SL, ST, f'{BG}/sl_sleigh_v2_st.jpg', 'All the Envy. None of the Tangles.', kicker='Be the Favorite House'))
both('SL_30_classic_halloween',
     photo_post(SL, SQ, f'{BG}/sl_halloween_v2_sq.jpg', 'Trick or Treat Tonight. Twinkle by December.', kicker='Halloween \u2192 Christmas'),
     photo_post(SL, ST, f'{BG}/sl_halloween_v2_sq.jpg', 'Trick or Treat Tonight. Twinkle by December.', kicker='Halloween \u2192 Christmas'))

both('SL_31_authentic_joy',
     photo_post(SL, SQ, f'{SLR}/sl_auth_31_feed.jpg', 'Real Home. Real Spruce Magic.', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_31_story.jpg', 'Real Home. Real Spruce Magic.', kicker='Authentic Spruce Install'))
both('SL_32_authentic_pond',
     photo_post(SL, SQ, f'{SLR}/sl_auth_32_feed.jpg', 'Even the Waterfall Gets Dressed Up', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_32_story.jpg', 'Even the Waterfall Gets Dressed Up', kicker='Authentic Spruce Install'))
both('SL_33_authentic_landscape',
     photo_post(SL, SQ, f'{SLR}/sl_auth_33_feed.jpg', 'Every Level of Your Yard, Lit', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_33_story.jpg', 'Every Level of Your Yard, Lit', kicker='Authentic Spruce Install'))
both('SL_34_authentic_forest',
     photo_post(SL, SQ, f'{SLR}/sl_auth_34_feed.jpg', 'Backyard Creek, Front Yard Wow', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_34_story.jpg', 'Backyard Creek, Front Yard Wow', kicker='Authentic Spruce Install'))
both('SL_35_authentic_trio',
     photo_post(SL, SQ, f'{SLR}/sl_auth_35_feed.jpg', 'Three Trees, One Showstopper Yard', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_35_story.jpg', 'Three Trees, One Showstopper Yard', kicker='Authentic Spruce Install'))

both('SL_36_authentic_roofline',
     photo_post(SL, SQ, f'{SLR}/sl_auth_36_feed.jpg', 'Every Gable. Every Edge.', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_36_story.jpg', 'Every Gable. Every Edge.', kicker='Authentic Spruce Install'))
both('SL_37_authentic_porch',
     photo_post(SL, SQ, f'{SLR}/sl_auth_37_feed.jpg', 'Built for Sitting Out Front', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_37_story.jpg', 'Built for Sitting Out Front', kicker='Authentic Spruce Install'))
both('SL_38_authentic_warmwhite',
     photo_post(SL, SQ, f'{SLR}/sl_auth_38_feed.jpg', 'Warm White Never Misses', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_38_story.jpg', 'Warm White Never Misses', kicker='Authentic Spruce Install'))
both('SL_39_authentic_firstnight',
     photo_post(SL, SQ, f'{SLR}/sl_auth_39_feed.jpg', 'The First Night We Plug It In', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_39_story.jpg', 'The First Night We Plug It In', kicker='Authentic Spruce Install'))
both('SL_40_authentic_trunkwrap',
     photo_post(SL, SQ, f'{SLR}/sl_auth_40_feed.jpg', 'Down to the Last Tree Trunk', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_40_story.jpg', 'Down to the Last Tree Trunk', kicker='Authentic Spruce Install'))
both('SL_41_authentic_bluecanopy',
     photo_post(SL, SQ, f'{SLR}/sl_auth_41_feed.jpg', 'A Waterfall of Blue, Block Wide', kicker='Authentic Commercial Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_41_story.jpg', 'A Waterfall of Blue, Block Wide', kicker='Authentic Commercial Install'))
both('SL_42_authentic_globes',
     photo_post(SL, SQ, f'{SLR}/sl_auth_42_feed.jpg', 'A Ceiling of Light', kicker='Authentic Commercial Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_42_story.jpg', 'A Ceiling of Light', kicker='Authentic Commercial Install'))
both('SL_43_authentic_classic',
     photo_post(SL, SQ, f'{SLR}/sl_auth_43_feed.jpg', 'Classic Red and Green, Done Right', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_43_story.jpg', 'Classic Red and Green, Done Right', kicker='Authentic Spruce Install'))

both('SL_44_authentic_storybook',
     photo_post(SL, SQ, f'{SLR}/sl_auth_44_feed.jpg', 'A Storybook Christmas', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_44_story.jpg', 'A Storybook Christmas', kicker='Authentic Spruce Install'))
both('SL_45_authentic_snowflakes',
     photo_post(SL, SQ, f'{SLR}/sl_auth_45_feed.jpg', 'Snowflakes That Never Melt', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_45_story.jpg', 'Snowflakes That Never Melt', kicker='Authentic Spruce Install'))
both('SL_46_authentic_columns',
     photo_post(SL, SQ, f'{SLR}/sl_auth_46_feed.jpg', 'Every Arch, Every Column', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_46_story.jpg', 'Every Arch, Every Column', kicker='Authentic Spruce Install'))
both('SL_47_authentic_estate',
     photo_post(SL, SQ, f'{SLR}/sl_auth_47_feed.jpg', 'The Whole Estate, Aglow', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_47_story.jpg', 'The Whole Estate, Aglow', kicker='Authentic Spruce Install'))

both('SL_48_authentic_warmwhite',
     photo_post(SL, SQ, f'{SLR}/sl_auth_48_feed.jpg', 'Wrapped in Warm White', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_48_story.jpg', 'Wrapped in Warm White', kicker='Authentic Spruce Install'))
both('SL_49_authentic_gables',
     photo_post(SL, SQ, f'{SLR}/sl_auth_49_feed.jpg', 'Bright Gables, Warm Welcome', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_49_story.jpg', 'Bright Gables, Warm Welcome', kicker='Authentic Spruce Install'))
both('SL_50_authentic_farmhouse',
     photo_post(SL, SQ, f'{SLR}/sl_auth_50_feed.jpg', 'The Modern Farmhouse Glow', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_50_story.jpg', 'The Modern Farmhouse Glow', kicker='Authentic Spruce Install'))
both('SL_51_authentic_angles',
     photo_post(SL, SQ, f'{SLR}/sl_auth_51_feed.jpg', 'Every Angle Aglow', kicker='Authentic Spruce Install'),
     photo_post(SL, ST, f'{SLR}/sl_auth_51_story.jpg', 'Every Angle Aglow', kicker='Authentic Spruce Install'))

print('ALL SPRUCE LIGHTS STATIC DONE (v4, photo-first)')
