import cadquery as cq
import shutil
from common import ROOT, COLORS, export_step

# JST VH standard top-entry, ratio-tuned from page-3 side profile + user's real-part photo.
PITCH=3.96
PIN_SQ=1.14
WAFER_Z=3.20
MATING_POST=7.70
SOLDER_TAIL=3.70
MAIN_DEPTH=8.50
PIN_ROW_Y=-2.25  # latch/front side

LOCK_SUPPORT_Y0=-3.30
LOCK_SUPPORT_Y1=-2.15
LOCK_SUPPORT_Z0=2.55
LOCK_SUPPORT_Z1=6.00

LOCK_TONGUE_Y0=-3.95
LOCK_TONGUE_Y1=1.25
LOCK_TONGUE_Z0=5.45
LOCK_TONGUE_Z1=6.20

LOCK_NOSE_Y0=-4.45
LOCK_NOSE_Y1=-3.85
LOCK_NOSE_Z0=5.25
LOCK_NOSE_Z1=5.90

def body_len(n):
    return (n-1)*PITCH + 3.90

def box(L,D,H,x=0,y=0,z=0):
    return cq.Workplane("XY").box(L,D,H,centered=(True,True,False)).translate((x,y,z))

def make_housing(n):
    B=body_len(n)
    h=box(B,MAIN_DEPTH,WAFER_Z)

    h=h.union(box(
        B,
        LOCK_SUPPORT_Y1-LOCK_SUPPORT_Y0,
        LOCK_SUPPORT_Z1-LOCK_SUPPORT_Z0,
        y=(LOCK_SUPPORT_Y0+LOCK_SUPPORT_Y1)/2,
        z=LOCK_SUPPORT_Z0
    ))

    h=h.union(box(
        B,
        LOCK_TONGUE_Y1-LOCK_TONGUE_Y0,
        LOCK_TONGUE_Z1-LOCK_TONGUE_Z0,
        y=(LOCK_TONGUE_Y0+LOCK_TONGUE_Y1)/2,
        z=LOCK_TONGUE_Z0
    ))

    h=h.union(box(
        B,
        LOCK_NOSE_Y1-LOCK_NOSE_Y0,
        LOCK_NOSE_Z1-LOCK_NOSE_Z0,
        y=(LOCK_NOSE_Y0+LOCK_NOSE_Y1)/2,
        z=LOCK_NOSE_Z0
    ))

    try: h=h.edges("|Z").fillet(0.10)
    except Exception: pass
    try: h=h.combine(clean=True)
    except Exception: pass
    return h,B

def make_pins(n):
    total=SOLDER_TAIL+WAFER_Z+MATING_POST
    solids=[]
    for i in range(n):
        x=(i-(n-1)/2)*PITCH
        p=(cq.Workplane("XY")
           .box(PIN_SQ,PIN_SQ,total,centered=(True,True,False))
           .translate((x,PIN_ROW_Y,-SOLDER_TAIL)))
        try:
            p=p.edges(">Z").chamfer(0.10)
            p=p.edges("<Z").chamfer(0.05)
        except Exception: pass
        solids.append(p.val())
    return cq.Compound.makeCompound(solids)

def main():
    out=ROOT/"generated"/"VH3.96"
    if out.exists():
        shutil.rmtree(out)

    for color,rgb in COLORS.items():
        for n in range(2,11):
            body,B=make_housing(n)
            pins=make_pins(n)
            a=cq.Assembly(name=f"VH3_96_{n}P_{color}_V8")
            a.add(body,name="WAFER_AND_LOCK",color=cq.Color(*rgb))
            a.add(pins,name=f"PINS_{n}",color=cq.Color(0.74,0.74,0.77))
            p=out/color/f"VH3.96_{n}P_{color}_V8_PROPORTION_TUNED.step"
            print(p,export_step(a,p))

if __name__=="__main__":
    main()
