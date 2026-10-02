import cadquery as cq
from common import ROOT, export_step

BODY_L=9.285
BODY_W=6.50
OVERALL_W=10.40
PITCH=2.54
PIN_W=0.455
PIN_T=0.28
FOOT_L=1.30
BODY_BOTTOM=0.34
BODY_TOP=3.45
BODY_H=BODY_TOP-BODY_BOTTOM

def build():
    body=cq.Workplane("XY").box(BODY_L,BODY_W,BODY_H,centered=(True,True,False)).translate((0,0,BODY_BOTTOM))
    try:
        body=body.edges(">Z").chamfer(0.18)
        body=body.edges("<Z").chamfer(0.12)
        body=body.edges("|Z").fillet(0.10)
    except Exception: pass
    d=(cq.Workplane("XY").workplane(offset=BODY_TOP-0.03)
       .center(-BODY_L/2+1.00,-BODY_W/2+0.95).circle(0.30).extrude(0.06))
    body=body.cut(d)

    root_y=BODY_W/2-0.08; tip_y=OVERALL_W/2; foot_start=tip_y-FOOT_L
    z_root=0.82; z_knee=0.44; z_foot=PIN_T/2
    prof=[
      (root_y,z_root-PIN_T/2),(root_y+0.30,z_root-PIN_T/2),
      (root_y+0.44,z_knee-PIN_T/2),(foot_start,z_foot-PIN_T/2),
      (tip_y,z_foot-PIN_T/2),(tip_y,z_foot+PIN_T/2),
      (foot_start,z_foot+PIN_T/2),(root_y+0.50,z_knee+PIN_T/2),
      (root_y+0.36,z_root+PIN_T/2),(root_y,z_root+PIN_T/2)]
    def lead(sign):
        pts=prof if sign>0 else [(-y,z) for y,z in reversed(prof)]
        w=cq.Workplane("YZ").moveTo(*pts[0])
        for p in pts[1:]: w=w.lineTo(*p)
        return w.close().extrude(PIN_W/2,both=True)
    lp,ln=lead(1),lead(-1)
    pins=[]
    for i in range(4):
        x=(i-1.5)*PITCH
        pins += [lp.translate((x,0,0)).val(), ln.translate((x,0,0)).val()]
    pins=cq.Compound.makeCompound(pins)

    a=cq.Assembly(name="AMC1200_DUB_SOP8_V4_CLEAN")
    a.add(body,name="MOLDED_BODY",color=cq.Color(0.045,0.045,0.045))
    a.add(pins,name="GULLWING_LEADS_8",color=cq.Color(0.74,0.74,0.77))
    return a

if __name__=="__main__":
    p=ROOT/"generated"/"AMC1200"/"AMC1200_DUB_SOP8_V4_CLEAN.step"
    print(p, export_step(build(),p))
