"""Tiny vectorised signed-distance raymarcher (numpy). Shared by every AgentVault ASCII scene."""
import numpy as np
def norm(v): return v/np.linalg.norm(v,axis=-1,keepdims=True)
def sd_box(p, c, b):
    q = np.abs(p - c) - b
    return np.linalg.norm(np.maximum(q,0),axis=-1) + np.minimum(np.max(q,axis=-1),0)
def march(sdf, ro, rd, tmax=80, steps=160, eps=2e-3, k=0.85):
    n = rd.shape[0]; t = np.zeros(n); hit = np.zeros(n,bool); alive = np.ones(n,bool)
    for _ in range(steps):
        idx = np.where(alive)[0]
        if idx.size==0: break
        p = ro[idx] + rd[idx]*t[idx,None]
        d = sdf(p)
        h = d < eps*(1+t[idx]*0.3)
        hit[idx[h]] = True
        t[idx] += d*k
        dead = h | (t[idx] > tmax)
        alive[idx[dead]] = False
    return t, hit
def normal(sdf, p, e=2e-3):
    ex = np.array([e,0,0]); ey=np.array([0,e,0]); ez=np.array([0,0,e])
    n = np.stack([sdf(p+ex)-sdf(p-ex), sdf(p+ey)-sdf(p-ey), sdf(p+ez)-sdf(p-ez)],-1)
    return norm(n)
def softshadow(sdf, p, L, k=10, tmax=30, steps=60):
    res = np.ones(p.shape[0]); t = np.full(p.shape[0], 0.05)
    for _ in range(steps):
        d = sdf(p + L*t[:,None])
        res = np.minimum(res, np.clip(k*d/t,0,1))
        t += np.clip(d, 0.02, 1.0)
        if np.all((t>tmax)|(res<0.01)): break
    return np.clip(res,0,1)
def ao(sdf, p, n, steps=5, delta=0.25):
    occ = np.zeros(p.shape[0])
    for i in range(1,steps+1):
        h = delta*i
        occ += (h - sdf(p+n*h))/ (2**i)
    return np.clip(1-occ*1.6,0,1)
def camera(ro, ta, W, H, fov=55, ss=2):
    f = norm(ta-ro); r = norm(np.cross(f, np.array([0,1,0.]))); u = np.cross(r,f)
    ys, xs = np.mgrid[0:H*ss, 0:W*ss].astype(float)
    ar = (W*0.6)/H  # cell aspect: cell width 0.6 of height
    sx = ((xs+0.5)/(W*ss)*2-1)*ar
    sy = -((ys+0.5)/(H*ss)*2-1)
    z = 1/np.tan(np.radians(fov/2))
    d = sx[...,None]*r + sy[...,None]*u + z*f
    return norm(d.reshape(-1,3)), (H*ss, W*ss)
