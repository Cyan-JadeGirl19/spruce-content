import sys, math; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL=(0,48,60,255);_K.TEAL_D=(0,33,42,255);_K.TEAL_L=(10,74,88,255)
_K.SCRIM_COLOR=(0,20,26);_K.FOOT_DARK=(0,26,33);_K.CINE_SHADOW=(0.0,0.10,0.13)
from vidkit import *
from PIL import Image, ImageDraw
import audio_kit as AK
ST=(1080,1920); dur=8.0
SPK = _K.SP
foot2 = brand_footer_layer(ST, SPK)
PP=f'{ROOT}/assets/photos/sp_real'; P2=f'{ROOT}/assets/photos/sp_real2'
A2i = bg_photo(f'{PP}/before_grime.jpg', 1080, 1920, focus=0.72, brighten=0.97)
B2i = bg_photo(f'{P2}/after_clean_match.jpg', 1080, 1920, focus=0.72)
def sl2(txt, cx, color):
    lay = Image.new('RGBA', ST, (0,0,0,0)); d = ImageDraw.Draw(lay)
    d.text((cx, 1920*0.78), txt, font=F(44,'ExtraBold'), fill=color, anchor='mm', stroke_width=2, stroke_fill=(0,20,26,200))
    return lay
la = sl2("BEFORE", 1080*0.74, (215,221,221,255))
lb = sl2("AFTER \u2728", 1080*0.26, (28,200,208))
cap2, _ = text_layer(ST, "The Spruce Difference", 'Bold', 50, maxw_frac=0.8, y_center=272)
def sp_ba():
    n=int(dur*FPS)
    for i in range(n):
        t=i/FPS
        x = 1080*(0.5 + 0.46*math.sin((t/dur)*2*math.pi - math.pi/2))
        img = wipe(A2i.copy(), B2i.copy(), int(x))
        d = ImageDraw.Draw(img)
        d.line([(int(x),0),(int(x),1920)], fill=(246,240,226), width=6)
        if x < 1080*0.72: img.alpha_composite(la)
        if x > 1080*0.28: img.alpha_composite(lb)
        d = ImageDraw.Draw(img)
        d.text((540,172), "PRESSURE WASHING", font=F(28,'Bold'), fill=(28,200,208), anchor='mm', stroke_width=1, stroke_fill=(0,20,26,150))
        img.alpha_composite(cap2); img.alpha_composite(foot2)
        yield img
AK.sp_track('/tmp/sp_ba2.wav', dur, seed=23, accents=[(0.5,932.3),(4.0,1174.7),(7.2,1396.9)], density=0.7, fade=1.0)
encode(sp_ba(), ST, 'videos/spruce_pro/SP_before_after_reel.mp4', chip_brand=SPK, audio_wav='/tmp/sp_ba2.wav')
print('SP BA fixed')
