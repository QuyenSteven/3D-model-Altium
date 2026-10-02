import cadquery as cq
from common import ROOT, export_step

BODY=14.0
OVERALL=16.0
PITCH=0.40
PIN_W=0.18
A1=0.10
A2=1.40
TOP=A1+A2

def build():
    body=cq.Workplane("XY").box(BODY,BODY,A2,centered=(True,True,False)).translate((0,0,A1))
    try: body=body.edges().chamfer(0.10)
    except Exception: pass
    dot=(cq.Workplane("XY").workplane(offset=TOP-0.05)
         .center(-5.75,-5.75).circle(0.32).extrude(0.10))
    body=body.cut(dot)

    x0=BODY/2-0.10; x1=BODY/2+0.18; x2=OVERALL/2-0.60; x3=OVERALL/2
    zi=0.43; zf=0.06; t=0.10
    lead=(cq.Workplane("XZ").moveTo(x0,zi-t/2).lineTo(x1,zi-t/2)
          .lineTo(x2,zf-t/2).lineTo(x3,zf-t/2).lineTo(x3,zf+t/2)
          .lineTo(x2,zf+t/2).lineTo(x1,zi+t/2).lineTo(x0,zi+t/2)
          .close().extrude(PIN_W/2,both=True))
    pos=[(i-15.5)*PITCH for i in range(32)]
    shapes=[]
    for p in pos: shapes.append(lead.translate((0,p,0)).val())
    for p in pos: shapes.append(lead.rotate((0,0,0),(0,0,1),90).translate((-p,0,0)).val())
    for p in pos: shapes.append(lead.rotate((0,0,0),(0,0,1),180).translate((0,-p,0)).val())
    for p in pos: shapes.append(lead.rotate((0,0,0),(0,0,1),-90).translate((p,0,0)).val())
    pins=cq.Compound.makeCompound(shapes)
    a=cq.Assembly(name="RTL8367S_LQFP128")
    a.add(body,name="IC_BODY",color=cq.Color(0.10,0.10,0.10))
    a.add(pins,name="LEADS_128",color=cq.Color(0.75,0.75,0.78))
    return a

if __name__=="__main__":
    p=ROOT/"generated"/"RTL8367S"/"RTL8367S_LQFP128.step"
    print(p, export_step(build(),p))
