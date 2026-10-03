#!/usr/bin/env python3
import json, sys
from pathlib import Path
import cadquery as cq

src=Path(sys.argv[1])
out=Path(sys.argv[2])
x=float(sys.argv[3]) if len(sys.argv)>3 else 0.0

wp=cq.importers.importStep(str(src))
shape=cq.Compound.makeCompound(wp.solids().vals())

plane=cq.Plane(origin=(x,0,0), xDir=(0,1,0), normal=(1,0,0))
sec=cq.Workplane(plane).add(shape).section()
wires=sec.wires().vals()

data={"source":str(src),"x":x,"wire_count":len(wires),"wires":[]}
for wi,w in enumerate(wires):
    edge_rows=[]
    for ei,e in enumerate(w.Edges()):
        verts=e.Vertices()
        pts=[{"y":round(v.Y,6),"z":round(v.Z,6)} for v in verts]
        edge_rows.append({
            "index":ei,
            "geom_type":str(e.geomType()),
            "vertices_yz":pts
        })
    wire_verts=[{"y":round(v.Y,6),"z":round(v.Z,6)} for v in w.Vertices()]
    data["wires"].append({
        "index":wi,
        "vertices_yz":wire_verts,
        "edges":edge_rows
    })

out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(data,indent=2),encoding="utf-8")
print(json.dumps(data,indent=2))
