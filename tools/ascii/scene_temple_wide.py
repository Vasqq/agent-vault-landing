"""The whole Temple of Saturn, reconstructed (cella, pediment, roof), standing on rolling hills."""
import numpy as np, json, math
from raymarch import *
import scene_temple as S
SP, HC, XW = S.SP, S.HC, S.XW
D = 17.0     # depth of the temple (cella behind the pronaos)
E0 = HC+0.03
def terrain(x, z):
    h = -4.2 + 3.2*np.sin(0.075*x+0.6)*np.sin(0.065*z+1.1) + 2.2*np.sin(0.045*x-0.06*z+0.4) + 0.7*np.sin(0.15*x+0.12*z)
    # flatten a plaza around the temple
    cx, cz = XW/2, D/2-3
    d = np.sqrt(((x-cx)/(XW/2+9))**2 + ((z-cz)/(D/2+10))**2)
    f = np.clip((d-1.0)/0.8, 0, 1); f = f*f*(3-2*f)
    return -3.4*(1-f) + h*f
def sdf_parts(p):
    x,y,z = p[:,0],p[:,1],p[:,2]
    cols = [S.column_sdf(p,cx,cz) for cx,cz in S.COLPOS]
    pod = sd_box(p, np.array([XW/2,-1.7,D/2-0.6]), np.array([XW/2+1.6,1.7,D/2+0.6]))
    lip = sd_box(p, np.array([XW/2,-0.1,D/2-0.6]), np.array([XW/2+1.75,0.1,D/2+0.75]))
    steps=[]
    for i in range(10):
        top = -3.4 + (i+1)*0.34; zf = -1.2 - (9-i)*0.42
        steps.append(sd_box(p, np.array([XW/2,(top-3.4)/2,(zf-1.2)/2]), np.array([XW/2-0.3,(top+3.4)/2,(-1.2-zf)/2+0.001])))
    cella = sd_box(p, np.array([XW/2, HC/2, (SP+0.7+D-1.0)/2]), np.array([XW/2+0.55, HC/2, (D-1.0-(SP+0.7))/2]))
    ent = sd_box(p, np.array([XW/2, E0+1.0, (D-0.5-0.8)/2]), np.array([XW/2+0.85, 1.0, (D-0.5+0.8)/2]))
    cor = sd_box(p, np.array([XW/2, E0+2.08, (D-0.5-0.8)/2]), np.array([XW/2+1.05, 0.1, (D-0.5+0.8)/2+0.2]))
    # gabled roof / pediment
    b, h = XW/2+1.1, 2.5; y0 = E0+2.18; cx = XW/2
    q = np.stack([np.abs(x-cx), y-y0],-1)
    nrm = np.array([h, b])/math.hypot(h,b)
    tri = np.maximum(-(y-y0), (q*nrm).sum(-1) - (b*h)/math.hypot(h,b))
    roof = np.maximum(tri, np.maximum(-0.95-z, z-(D-0.3)))
    building = np.minimum.reduce(cols+[pod,lip,cella,ent,cor,roof]+steps)
    ground = (y - terrain(x,z))*0.55
    return building, ground
def sdf(p):
    b,g = sdf_parts(p); return np.minimum(b,g)

def render_wide(cols=330, rows=104, ss=2):
    """Closing view: the whole temple, reconstructed, from above and far away, on rolling ground.
    Returns (lum, hit, ground_mask) per character cell; ground cells become the digital landscape."""
    ro = np.array([-16.0, 8.5, -24.0]); ta = np.array([XW/2+1.0, 1.2, 5.0])
    rd,(Hs,Ws) = camera(ro, ta, cols, rows, fov=40, ss=ss)
    ro_ = np.broadcast_to(ro, rd.shape).copy()
    t, hit = march(sdf, ro_, rd, tmax=140, steps=260)
    p = ro_[hit]+rd[hit]*t[hit,None]
    n = normal(sdf,p)
    Ld = norm(np.array([-0.55,0.6,-0.55]))
    dif = np.clip((n*Ld).sum(-1),0,1)
    sh = softshadow(sdf, p+n*0.02, Ld, k=10, tmax=40)
    a = ao(sdf,p,n)
    bpart, gpart = sdf_parts(p)
    isg = gpart < bpart
    alb = np.ones(p.shape[0])
    alb[~isg] *= 0.9 + 0.2*((np.sin(p[~isg,0]*41.3+p[~isg,1]*77.1+p[~isg,2]*19.7)*43758.5)%1)
    # door of the cella: dark
    door = (~isg) & (np.abs(p[:,2]-(SP+0.7))<0.08) & (np.abs(p[:,0]-XW/2)<1.3) & (p[:,1]<5.2)
    alb[door] = 0.15
    # ground furrows, like ploughed hills
    alb[isg] = 0.35 + 0.3*(np.sin(p[isg,2]*3.0 + np.sin(p[isg,0]*0.25)*2.4) > 0.3)
    low = (~isg) & (p[:,1] < -0.05)
    lum = np.zeros(rd.shape[0])
    col = (dif*sh*1.05 + 0.12*np.clip(n[:,1]*0.5+0.5,0,1)*a + 0.02)*alb
    col[low] *= np.where(n[low,1]>0.7, 1.0, np.where(n[low,2]<-0.7, 0.4, 0.7))
    fog = np.exp(-np.maximum(t[hit]-25,0)*0.02)
    lum[hit] = np.clip(col*fog,0,1)
    mat = np.zeros(rd.shape[0]); mat[np.where(hit)[0][isg]] = 1
    g = lum.reshape(Hs,Ws).reshape(rows,ss,cols,ss).mean(axis=(1,3))
    hc = hit.reshape(Hs,Ws).reshape(rows,ss,cols,ss).mean(axis=(1,3))
    gm = mat.reshape(Hs,Ws).reshape(rows,ss,cols,ss).mean(axis=(1,3)) > 0.5
    return g, hc, gm
