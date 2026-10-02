"""Spruce Lights SHOWCASE series — 5 concepts x 2 formats, real property photos.
1. Residential 'Homes That Glow'  2. Commercial 'Businesses That Shine'
3. Municipal 'Towns That Twinkle' 4. Transformation (matched day->dusk pair)
5. The Crew 'Done Completely For You'
Website Edition: pine, serif titles, gold labels, brand chip, SOOTHING quiet twinkle."""
import sys, math; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL=(13,27,16,255);_K.TEAL_D=(8,18,11,255);_K.TEAL_L=(24,44,28,255)
_K.SCRIM_COLOR=(2,14,8);_K.FOOT_DARK=(3,20,12);_K.CINE_SHADOW=(0.0,0.05,0.028)
from vidkit import *
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import audio_kit as AK
import os

FONTS=f'{ROOT}/assets/fonts'
OUT=f'{ROOT}/videos/spruce_lights/showcase'
os.makedirs(OUT, exist_ok=True)
SLR=f'{ROOT}/assets/photos/sl_real'; BG=f'{ROOT}/assets/bg'
SQ=(1080,1080); ST=(1080,1920)
GOLD=(240,176,45); CREAM=(246,240,226); SAGE=(164,178,156); DK=(13,25,15)
LOGO_W = load_logo(SL, light_bg=False).crop(load_logo(SL, light_bg=False).getbbox())
LOGO_W.thumbnail((760,820), Image.LANCZOS)

_SFC={}
def SF(px,wght=800):
    k=(px,wght)
    if k not in _SFC:
        f=ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf',px)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k]=f
    return _SFC[k]

def serif_layer(size,text,px,wght=800,color=CREAM,maxw_frac=0.84,lh=1.14,y_center=None,shadow=True):
    W,Hh=size; layer=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(layer); f=SF(px,wght)
    lines=wrap_text(text,f,int(W*maxw_frac),d); th=len(lines)*px*lh
    y=((Hh-th)/2 if y_center is None else y_center-th/2)+px*0.1
    for ln in lines:
        w=d.textlength(ln,font=f)
        if shadow:
            sh=Image.new('RGBA',size,(0,0,0,0)); ImageDraw.Draw(sh).text(((W-w)/2+3,y+4),ln,font=f,fill=(0,10,6,190))
            layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        d.text(((W-w)/2,y),ln,font=f,fill=color); y+=px*lh
    return layer,th

def kicker_layer(size,text,y,px=26):
    W,Hh=size; layer=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    f=F(px,'SemiBold'); tw=d.textlength(text,font=f)
    x0=W/2-tw/2-52
    d.rounded_rectangle([x0,y-26,x0+tw+104,y+26],26,fill=(13,25,15,215),outline=GOLD+(170,),width=2)
    d.ellipse([x0+24,y-5,x0+34,y+5],fill=GOLD)
    d.text((x0+52,y-1),text,font=f,fill=GOLD,anchor='lm')
    return layer

