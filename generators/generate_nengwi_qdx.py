import cadquery as cq
from pathlib import Path
from common import ROOT, export_step

BODY_X=30.00
BODY_Y=12.00
BODY_Z=15.00
PIN_W=0.70
PIN_T=0.70
PIN_TAIL=4.10
PIN_EMBED=0.85
PIN1_FROM_LEFT=2.63
PIN1_TO_PIN9=24.74
PITCH=2.54
PIN_ROW_FROM_FRONT=0.64
PIN_ROW_Y=-BODY_Y/2+PIN_ROW_FROM_FRONT

PIN_X_POS={
    1:-BODY_X/2+PIN1_FROM_LEFT,
    2:-BODY_X/2+PIN1_FROM_LEFT+PITCH,
    3:-BODY_X/2+PIN1_FROM_LEFT+2*PITCH,
    4:-BODY_X/2+PIN1_FROM_LEFT+3*PITCH,
    6: BODY_X/2-PIN1_FROM_LEFT-3*PITCH,
    7: BODY_X/2-PIN1_FROM_LEFT-2*PITCH,
    8: BODY_X/2-PIN1_FROM_LEFT-PITCH,
    9: BODY_X/2-PIN1_FROM_LEFT,
}

BODY_COLOR=cq.Color(0.035,0.050,0.060)
PIN_COLOR=cq.Color(0.72,0.72,0.76)
TEXT_COLOR=cq.Color(0.80,0.82,0.84)

def make_body():
    body=cq.Workplane("XY").box(BODY_X,BODY_Y,BODY_Z,centered=(True,True,False))
    try:
        body=body.edges("|Z").fillet(0.18)
        body=body.edges(">Z").chamfer(0.12)
    except Exception:
        pass
    relief_x=0.75
    relief_z=0.65
    for sx in (-1,1):
        cut=(cq.Workplane("XY")
             .box(relief_x,BODY_Y+0.2,relief_z,centered=(True,True,False))
             .translate((sx*(BODY_X/2-relief_x/2),0,0)))
        body=body.cut(cut)
    return body

def make_pins():
    solids=[]
    z0=-PIN_TAIL
    z1=PIN_EMBED
    for n in (1,2,3,4,6,7,8,9):
        p=(cq.Workplane("XY")
           .box(PIN_W,PIN_T,z1-z0,centered=(True,True,False))
           .translate((PIN_X_POS[n],PIN_ROW_Y,z0)))
        try:
            p=p.edges("<Z").chamfer(0.07)
        except Exception:
            pass
        solids.append(p.val())
    return cq.Compound.makeCompound(solids)

def front_text(txt,z,size,depth=0.018):
    return (cq.Workplane("XZ",origin=(0,-BODY_Y/2-0.002,0))
            .center(0,z)
            .text(txt,size,depth,halign="center",valign="center"))

def pin1_marker():
    return (cq.Workplane("XZ",origin=(0,-BODY_Y/2-0.003,0))
            .center(-BODY_X/2+2.05,2.25)
            .circle(0.30).extrude(0.02))

def build(name,realistic):
    a=cq.Assembly(name=name.replace("-","_"))
    a.add(make_body(),name="MOLDED_CASE",color=BODY_COLOR)
    a.add(make_pins(),name="PINS_1_2_3_4_6_7_8_9",color=PIN_COLOR)
    if realistic:
        try:
            a.add(front_text("NENGWI",10.6,2.10),name="MARK_BRAND",color=TEXT_COLOR)
            a.add(front_text(name,7.6,1.55),name="MARK_PART",color=TEXT_COLOR)
            a.add(pin1_marker(),name="PIN1_MARK",color=TEXT_COLOR)
        except Exception:
            pass
    return a

def main():
    out=ROOT/"generated"/"NENGWI_QDX"
    out.mkdir(parents=True,exist_ok=True)
    for name in ("QDX05GXXXX-B","QDX12GXXXX-B"):
        for suffix,realistic in (("REALISTIC",True),("CLEAN",False)):
            p=out/f"NENGWI_{name}_{suffix}.step"
            print(p,export_step(build(name,realistic),p))

if __name__=="__main__":
    main()
