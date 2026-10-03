#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import cadquery as cq

src=Path(sys.argv[1])
out=Path(sys.argv[2])
wp=cq.importers.importStep(str(src))
solids=wp.solids().vals()
rows=[]
for i,s in enumerate(solids):
    b=s.BoundingBox()
    rows.append({
        "index":i,
        "volume":float(s.Volume()),
        "bbox":{
            "xmin":b.xmin,"xmax":b.xmax,"xlen":b.xlen,
            "ymin":b.ymin,"ymax":b.ymax,"ylen":b.ylen,
            "zmin":b.zmin,"zmax":b.zmax,"zlen":b.zlen,
        }
    })
comp=cq.Compound.makeCompound(solids)
b=comp.BoundingBox()
data={
    "source":str(src),
    "solid_count":len(solids),
    "overall_bbox":{"xlen":b.xlen,"ylen":b.ylen,"zlen":b.zlen,
                    "xmin":b.xmin,"xmax":b.xmax,
                    "ymin":b.ymin,"ymax":b.ymax,
                    "zmin":b.zmin,"zmax":b.zmax},
    "solids":rows
}
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(data,indent=2),encoding="utf-8")
print(json.dumps(data,indent=2))
