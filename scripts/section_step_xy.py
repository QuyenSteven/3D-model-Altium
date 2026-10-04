#!/usr/bin/env python3
import json, sys
from pathlib import Path
import cadquery as cq

src=Path(sys.argv[1]); out=Path(sys.argv[2]); z=float(sys.argv[3])
wp=cq.importers.importStep(str(src))
shape=cq.Compound.makeCompound(wp.solids().vals())
plane=cq.Plane(origin=(0,0,z), xDir=(1,0,0), normal=(0,0,1))
sec=cq.Workplane(plane).add(shape).section()
wires=sec.wires().vals()

data={"source":str(src),"z":z,"wire_count":len(wires),"wires":[]}
for wi,w in enumerate(wires):
    verts=[{"x":round(v.X,6),"y":round(v.Y,6)} for v in w.Vertices()]
    bb=w.BoundingBox()
    data["wires"].append({
      "index":wi,
      "bbox":{"xmin":bb.xmin,"xmax":bb.xmax,"xlen":bb.xlen,
              "ymin":bb.ymin,"ymax":bb.ymax,"ylen":bb.ylen},
      "vertices_xy":verts
    })
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(data,indent=2),encoding="utf-8")
print(json.dumps(data,indent=2))
