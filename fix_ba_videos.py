import sys, math; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL=(13,27,16,255);_K.TEAL_D=(8,18,11,255);_K.TEAL_L=(24,44,28,255)
_K.SCRIM_COLOR=(2,14,8);_K.FOOT_DARK=(3,20,12);_K.CINE_SHADOW=(0.0,0.05,0.028)
from vidkit import *
from PIL import Image, ImageDraw, ImageFont
import audio_kit as AK
FONTS=f'{ROOT}/assets/fonts'
_SFC={}
def SF(px,wght=800):
    k=(px,wght)
    if k not in _SFC:
        f=ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf',px)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k]=f
    return _SFC[k]
def serif_layer(size,text,px,wght=800,color=(246,240,226,255),maxw_frac=0.84,lh=1.14,y_center=None):
    W,Hh=size; layer=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(layer); f=SF(px,wght)
    lines=wrap_text(text,f,int(W*maxw_frac),d); th=len(lines)*px*lh
    y=((Hh-th)/2 if y_center is None else y_center-th/2)+px*0.1
    for ln in lines:
        w=d.textlength(ln,font=f)
        sh=Image.new('RGBA',size,(0,0,0,0)); ImageDraw.Draw(sh).text(((W-w)/2+3,y+4),ln,font=f,fill=(0,10,6,190))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        d.text(((W-w)/2,y),ln,font=f,fill=color); y+=px*lh
    return layer,th

ST=(1080,1920); BG=f'{ROOT}/assets/bg'; dur=8.0

# ================= SPRUCE LIGHTS BA (matched pair) =================
LOGO_W = load_logo(SL, light_bg=False).crop(load_logo(SL, light_bg=False).getbbox()); LOGO_W.thumbnail((820,900), Image.LANCZOS)
foot = brand_footer_layer(ST, SL)
A0 = bg_photo(f'{BG}/sl_day.jpg', 1080, 1920, focus=0.5, brighten=0.97)
B0 = bg_photo(f'{BG}/sl_night_match.jpg', 1080, 1920, focus=0.5)
def side_label(txt, cx, color):
    lay = Image.new('RGBA', ST, (0,0,0,0)); d = ImageDraw.Draw(lay)
    d.text((cx, 1920*0.78), txt, font=F(44,'ExtraBold'), fill=color, anchor='mm', stroke_width=2, stroke_fill=(0,20,12,200))
    return lay
lbl_a = side_label("BEFORE", 1080*0.74, (215,221,215,255))
lbl_b = side_label("AFTER \u2728", 1080*0.26, (240,176,45))
cap, _ = serif_layer(ST, "Same Home. New Magic.", 54, 800, (246,240,226,255), maxw_frac=0.8, y_center=272)
def sl_ba():
    n=int(dur*FPS)
    for i in range(n):
        t=i/FPS
        x = 1080*(0.5 + 0.46*math.sin((t/dur)*2*math.pi - math.pi/2))
        img = wipe(A0.copy(), B0.copy(), int(x))
        d = ImageDraw.Draw(img)
        d.line([(int(x),0),(int(x),1920)], fill=(246,240,226), width=6)
        if x < 1080*0.72: img.alpha_composite(lbl_a)
        if x > 1080*0.28: img.alpha_composite(lbl_b)
        d = ImageDraw.Draw(img)
        d.text((540,172), "THE SPRUCE DIFFERENCE", font=F(28,'Bold'), fill=(240,176,45), anchor='mm', stroke_width=1, stroke_fill=(0,20,12,150))
        img.alpha_composite(cap); img.alpha_composite(foot)
        yield img
AK.sl_track('/tmp/sl_ba2.wav', dur, seed=8, accents=[(0.5,1046.5),(4.0,1318.5),(7.2,1568.0)], density=0.7, fade=1.0)
encode(sl_ba(), ST, 'videos/spruce_lights/SL_before_after_reel.mp4', chip_brand=SL, audio_wav='/tmp/sl_ba2.wav')
print('SL BA fixed')
