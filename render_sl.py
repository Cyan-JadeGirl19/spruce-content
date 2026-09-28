"""Spruce Lights statics v3 — UNIQUE image per card, cinematic frosted blend."""
import sys; sys.path.insert(0, '/home/user/spruce')
from templates import *
from spruce_kit import *

BG = f'{ROOT}/assets/bg'
SLR = f'{ROOT}/assets/photos/sl_real'
OUT = f'{ROOT}/deliverables/spruce_lights'

def both(name, fn_sq, fn_st):
    save(fn_sq, f'{OUT}/feed/{name}_feed.jpg')
    save(fn_st, f'{OUT}/story/{name}_story.jpg')
    print('ok', name)

# 01 launch — real tan home at dusk
both('SL_01_booking_launch',
    hero(SL, SQ, f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Now Booking October', 'Your Home, Aglow All Season Long', 'Custom design • Pro install • We store them till next year', strand=True),
    hero(SL, ST, f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Now Booking October', 'Your Home, Aglow All Season Long', 'Custom design • Professional install • We store them till next year', strand=True, badge='Slots Filling Fast'))

# 02 review — real red-brick home
both('SL_02_review_michelle',
    review(SL, SQ, 'Spruce made our house look magical throughout Christmas and New Years! Easy to work with and a unique, natural look for our home.', 'Michelle B.', 'Google Review • Greenville, SC', bg_path=f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg'),
    review(SL, ST, 'Spruce made our house look magical throughout Christmas and New Years! Easy to work with and they created a unique and natural look for our home. We will definitely be using them again!', 'Michelle B.', 'Google Review • Greenville, SC', bg_path=f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg'))

# 03 before/after — AI day/night pair
both('SL_03_before_after',
    before_after(SL, SQ, f'{BG}/sl_day.jpg', f'{BG}/sl_night.jpg', 'The Spruce Difference', 'From Everyday to Enchanting'),
    before_after(SL, ST, f'{BG}/sl_day.jpg', f'{BG}/sl_night.jpg', 'The Spruce Difference', 'From Everyday to Enchanting'))

# 04 stat — real C9 bulb macro
both('SL_04_free_service_calls',
    stat(SL, SQ, 'The Spruce Promise', '100%', 'Free Service Calls', 'Burnt-out bulb? Weather damage? Our elves are on standby all season — you never touch a ladder.', bg_path=f'{SLR}/sl_15_hting-installation-municipalities-2.jpg'),
    stat(SL, ST, 'The Spruce Promise', '100%', 'Free Service Calls', 'Burnt-out bulb? Weather damage? Our elves are on standby all season to get your display glowing again — fast, and free.', bg_path=f'{SLR}/sl_15_hting-installation-municipalities-2.jpg'))

# 05 process — real crew carrying strands
both('SL_05_process',
    steps(SL, SQ, 'Effortless by Design', 'The Spruce Process', [('Design Consultation', 'A custom look drawn for YOUR home'), ('Custom-Fit Install', 'Commercial-grade lights, perfect lines'), ('Takedown & Storage', 'We pack and store them till next year')], bg_path=f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg'),
    steps(SL, ST, 'Effortless by Design', 'The Spruce Process', [('Design Consultation', 'A custom light design drawn for YOUR home'), ('Custom-Fit Installation', 'Commercial-grade lights, perfect clean lines'), ('Post-Season Takedown', 'We remove everything after the holidays'), ('Year-Round Storage', 'Climate-safe storage until next season')], bg_path=f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg'))

# 06 services — real municipal plaza
both('SL_06_services',
    services(SL, SQ, 'All-Inclusive Holiday Lighting', 'One Call Does It All', ['Residential Homes & HOAs', 'Commercial Properties', 'Municipal & Town Displays', 'Garland • Wreaths • Decor'], bg_path=f'{SLR}/sl_16_hting-installation-municipalities-3.jpg'),
    services(SL, ST, 'All-Inclusive Holiday Lighting', 'One Call Does It All', ['Residential Homes & HOAs', 'Commercial Properties', 'Municipal & Town Displays', 'Garland • Wreaths • Holiday Decor', 'Tree Wrapping & Ground Displays'], bg_path=f'{SLR}/sl_16_hting-installation-municipalities-3.jpg'))

# 07 poll — real color-lit walkway
both('SL_07_poll',
    poll(SL, SQ, 'Comment below', 'Which lit look wins?', ['Roofline Glow', 'Wrapped Trees', 'Walkway Magic', 'All of it — Max Twinkle'], bg_path=f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg', note='Tell us and we might design it for you 😉'),
    poll(SL, ST, 'Comment below', 'Which lit look wins?', ['Roofline Glow', 'Wrapped Trees', 'Walkway Magic', 'All of it — Max Twinkle'], bg_path=f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg', note='Tell us and we might design it for you 😉'))

# 08 halloween crossover — AI porch
both('SL_08_halloween_crossover',
    hero(SL, SQ, f'{BG}/sl_halloween.jpg', 'Halloween → Christmas', 'Trick or Treat Tonight. Twinkle by December.', 'The smartest households book their Christmas lights on Halloween week', cta=True),
    hero(SL, ST, f'{BG}/sl_halloween.jpg', 'Halloween → Christmas', 'Trick or Treat Tonight. Twinkle by December.', 'The smartest households book their Christmas lights on Halloween week', cta=True, badge='Smart Move'))

# 09 why pro — AI hands clipping detail
both('SL_09_why_pro',
    tip(SL, SQ, 'Good to Know', 'Why Homeowners Leave the Ladder to Us', 'Commercial-grade C7 & C9 lights custom-cut for your roofline. No ladder tumbles, no tangled storage bins, no half-lit strands in December. Just a perfect display — installed, maintained and stored by our crew.', bg_path=f'{BG}/sl_hands.jpg'),
    tip(SL, ST, 'Good to Know', 'Why Homeowners Leave the Ladder to Us', 'Commercial-grade C7 & C9 lights custom-cut for your exact roofline. No ladder tumbles. No tangled storage bins. No half-lit strands on Christmas Eve. Just a flawless display — installed, maintained and stored by our crew, year after year.', bg_path=f'{BG}/sl_hands.jpg'))

# 10 review — real snowman home
both('SL_10_review_randy',
    review(SL, SQ, 'Great team. Showed up and did excellent work. Highly recommend.', 'Randy T.', 'Google Review • Upstate, SC', bg_path=f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg'),
    review(SL, ST, 'Great team. Showed up and did excellent work. Highly recommend.', 'Randy T.', 'Google Review • Upstate, SC', bg_path=f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg'))

# 11 fun — AI reindeer yard
both('SL_11_griswold',
    hero(SL, SQ, f'{BG}/sl_sleigh.jpg', 'The Favorite Neighbor Formula', 'All the Envy. None of the Tangles.', 'Be the house everyone slows down for — we handle every detail', strand=True),
    hero(SL, ST, f'{BG}/sl_sleigh.jpg', 'The Favorite Neighbor Formula', 'All the Envy. None of the Tangles.', 'Be the house everyone slows down for — we handle every glowing detail', strand=True))

# 12 countdown — AI bokeh curtain
both('SL_12_countdown_nov1',
    countdown(SL, SQ, 'Mark Your Calendar', 'NOV 1', 'Our installation calendar fills first-come, first-served. October bookings get the best design slots — before the rush.', badge='Prime Slots'),
    countdown(SL, ST, 'Mark Your Calendar', 'NOV 1', 'Our installation calendar fills first-come, first-served. October bookings get the best design slots — before the holiday rush.', badge='Prime Slots'))

# 13 HOA — real aerial street
both('SL_13_hoa_streets',
    hero(SL, SQ, f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'HOAs • Businesses • Towns', 'Light Up the Whole Street', 'Bulk programs for neighborhoods, retail centers and municipalities', cta=True),
    hero(SL, ST, f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'HOAs • Businesses • Towns', 'Light Up the Whole Street', 'Bulk lighting programs for neighborhoods, retail centers and municipalities', cta=True))

# 14 why october — AI farmhouse
both('SL_14_why_october',
    tip(SL, SQ, 'Pro Tip', 'Why Smart Homeowners Book in October', 'October installs mean your design gets first pick of dates, lights are up before family arrives, and you skip the December scramble entirely. Same price — just a better spot in line.', bg_path=f'{BG}/sl_farmhouse.jpg'),
    tip(SL, ST, 'Pro Tip', 'Why Smart Homeowners Book in October', 'October installs mean your design gets first pick of install dates, your lights are up before family arrives, and you skip the December scramble entirely. Same price — just a much better spot in line.', bg_path=f'{BG}/sl_farmhouse.jpg'))

# 15 poll — real downtown tree crowd
both('SL_15_poll_ladder',
    poll(SL, SQ, 'Honest poll', 'Where will YOU spend a weekend this December?', ['On a ladder, untangling lights', 'On the couch, sipping cocoa'], bg_path=f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', note='There is a right answer 🎄'),
    poll(SL, ST, 'Honest poll', 'Where will YOU spend a weekend this December?', ['On a ladder, untangling lights', 'On the couch, sipping cocoa'], bg_path=f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', note='There is a right answer 🎄'))

# 16 tree wraps — AI wrapped oak
both('SL_16_tree_wraps',
    hero(SL, SQ, f'{BG}/sl_tree.jpg', 'Signature Spruce Service', 'Trees That Stop Traffic', 'Professional trunk-and-branch wrapping with festival-grade lights', cta=True),
    hero(SL, ST, f'{BG}/sl_tree.jpg', 'Signature Spruce Service', 'Trees That Stop Traffic', 'Professional trunk-and-branch wrapping with festival-grade lights — your yard becomes the landmark', cta=True))

# 17 review — real hand placing lights on big tree
both('SL_17_review_jan',
    review(SL, SQ, 'My trees wrapped in Christmas lights look amazing!! Spruce is awesome — highly, highly recommend!', 'Jan H.', 'Google Review • Greenville, SC', bg_path=f'{SLR}/sl_14_hting-installation-municipalities-1.jpg'),
    review(SL, ST, 'My trees wrapped in Christmas lights look amazing!! Spruce is awesome — highly, highly recommend!', 'Jan H.', 'Google Review • Greenville, SC', bg_path=f'{SLR}/sl_14_hting-installation-municipalities-1.jpg'))

# 18 urgency — AI precision roofline
both('SL_18_october_filling',
    stat(SL, SQ, 'Booking Update', 'OCT', '31', 'Prime October installation slots close at month-end. After that, it’s November scheduling and the design calendar gets tight.', badge='Filling Fast'),
    stat(SL, ST, 'Booking Update', 'OCT', '31', 'Prime October installation slots close at month-end. After that it’s November scheduling — and the design calendar gets tight.', badge='Filling Fast'))

# 19 CTA — AI golden bokeh
both('SL_19_cta',
    cta_card(SL, SQ, 'Let’s Light Up Your Holidays', 'Free design consultation • Free service calls all season • We install, remove & store', bg_path=f'{BG}/sl_macro.jpg'),
    cta_card(SL, ST, 'Let’s Light Up Your Holidays', 'Free design consultation • Free service calls all season • We install, remove & store everything', bg_path=f'{BG}/sl_macro.jpg'))

# 20 halloween day — AI lit doorway
both('SL_20_halloween_day',
    hero(SL, SQ, f'{BG}/sl_garland.jpg', 'Happy Halloween, Greenville 🎃', 'Candy Tonight. Twinkle Soon.', 'While you hand out candy, we’ll be penciling in light designs — grab your October slot', cta=True),
    hero(SL, ST, f'{BG}/sl_garland.jpg', 'Happy Halloween, Greenville 🎃', 'Candy Tonight. Twinkle Soon.', 'While you hand out candy, we’ll be penciling in light designs — grab your October slot before the calendar flips', cta=True))

print('ALL SPRUCE LIGHTS STATIC DONE (v3, unique images)')
