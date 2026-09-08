# -*- coding: utf-8 -*-
"""Build the compact JSON payload embedded in the presentation:
simplified + projected geometry, the harmonised price panel, and derived series."""
import json, io, csv, math, collections, statistics as st

# ---------- geometry helpers ----------
def dp(pts, eps):
    """Douglas-Peucker on a ring."""
    if len(pts) < 3: return pts
    def d2(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2-x1, y2-y1
        if dx == 0 and dy == 0: return (x-x1)**2 + (y-y1)**2
        t = max(0, min(1, ((x-x1)*dx + (y-y1)*dy)/(dx*dx+dy*dy)))
        return (x-(x1+t*dx))**2 + (y-(y1+t*dy))**2
    keep = [False]*len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts)-1)]
    while stack:
        i, j = stack.pop()
        if j <= i+1: continue
        md, mi = -1, i
        for k in range(i+1, j):
            dd = d2(pts[k], pts[i], pts[j])
            if dd > md: md, mi = dd, k
        if md > eps*eps:
            keep[mi] = True; stack += [(i, mi), (mi, j)]
    return [p for p, k in zip(pts, keep) if k]

def rings(geom):
    t, c = geom["type"], geom["coordinates"]
    if t == "Polygon": return [c]
    if t == "MultiPolygon": return c
    return []

def area(r):
    s = 0
    for i in range(len(r)-1):
        s += r[i][0]*r[i+1][1] - r[i+1][0]*r[i][1]
    return abs(s)/2

# ---------- projection ----------
LAT0, LON0 = 49.815, 6.13
K = math.cos(math.radians(LAT0))
def proj(lon, lat): return ((lon-LON0)*K, -(lat-LAT0))

def build_shapes(features, namekey, eps_deg, min_area_frac=0.004, quant=2000.0):
    raw = []
    for f in features:
        nm = f["properties"][namekey]
        polys = []
        for poly in rings(f["geometry"]):
            outer = poly[0]
            if len(outer) < 4: continue
            polys.append([proj(x, y) for x, y in outer])
        if polys: raw.append((nm, polys))
    # global bbox
    xs = [p[0] for _, ps in raw for r in ps for p in r]
    ys = [p[1] for _, ps in raw for r in ps for p in r]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    sc = 1000.0/max(x1-x0, y1-y0)
    W, H = (x1-x0)*sc, (y1-y0)*sc
    out = {}
    for nm, polys in raw:
        polys = [[( (p[0]-x0)*sc, (p[1]-y0)*sc ) for p in r] for r in polys]
        big = max(area(r) for r in polys)
        polys = [r for r in polys if area(r) >= big*min_area_frac]
        simp = []
        for r in polys:
            s = dp(r, eps_deg*sc)
            if len(s) >= 4:
                simp.append([[round(p[0], 2), round(p[1], 2)] for p in s])
        if simp: out[nm] = simp
    return out, round(W, 2), round(H, 2)

# ---------- communes ----------
gj = json.load(io.open("data/raw/communes4326.geojson", encoding="utf8"))
canton = {f["properties"]["COMMUNE"]: f["properties"]["CANTON"] for f in gj["features"]}
lau   = {f["properties"]["COMMUNE"]: f["properties"]["LAU2"] for f in gj["features"]}
shapes, W, H = build_shapes(gj["features"], "COMMUNE", 0.00035)
print(f"communes: {len(shapes)} shapes, viewBox {W} x {H}, "
      f"pts={sum(len(r) for s in shapes.values() for r in s)}")

# centroid of the largest ring, for labels / zoom
cent = {}
for nm, polys in shapes.items():
    r = max(polys, key=area)
    cx = sum(p[0] for p in r)/len(r); cy = sum(p[1] for p in r)/len(r)
    cent[nm] = [round(cx, 1), round(cy, 1)]


from pathlib import Path
Path("data/clean").mkdir(parents=True,exist_ok=True)
Path("data/clean/payload.json").write_text(json.dumps({"shapes":shapes,"vb":[W,H],"cent":cent},ensure_ascii=False),encoding="utf-8")
