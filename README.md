# 🎄 Spruce — October 2026 Social Content System

Production pipeline + finished assets for two brands:

| Brand | Site | Social |
|---|---|---|
| Spruce Holiday Lighting & Events | [sprucelights.com](https://sprucelights.com) | @spruceholidaylighting |
| Spruce Services & Solutions | [sprucepro.com](https://sprucepro.com) | @spruce_pro |

**80 finished graphics** (20 unique designs × 2 formats per brand — all unique
photography, real company logos, cinematic frosted-blend treatment) +
**8 motion videos** with branded chime soundtracks + **31-day content calendar**
with ready-to-paste captions.

## Repo layout
```
assets/
  brand/      real logos (PNG, transparency) — do not convert to JPG
  bg/         AI cinematic backgrounds (JPG)
  photos/     real job photos harvested from both websites
  fonts/      Poppins + Playfair Display (OFL licensed)
deliverables/
  spruce_lights/{feed,story}/   40 finished JPGs (1080×1080, 1080×1920)
  spruce_pro/{feed,story}/      40 finished JPGs
  SPRUCE_Oct2026_Content_Calendar.html   day-by-day plan + captions
  SPRUCE_Master_Asset_Gallery.html       visual browser for all assets
videos/
  spruce_lights/  4 MP4 (sting, promo reel, promo feed, before/after)
  spruce_pro/     4 MP4
spruce_kit.py    brand kit: colors, logos, mist/frost/cinema blend engine
templates.py     card templates (hero, review, steps, poll, stat, tip…)
render_sl.py     renders all Spruce Lights statics
render_sp.py     renders all Spruce Pro statics
render_videos_*.py  renders the 8 videos (needs imageio-ffmpeg)
audit.py         automated logo/text collision audit (80 cards)
build_docs.py    builds calendar + gallery HTML
```

## Rebuild anything
```bash
pip install pillow numpy imageio-ffmpeg
python3 render_sl.py && python3 render_sp.py   # statics
python3 python3 audit.py                       # verify 0 collisions
python3 render_videos_sl.py && python3 render_videos_sp.py  # videos
python3 build_docs.py                          # calendar + gallery
./make_zips.sh                                 # download bundles
```

## Brand system
- Deep Teal `#00303C` · Cyan `#1CC8D0` · Lime `#90D000` · Spruce Red `#C82028`
- Poppins (ExtraBold/Medium) + Playfair italic for reviews
- Signature devices: C9 bulb strands, logo sparkles, red urgency chips, lime CTA pills
- Blend v3: cinematic grade (teal shadows / warm highlights) + frosted-glass
  text zones + vignette + grain
