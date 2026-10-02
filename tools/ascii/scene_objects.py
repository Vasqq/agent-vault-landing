"""Small objects: the Roman ring-key and the AgentVault coin."""
import numpy as np, json, math
from PIL import Image, ImageDraw, ImageFont
from raymarch import *
def rotx(p,a):
    c,s=math.cos(a),math.sin(a); return np.stack([p[:,0], c*p[:,1]-s*p[:,2], s*p[:,1]+c*p[:,2]],-1)
def roty(p,a):
    c,s=math.cos(a),math.sin(a); return np.stack([c*p[:,0]+s*p[:,2], p[:,1], -s*p[:,0]+c*p[:,2]],-1)
def rotz(p,a):
    c,s=math.cos(a),math.sin(a); return np.stack([c*p[:,0]-s*p[:,1], s*p[:,0]+c*p[:,1], p[:,2]],-1)
def shade(sdf, ro, ta, COLS, ROWS, Ld, fov=40, alb=None, ss=3):
    rd,(Hs,Ws) = camera(np.array(ro,float), np.array(ta,float), COLS, ROWS, fov=fov, ss=ss)
    ro_ = np.broadcast_to(np.array(ro,float), rd.shape).copy()
    t, hit = march(sdf, ro_, rd, tmax=40, steps=200, eps=1e-3)
    lum = np.zeros(rd.shape[0]); p = ro_[hit]+rd[hit]*t[hit,None]; n = normal(sdf,p,1e-3)
    L = norm(np.array(Ld,float)); dif = np.clip((n*L).sum(-1),0,1)
    h = norm(L - rd[hit]); spec = np.clip((n*h).sum(-1),0,1)**40
    sh = softshadow(sdf, p+n*0.005, L, k=16, tmax=10)
    a = alb(p) if alb else 1.0
    lum[hit] = np.clip((dif*sh*0.95 + 0.08 + 0.7*spec*sh)*a, 0, 1)
    g = lum.reshape(Hs,Ws).reshape(ROWS,ss,COLS,ss).mean(axis=(1,3))
    hc = hit.reshape(Hs,Ws).reshape(ROWS,ss,COLS,ss).mean(axis=(1,3))
    return g, hc
# ---- ring key ----
def key_sdf(p):
    q = rotz(roty(rotx(p, 1.1), 0.5), -0.25)
    # ring (torus around y axis), center origin
    R, r = 1.0, 0.18
    x,y,z = q[:,0],q[:,1],q[:,2]
    tor = np.sqrt((np.sqrt(x*x+z*z)-R)**2 + y*y) - r
    # plate from ring top outward (along +x) then bit
    stem = sd_box(q, np.array([1.55,0,0]), np.array([0.5,0.12,0.2]))
    bit = sd_box(q, np.array([2.05,0,0]), np.array([0.14,0.12,0.55]))
    teeth = []
    for zz in (-0.35, 0.0, 0.35):
        teeth.append(sd_box(q, np.array([2.3,0,zz]), np.array([0.14,0.12,0.09])))
    bez = sd_box(q, np.array([1.05,0,0]), np.array([0.12,0.2,0.26]))
    return np.minimum.reduce([tor, stem, bit, bez] + teeth)
# ---- coin ----
tw=2048; timg=Image.new('L',(tw,tw),0); dt=ImageDraw.Draw(timg)
import os
_F = next((p for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/Library/Fonts/Arial Bold.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf', 'C:/Windows/Fonts/arialbd.ttf'] if os.path.exists(p)), None)
fnt = ImageFont.truetype(_F, 150) if _F else ImageFont.load_default()
LEG = "AGENTVAVLT · AERARIVM · MMXXVI · "
cxy = tw/2; rad = tw*0.39
for i,ch in enumerate(LEG):
    ang = -math.pi/2 + i*(2*math.pi/len(LEG))
    im = Image.new('L',(200,200),0); ImageDraw.Draw(im).text((100,100), ch, font=fnt, fill=255, anchor='mm')
    im = im.rotate(-math.degrees(ang)-90, resample=Image.BICUBIC)
    timg.paste(255, (int(cxy+rad*math.cos(ang)-100), int(cxy+rad*math.sin(ang)-100)), im)
TEX = np.asarray(timg)/255.0
def coin_local(p):
    return rotx(roty(p, -0.35), 1.1)   # tilt the disc toward camera
def coin_sdf(p):
    q = coin_local(p); x,y,z = q[:,0],q[:,1],q[:,2]
    rr = np.sqrt(x*x+z*z)
    disc = np.maximum(rr-1.0, np.abs(y)-0.07)
    rim = np.maximum(np.maximum(rr-1.0, 0.9-rr), np.abs(y)-0.11)
    # beads
    ang = np.arctan2(z,x); k = np.round(ang/(2*math.pi/60))*(2*math.pi/60)
    bx, bz = 0.84*np.cos(k), 0.84*np.sin(k)
    bead = np.sqrt((x-bx)**2+(y-0.07)**2+(z-bz)**2)-0.028
    # keyhole relief in the centre
    kh1 = np.maximum(np.sqrt(x*x+(z-0.12)**2)-0.2, np.abs(y-0.08)-0.07)
    kh2 = sd_box(q, np.array([0,0.08,-0.14]), np.array([0.1,0.07,0.24]))
    return np.minimum.reduce([disc, rim, bead, kh1, kh2])
def coin_alb(p):
    q = coin_local(p); x,z = q[:,0],q[:,2]
    u = ((x/1.0)*0.5+0.5)*(tw-1); v = ((z/1.0)*0.5+0.5)*(tw-1)
    ink = TEX[np.clip(v.astype(int),0,tw-1), np.clip(u.astype(int),0,tw-1)]
    face = q[:,1] > 0.05
    a = np.full(p.shape[0], 0.8); a[face] = 0.5 + 0.45*ink[face]
    return a

def render_key():
    """Problem section: a Roman ring-key (anulus clavis), bit pointing up-left so it can dissolve."""
    return shade(key_sdf, [0.8,0.6,-6.2], [1.0,0,0], 130, 66, [-0.6,0.7,-0.5], fov=38)
def render_coin():
    """Mechanism section: the travelling coin. Keyhole relief (the AgentVault mark), AGENTVAVLT legend, beaded rim."""
    return shade(coin_sdf, [0,0,-6.5], [0,0,0], 120, 66, [-0.55,0.8,-0.25], fov=24, alb=coin_alb)
