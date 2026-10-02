"""Temple of Saturn, Forum Romanum: the AgentVault hero object.

Roman, not Greek: tall podium with frontal stairs, smooth (unfluted) Ionic columns,
six across the front plus one returning on each side, and the real restoration
inscription on the architrave.
"""
import numpy as np, json
from PIL import Image, ImageDraw, ImageFont
from raymarch import *
SP=2.6; HC=8.0; NF=6
XW=(NF-1)*SP
def cyl_y(p, c, r, y0, y1):
    q=p-c; d=np.sqrt(q[:,0]**2+q[:,2]**2)-r
    return np.maximum(d, np.maximum(y0-p[:,1], p[:,1]-y1))
def column_sdf(p, cx, cz):
    q = p - np.array([cx,0,cz])
    x,y,z = q[:,0],q[:,1],q[:,2]
    rr = 0.5*(1-0.12*np.clip(y/HC,0,1))
    rad = np.sqrt(x*x+z*z)
    shaft = np.maximum(rad-rr, np.maximum(0.4-y, y-(HC-0.45)))
    base1 = np.maximum(rad-0.68, np.maximum(-y, y-0.2)); base2 = np.maximum(rad-0.58, np.maximum(-(y-0.2), y-0.4))
    ech = np.maximum(rad-0.56, np.maximum(-(y-(HC-0.45)), y-(HC-0.15)))
    abac = sd_box(q, np.array([0,HC-0.06,0]), np.array([0.72,0.09,0.72]))
    # ionic volutes: rolls along z at each side
    vol = np.minimum(np.maximum(np.sqrt((x-0.52)**2+(y-(HC-0.38))**2)-0.24, np.abs(z)-0.5),
                     np.maximum(np.sqrt((x+0.52)**2+(y-(HC-0.38))**2)-0.24, np.abs(z)-0.5))
    return np.minimum.reduce([shaft, base1, base2, ech, abac, vol])
COLPOS = [(i*SP,0.0) for i in range(NF)] + [(0.0,SP),(XW,SP)]
def sdf(p):
    ds = [column_sdf(p,cx,cz) for cx,cz in COLPOS]
    E0 = HC+0.03
    arch = sd_box(p, np.array([XW/2,E0+0.5,0]), np.array([XW/2+0.85,0.5,0.78]))
    frz  = sd_box(p, np.array([XW/2,E0+1.35,0.04]), np.array([XW/2+0.85,0.35,0.74]))
    cor  = sd_box(p, np.array([XW/2,E0+1.88,0]), np.array([XW/2+1.1,0.18,1.0]))
    sides = [sd_box(p, np.array([sx,E0+0.95,SP/2]), np.array([0.8,0.95,SP/2+0.8])) for sx in (0,XW)]
    pod = sd_box(p, np.array([XW/2,-2.1,6]), np.array([XW/2+1.6,2.1,7.4]))
    lip = sd_box(p, np.array([XW/2,-0.12,6]), np.array([XW/2+1.8,0.12,7.6]))
    steps = []
    for i in range(12):
        top = -4.2 + (i+1)*0.35
        zf = -1.4 - (11-i)*0.45
        steps.append(sd_box(p, np.array([XW/2, (top-4.2)/2, (zf+(-1.4))/2]), np.array([XW/2-0.4, (top+4.2)/2, (-1.4-zf)/2+0.001])))
    ground = p[:,1]+4.2
    return np.minimum.reduce(ds+[arch,frz,cor,lip,pod,ground]+sides+steps)
# inscription texture for architrave front face (z = -0.78)
TXT = "SENATVS·POPVLVSQVE·ROMANVS·INCENDIO·CONSVMPTVM·RESTITVIT"
tw, th = 3000, 90
timg = Image.new('L',(tw,th),0); dt=ImageDraw.Draw(timg)
import os
_FONT = next((p for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf', '/Library/Fonts/Georgia Bold.ttf', '/System/Library/Fonts/Supplemental/Georgia Bold.ttf', 'C:/Windows/Fonts/georgiab.ttf'] if os.path.exists(p)), None)
font = ImageFont.truetype(_FONT, 72) if _FONT else ImageFont.load_default()
bb = dt.textbbox((0,0),TXT,font=font); scale = (tw-40)/(bb[2]-bb[0])
font = ImageFont.truetype(_FONT, int(72*min(scale,1.2))) if _FONT else font
bb = dt.textbbox((0,0),TXT,font=font)
dt.text(((tw-(bb[2]-bb[0]))/2 - bb[0], (th-(bb[3]-bb[1]))/2 - bb[1]), TXT, font=font, fill=255)
TEX = np.asarray(timg)/255.0
def albedo(p):
    a = np.ones(p.shape[0])
    rng = np.sin(p[:,0]*37.1+p[:,1]*91.7+p[:,2]*53.3)*43758.5453; n = rng-np.floor(rng)
    a *= 0.86 + 0.22*n
    E0 = HC+0.03
    face = (np.abs(p[:,2]+0.78)<0.05)&(p[:,1]>E0+0.12)&(p[:,1]<E0+0.9)&(p[:,0]>-0.6)&(p[:,0]<XW+0.6)
    u = np.clip((p[face,0]+0.6)/(XW+1.2),0,0.9999); v = np.clip(1-(p[face,1]-(E0+0.12))/0.78,0,0.9999)
    ink = TEX[(v*th).astype(int),(u*tw).astype(int)]
    a[face] *= (1.15 - 1.0*ink)
    a[p[:,1]<-4.19] = 0.02
    a[(p[:,1]<0)&(p[:,1]>-4.19)] *= 0.75
    return a

def render_close(cols=220, rows=125, ss=2):
    """Hero view: low three-quarter angle up the stairs to the portico. Returns (lum, hit) per character cell."""
    ro = np.array([-3.6, -3.4, -10.5]); ta = np.array([7.5, 5.3, 2.0])
    rd, (Hs, Ws) = camera(ro, ta, cols, rows, fov=66, ss=ss)
    ro_ = np.broadcast_to(ro, rd.shape).copy()
    t, hit = march(sdf, ro_, rd, tmax=90, steps=200)
    lum = np.zeros(rd.shape[0])
    p = ro_[hit] + rd[hit]*t[hit, None]
    n = normal(sdf, p)
    Ld = norm(np.array([-0.62, 0.42, -0.66]))
    dif = np.clip((n*Ld).sum(-1), 0, 1)
    sh = softshadow(sdf, p + n*0.01, Ld, k=12)
    a = ao(sdf, p, n)
    sky = np.clip(n[:, 1]*0.5 + 0.5, 0, 1)
    col = (dif*sh*1.1 + 0.1*sky*a + 0.03)*albedo(p)
    low = p[:, 1] < -0.05   # podium and stairs: separate treads from risers
    col[low] *= np.where(n[low, 1] > 0.7, 1.05, np.where(n[low, 2] < -0.7, 0.38, 0.7))
    fog = np.exp(-np.maximum(t[hit] - 10, 0)*0.03)
    lum[hit] = np.clip(col*fog, 0, 1)
    g = lum.reshape(Hs, Ws).reshape(rows, ss, cols, ss).mean(axis=(1, 3))
    hc = hit.reshape(Hs, Ws).reshape(rows, ss, cols, ss).mean(axis=(1, 3))
    return g, hc
