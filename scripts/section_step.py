#!/usr/bin/env python3
import json, sys
from pathlib import Path
import cadquery as cq

src=Path(sys.argv[1])
out=Path(sys.argv[2])
x=float(sys.argv[3]) if len(sys.argv)>3 else 0.0

wp=cq.importers.importStep(str(src))
solids=wp.solids().vals()
shape=cq.Compound.makeCompound(solids)

plane=cq.Plane(origin=(x,0,0), xDir=(0,1,0), normal=(1,0,0))
sec=cq.Workplane(plane).add(shape).section()
wires=sec.wires().vals()

data={"source":str(src),"x":x,"wire_count":len(wires),"wires":[]}
for wi,w in enumerate(wires):
    edges=w.Edges()
    pts=[]
    for e in edges:
        try:
            ds=e.discretize(tolerance=0.03)
        except TypeError:
            ds=e.discretize(0.03)
        for v in ds:
            p=(round(v.y,5), round(v.z,5))
            if not pts or p!=pts[-1]:
                pts.append(p)
    data["wires"].append({"index":wi,"points_yz":pts})

out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(data,indent=2),encoding="utf-8")
print(json.dumps(data,indent=2))