def label_layer(size,text,y,px=34):
    W,Hh=size; layer=Image.new('RGBA',size,(0,0,0,0)); d=ImageDraw.Draw(layer)
    f=F(px,'Bold'); tw=d.textlength(text,font=f)
    ov=Image.new('RGBA',size,(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle([W/2-tw/2-26,y-30,W/2+tw/2+26,y+30],30,fill=(13,25,15,190),outline=GOLD+(120,),width=2)
    layer.alpha_composite(ov); d=ImageDraw.Draw(layer)
    d.text((W/2,y-2),text,font=f,fill=CREAM,anchor='mm')
    return layer

def endcard_frames(size, dur=3.6):
    W,Hh=size
    base=vgrad(size,(16,30,19),(7,15,9))
    base.alpha_composite(radial_glow(size,(W/2,int(Hh*0.42)),W*0.8,GOLD,peak=26))
    foot=brand_footer_layer(size,SL)
    lg=LOGO_W.copy(); lw=int(W*0.42)
    lgr=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
    tag,_=serif_layer(size,"Your home, aglow all season long.",int(44*size[1]/1920),760,CREAM,maxw_frac=0.8,y_center=int(Hh*0.66),shadow=False)
    ph=F(int(46*size[1]/1920),'ExtraBold')
    pill_t="Get My Free Quote"
    n=int(dur*FPS)
    for i in range(n):
        t=i/FPS
        img=base.copy(); d=ImageDraw.Draw(img)
        e=ease(seg(t,0.15,0.9))
        if e>0:
            l2=lgr.copy(); la=l2.getchannel('A').point(lambda v:int(v*e)); l2.putalpha(la)
            img.alpha_composite(l2,((W-l2.width)//2,int(Hh*0.16+(1-e)*60)))
        te=ease(seg(t,0.7,1.4))
        if te>0:
            tg=tag.copy(); ta=tg.getchannel('A').point(lambda v:int(v*te)); tg.putalpha(ta)
            img.alpha_composite(tg)
        pe=ease(seg(t,1.0,1.7))
        if pe>0:
            cy=int(Hh*0.78)
            f=F(int(40*size[1]/1920),'Bold'); tw=d.textlength(pill_t,font=f)
            pw=tw+110; ph2=int(84*size[1]/1920)
            d.rounded_rectangle([W/2-pw/2,cy-ph2//2,W/2+pw/2,cy+ph2//2],ph2//2,fill=tuple(int(c*pe+ (0)*(1-pe)) for c in GOLD))
            d.text((W/2,cy-2),pill_t,font=f,fill=DK,anchor='mm')
            d.text((W/2,int(Hh*0.86)),SL['phone'],font=ph,fill=CREAM,anchor='mm')
        sp=sparkle_field_layer(size,7,n=10,ymax_frac=0.95)
        draw_sparkle_field(img,sp,t+1.0)
        img.alpha_composite(foot)
        yield img

FPSn=FPS
def showcase(size, shots, kicker, title, title_y, label_y, wav, seed=21, dur=15.0):
    W,Hh=size
    foot=brand_footer_layer(size,SL)
    shot_d=(dur-3.6)/len(shots)
    pics=[bg_photo(p,W,Hh,focus=f,brighten=1.0) for (p,f,lab) in shots]
    klayer=kicker_layer(size,kicker,title_y-110)
    tlayer,_=serif_layer(size,title,int(64*size[1]/1920),780,CREAM,maxw_frac=0.86,y_center=title_y)
    labels=[label_layer(size,lab,label_y) for (p,f,lab) in shots]
    sp=sparkle_field_layer(size,6,n=9,ymax_frac=0.35)
    n=int(dur*FPS)
    for i in range(n):
        t=i/FPS
        if t >= dur-3.6:
            break
        idx=min(int(t/shot_d),len(shots)-1)
        lt=(t-idx*shot_d)/shot_d
        img=kb_from(pics[idx],size,lt,z0=1.06,z1=1.18)
        if idx>0 and t-idx*shot_d<0.45:
            img.alpha_composite(Image.new('RGBA',size,(13,25,15,int(255*(1-(t-idx*shot_d)/0.45)))))
        if t<3.0:
            e=seg(t,0.2,0.9); o=1-seg(t,2.5,3.0)
            ke=klayer.copy(); ka=ke.getchannel('A').point(lambda v:int(v*e*o)); ke.putalpha(ka); img.alpha_composite(ke)
            te=tlayer.copy(); ta=te.getchannel('A').point(lambda v:int(v*ease(seg(t,0.4,1.1))*o)); te.putalpha(ta); img.alpha_composite(te)
        le=labels[idx]
        if lt>0.18 and lt<0.92:
            la=le.getchannel('A').point(lambda v:int(v*ease(seg(lt,0.18,0.4))*(1-ease(seg(lt,0.85,0.98)))))
            le2=le.copy(); le2.putalpha(la); img.alpha_composite(le2)
        img.alpha_composite(foot)
        draw_sparkle_field(img,sp,t)
        yield img
    yield from endcard_frames(size, 3.6)

def kb_from(pic,size,t,z0=1.06,z1=1.18):
    W,Hh=size
    z=z0+(z1-z0)*easeio(t)
    im=pic.copy()
    nw,nh=int(W*z),int(Hh*z)
    im=im.resize((nw,nh),Image.LANCZOS)
    x=(nw-W)//2; y=(nh-Hh)//2
    return im.crop((x,y,x+W,y+Hh))

from vidkit import easeio, seg, ease

CONCEPTS=[
    ('residential','RESIDENTIAL','Homes That Glow',
     [(f'{SLR}/sl_02_spruce-christmas-lighting.jpg',0.5,'Roofline Glow'),
      (f'{SLR}/sl_11_ghting-installation-greenville-sc-2.jpg',0.5,'Warm & Classic'),
      (f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg',0.5,'Bold In Color')],31),
    ('commercial','COMMERCIAL','Businesses That Shine',
     [(f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg',0.45,'Landmarks & Venues'),
      (f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg',0.5,'Plazas & Centers'),
      (f'{SLR}/sl_17_hting-installation-municipalities-4.jpg',0.5,'Facilities & Campuses')],37),
    ('municipal','MUNICIPAL','Towns That Twinkle',
     [(f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg',0.5,'Parks & Walkways'),
      (f'{SLR}/sl_16_hting-installation-municipalities-3.jpg',0.45,'Civic Plazas'),
      (f'{SLR}/sl_05_nstallation-service-greenville-sc-3.jpg',0.5,'Festivals & Events')],41),
    ('crew','OUR CREW','Done Completely For You',
     [(f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg',0.4,'Custom Design'),
      (f'{SLR}/sl_14_hting-installation-municipalities-1.jpg',0.45,'Professional Install'),
      (f'{SLR}/sl_02_spruce-christmas-lighting.jpg',0.5,'You Just Come Home')],47),
]

def render_all():
    for name,kicker,title,shots,seed in CONCEPTS:
        for suffix,size,ty,ly in (('feed',SQ,410,872),('vertical',ST,620,1470)):
            wav=f'/tmp/shl_{name}.wav'
            AK.sl_track(wav,15.0,seed=seed,accents=[(5.0,783.99),(10.0,1046.5),(12.6,1318.5)],density=0.8,fade=1.7)
            path=f'{OUT}/SL_showcase_{name}_{suffix}.mp4'
            encode(showcase(size,shots,kicker,title,ty,ly,wav,seed=seed), size, path,
                   chip_brand=SL, audio_wav=wav)
            print('ok',os.path.basename(path))

# 4th concept = transformation (matched pair), special
def render_transformation():
    A0=bg_photo(f'{BG}/sl_day.jpg',1080,1080,focus=0.5,brighten=0.97)
    B0=bg_photo(f'{BG}/sl_night_match.jpg',1080,1080,focus=0.5)
    A1=bg_photo(f'{BG}/sl_day.jpg',1080,1920,focus=0.5,brighten=0.97)
    B1=bg_photo(f'{BG}/sl_night_match.jpg',1080,1920,focus=0.5)
    for suffix,size,Ai,Bi in (('feed',SQ,A0,B0),('vertical',ST,A1,B1)):
        W,Hh=size
        foot=brand_footer_layer(size,SL)
        klayer=kicker_layer(size,'THE TRANSFORMATION',150 if Hh>1200 else 120)
        tlayer,_=serif_layer(size,'Same Home. New Magic.',int(62*Hh/1920),780,CREAM,maxw_frac=0.86,
                             y_center=(260 if Hh>1200 else 210))
        la=label_layer(size,'BEFORE',int(Hh*0.80)); lb=label_layer(size,'AFTER \u2728',int(Hh*0.80))
        dur=15.0; n=int(dur*FPS)
        def gen():
            for i in range(n):
                t=i/FPS
                if t>=dur-3.6: break
                # wipe sweeps day->dusk twice: 0-6s sweep, 6-11.4 hold with glow pulse
                if t<6.0:
                    x=int(W*(0.12+0.76*ease(seg(t,0.8,5.2))))
                    img=wipe(Ai.copy(),Bi.copy(),x)
                    d=ImageDraw.Draw(img); d.line([(x,0),(x,Hh)],fill=CREAM,width=6)
                else:
                    img=Bi.copy()
                    if t<6.6:
                        img.alpha_composite(Image.new('RGBA',size,(255,255,240,int(120*(1-(t-6.0)/0.6)))))
                if t<3.0:
                    e=seg(t,0.2,0.9); o=1-seg(t,2.5,3.0)
                    ke=klayer.copy(); ka=ke.getchannel('A').point(lambda v:int(v*e*o)); ke.putalpha(ka); img.alpha_composite(ke)
                    te=tlayer.copy(); ta=te.getchannel('A').point(lambda v:int(v*ease(seg(t,0.4,1.1))*o)); te.putalpha(ta); img.alpha_composite(te)
                if t<5.2 and t>1.0:
                    la2=la.copy(); laa=la2.getchannel('A').point(lambda v:int(v*(1-ease(seg(t,4.4,5.0))))); la2.putalpha(laa); img.alpha_composite(la2)
                if t>3.4:
                    lb2=lb.copy(); lba=lb2.getchannel('A').point(lambda v:int(v*ease(seg(t,3.4,3.9)))); lb2.putalpha(lba); img.alpha_composite(lb2)
                img.alpha_composite(foot)
                yield img
            yield from endcard_frames(size,3.6)
        wav='/tmp/shl_transform.wav'
        AK.sl_track(wav,15.0,seed=53,accents=[(3.5,1046.5),(5.2,1318.5),(12.6,1568.0)],density=0.8,fade=1.7)
        encode(gen(),size,f'{OUT}/SL_showcase_transformation_{suffix}.mp4',chip_brand=SL,audio_wav=wav)
        print('ok',f'SL_showcase_transformation_{suffix}.mp4')

if __name__=='__main__':
    render_all()
    render_transformation()
    print('SHOWCASE SERIES DONE (5 concepts x 2 formats)')
