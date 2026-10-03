import cadquery as cq
import shutil
from common import ROOT, COLORS, export_step

# JST VH standard top-entry header, B2P-VH ... B10P-VH
# Geometry baseline from JST VH catalog page 3.
PITCH = 3.96
PIN_SQ = 1.14

# Along pin/Z axis:
MATING_POST = 7.70
BODY_Z = 3.20
SOLDER_TAIL = 3.70
TOP_Z = BODY_Z + MATING_POST   # 10.90 mm above PCB

# Across connector depth/Y:
MAIN_DEPTH = 8.50
OVERALL_LOCK_DEPTH = 9.40
PIN_FROM_LOCK_SIDE = 2.00
PIN_ROW_Y = -MAIN_DEPTH/2 + PIN_FROM_LOCK_SIDE  # latch/front = -Y

def body_len(n):
    A = (n - 1) * PITCH
    return A + 3.90

def box(L,D,H,x=0,y=0,z=0):
    return cq.Workplane("XY").box(L,D,H,centered=(True,True,False)).translate((x,y,z))

def make_housing(n):
    B = body_len(n)

    # Main low wafer: this is NOT an XH-style shrouded housing.
    h = box(B, MAIN_DEPTH, BODY_Z)

    # Full-width upper locking ear / shelf visible in JST VH page-3 side view.
    # It spans the whole connector width (B) and projects toward the latch/front side.
    EAR_T = 0.72
    EAR_DEPTH = 5.20
    EAR_Y = -MAIN_DEPTH/2 + EAR_DEPTH/2 - 0.15
    ear = box(B, EAR_DEPTH, EAR_T, y=EAR_Y, z=BODY_Z)
    h = h.union(ear)

    # Small leading lip on the ear to match the hooked profile in side view.
    LIP_DEPTH = 0.70
    lip = box(B, LIP_DEPTH, 0.34,
              y=-MAIN_DEPTH/2 + LIP_DEPTH/2 - 0.18,
              z=BODY_Z + EAR_T)
    h = h.union(lip)

    # Small molding chamfer
    try:
        h = h.edges("|Z").fillet(0.10)
        h = h.edges(">Z").chamfer(0.08)
    except Exception:
        pass

    # Center locking tongue/ramp on the front/latch side.
    extra = OVERALL_LOCK_DEPTH - MAIN_DEPTH
    latch_w = min(3.20, max(2.20, B * 0.42))
    # tongue projects beyond the main wafer
    tongue = box(
        latch_w, extra + 1.15, 1.35,
        y=-(MAIN_DEPTH/2 + extra/2) + 0.15,
        z=0.55
    )
    h = h.union(tongue)

    # upper locking ramp, approximated as a short cap
    # Central locking web under the full-width ear.
    ramp = box(
        latch_w * 0.78, 1.30, 0.55,
        y=-(MAIN_DEPTH/2 + 0.38),
        z=1.70
    )
    h = h.union(ramp)

    # Pin-1 molded corner notch / orientation cue
    try:
        notch = box(
            0.65, 0.65, 0.42,
            x=-B/2 + 0.33,
            y=-MAIN_DEPTH/2 + 0.33,
            z=BODY_Z - 0.42
        )
        h = h.cut(notch)
    except Exception:
        pass

    try:
        h = h.combine(clean=True)
    except Exception:
        pass

    return h, B

def make_pins(n):
    solids=[]
    # Continuous square contact: 3.7 mm below PCB + 3.2 mm through wafer + 7.7 mm mating post.
    total = SOLDER_TAIL + BODY_Z + MATING_POST
    for i in range(n):
        x=(i-(n-1)/2)*PITCH
        p=(cq.Workplane("XY")
           .box(PIN_SQ,PIN_SQ,total,centered=(True,True,False))
           .translate((x,PIN_ROW_Y,-SOLDER_TAIL)))
        try:
            p = p.edges(">Z").chamfer(0.10)
            p = p.edges("<Z").chamfer(0.05)
        except Exception:
            pass
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
            a=cq.Assembly(name=f"VH3_96_{n}P_{color}_V6")
            a.add(body,name="WAFER",color=cq.Color(*rgb))
            a.add(pins,name=f"PINS_{n}",color=cq.Color(0.74,0.74,0.77))
            p=out/color/f"VH3.96_{n}P_{color}_V7_TOP_EAR_FIXED.step"
            print(p, export_step(a,p))

if __name__=="__main__":
    main()
