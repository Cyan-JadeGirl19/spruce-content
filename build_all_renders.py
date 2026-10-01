#!/usr/bin/env python3
"""Build /home/user/ALL_RENDERS.html — single-file review gallery (v8)."""
import base64, glob, io, os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/user/ALL_RENDERS.html"

def img_b64(path, width=560, q=72):
    im = Image.open(path).convert("RGB")
    if im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q)
    return base64.b64encode(buf.getvalue()).decode()

def vid_b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

def title_of(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    parts = stem.split("_")[2:]  # drop SL_01_
    t = " ".join(parts).replace("-", " ").title()
    return t if t else stem

CARD_CSS = ("background:#111c16;border:1px solid #23392c;border-radius:14px;overflow:hidden;"
            "break-inside:avoid;margin-bottom:18px")
LABEL_CSS = ("padding:8px 12px;font:600 12px/1.35 system-ui;color:#bfd6c6;letter-spacing:.04em;"
             "text-transform:uppercase")

def grid(paths, cols):
    cells = []
    for p in paths:
        b = img_b64(p)
        cells.append(f'<figure style="{CARD_CSS}">'
                     f'<img src="data:image/jpeg;base64,{b}" style="width:100%;display:block">'
                     f'<figcaption style="{LABEL_CSS}">{title_of(p)}</figcaption></figure>')
    return (f'<div style="column-gap:16px;columns:{cols};">'
            + "".join(cells) + "</div>")

def video_row(paths):
    cells = []
    for p in paths:
        prev = "/tmp/vprev/" + os.path.basename(p)
        b = vid_b64(prev if os.path.exists(prev) else p)
        cells.append(f'<figure style="{CARD_CSS}">'
                     f'<video src="data:video/mp4;base64,{b}" controls playsinline '
                     f'style="width:100%;display:block;background:#000"></video>'
                     f'<figcaption style="{LABEL_CSS}">{os.path.basename(p)}</figcaption></figure>')
    return '<div style="display:flex;flex-wrap:wrap;gap:16px">' + "".join(cells) + "</div>"

def section(head, sub, body, accent):
    return (f'<section style="margin:34px 0">'
            f'<h2 style="font:800 22px/1.2 system-ui;color:{accent};margin:0 0 4px">{head}</h2>'
            f'<p style="font:400 13px/1.5 system-ui;color:#8fa998;margin:0 0 14px">{sub}</p>'
            f'{body}</section>')

def brand_paths(brand):
    feed = sorted(glob.glob(f"{ROOT}/deliverables/{brand}/feed/*.jpg"))
    story = sorted(glob.glob(f"{ROOT}/deliverables/{brand}/story/*.jpg"))
    return feed, story

slf, sls = brand_paths("spruce_lights")
spf, sps = brand_paths("spruce_pro")
slv = sorted(glob.glob(f"{ROOT}/videos/spruce_lights/*.mp4"))
spv = sorted(glob.glob(f"{ROOT}/videos/spruce_pro/*.mp4"))
shv = sorted(glob.glob(f"{ROOT}/videos/spruce_lights/showcase/*.mp4"))

html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Spruce — October 2026 Master Gallery (v8)</title></head>
<body style="margin:0;background:#0b120e;color:#e8f0ea;font-family:system-ui">
<div style="max-width:1180px;margin:0 auto;padding:30px 20px 60px">
<h1 style="font:800 30px/1.15 system-ui;margin:0 0 6px">Spruce Lights + Spruce Pro — October 2026</h1>
<p style="font:400 14px/1.5 system-ui;color:#8fa998;margin:0 0 22px">
Master gallery v8 — {len(slf)+len(spf)} feed + {len(sls)+len(sps)} story cards, 8 videos, calendar &amp; gallery pages.
<b style="color:#d8e6dc">New:</b> Spruce Lights “Website Edition” — the sprucelights.com look:
dark pine green, cream Playfair serif headlines with gold highlight phrases, gold calls-to-action, sage body text.
Brand chips on every card. Spruce Pro untouched.</p>

<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:8px">
<span style="background:#1c3a26;color:#9fe06a;font:700 12px/1 system-ui;padding:9px 14px;border-radius:99px">SPRUCE LIGHTS — HOLIDAY LIGHTING</span>
<span style="background:#0d3a40;color:#5fe3ea;font:700 12px/1 system-ui;padding:9px 14px;border-radius:99px">SPRUCE PRO — EXTERIOR CLEANING</span>
<span style="background:#161d18;color:#9ab5a2;font:600 12px/1 system-ui;padding:9px 14px;border-radius:99px">logos 168px everywhere</span>
<span style="background:#161d18;color:#9ab5a2;font:600 12px/1 system-ui;padding:9px 14px;border-radius:99px">80 unique backgrounds</span>
</div>

{section("Spruce Lights — feed (1:1) · paper edition", "Website edition — pine cards, Playfair serif headlines, gold CTAs (matches sprucelights.com) · lime→gold accent · (864) 288-2459", grid(slf, 3), "#9fe06a")}
{section("Spruce Lights — stories (9:16)", "Same paper system, tall format", grid(sls, 4), "#9fe06a")}
{section("Spruce Pro — feed (1:1)", "Deep teal system, cyan chips · (864) 483-4300 · unchanged this round", grid(spf, 3), "#5fe3ea")}
{section("Spruce Pro — stories (9:16)", "", grid(sps, 4), "#5fe3ea")}
{section("Showcase — real lights (NEW)", "5 video posts × feed + story: residential · commercial · municipal · true before/after (same home) · grand tour — soothing twinkle", video_row(shv), "#ffd76a")}
{section("Videos — Spruce Lights (brand)", "Sting · promo reel · promo feed · before/after reel (true same-home pair, soothing mix)", video_row(slv), "#9fe06a")}
{section("Videos — Spruce Pro (teal, music-box twinkle)", "", video_row(spv), "#5fe3ea")}
<p style="font:400 12px/1.6 system-ui;color:#6d8577;margin-top:26px">
Also in the download packs: content_calendar.html (full October posting plan) and gallery.html.
Downloads: DOWNLOAD_1_SpruceLights_Graphics.zip · DOWNLOAD_2_SprucePro_Graphics.zip · DOWNLOAD_3_Spruce_Videos.zip</p>
</div></body></html>"""

open(OUT, "w").write(html)
print(f"ALL_RENDERS v8 written: {os.path.getsize(OUT):,} bytes")
