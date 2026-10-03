import cadquery as cq
import shutil
from common import ROOT, COLORS, export_step

# VH3.96 SHOU HAN straight male PCB header.
# Canonical geometry is reference-driven from exact EasyEDA/LCSC source models:
# C5379868..C5379876 and especially the clean 4P C5379870 section.
PITCH = 3.96

# Exact/observed pin geometry from C5379870 pin-center section.
PIN_ROW_Y = 1.35
PIN_FULL = 1.13
PIN_TIP = 0.53
PIN_Z0 = -3.50
PIN_Z1 = -2.380385
PIN_Z2 = 8.980385
PIN_Z3 = 10.10

# Exact center YZ plastic profile extracted from C5379870 at X=0.
# Coordinates are (Y, Z), mm.
BODY_PROFILE = [
    (3.35, 7.90),
    (3.35, 3.10),
    (-3.35, 3.10),
    (-3.35, 0.50),
    (4.35, 0.50),
    (4.35, 7.30),
    (4.85, 7.30),
    (4.85, 7.90),
    (4.501666, 9.20),
    (3.698334, 9.20),
]

def body_len(n):
    # Exact SHOU HAN family is essentially N * 3.96:
    # 4P=15.84, 5P=19.80, 9P=35.64, 10P=39.60.
    return n * PITCH

def make_housing(n):
    B = body_len(n)
    w = cq.Workplane("YZ").moveTo(*BODY_PROFILE[0])
    for pt in BODY_PROFILE[1:]:
        w = w.lineTo(*pt)
    body = w.close().extrude(B/2, both=True)
    return body, B

def make_pin(x):
    # Bottom tapered end.
    bottom = (
        cq.Workplane("XY")
        .workplane(offset=PIN_Z0)
        .center(x, PIN_ROW_Y)
        .rect(PIN_TIP, PIN_TIP)
        .workplane(offset=PIN_Z1-PIN_Z0)
        .rect(PIN_FULL, PIN_FULL)
        .loft(combine=True)
    )

    # Full square middle shank.
    shank = (
        cq.Workplane("XY")
        .box(PIN_FULL, PIN_FULL, PIN_Z2-PIN_Z1, centered=(True, True, False))
        .translate((x, PIN_ROW_Y, PIN_Z1))
    )

    # Top tapered end.
    top = (
        cq.Workplane("XY")
        .workplane(offset=PIN_Z2)
        .center(x, PIN_ROW_Y)
        .rect(PIN_FULL, PIN_FULL)
        .workplane(offset=PIN_Z3-PIN_Z2)
        .rect(PIN_TIP, PIN_TIP)
        .loft(combine=True)
    )
    return bottom.union(shank).union(top)

def make_pins(n):
    solids=[]
    for i in range(n):
        x=(i-(n-1)/2)*PITCH
        solids.append(make_pin(x).val())
    return cq.Compound.makeCompound(solids)

def main():
    out=ROOT/"generated"/"VH3.96"
    if out.exists():
        shutil.rmtree(out)

    for color,rgb in COLORS.items():
        for n in range(2,11):
            body,B=make_housing(n)
            pins=make_pins(n)
            a=cq.Assembly(name=f"VH3_96_{n}P_{color}_V9")
            a.add(body,name="HOUSING_REFERENCE_PROFILE",color=cq.Color(*rgb))
            a.add(pins,name=f"PINS_{n}",color=cq.Color(0.74,0.74,0.77))
            p=out/color/f"VH3.96_{n}P_{color}_V9_EXACT_PROFILE.step"
            print(p, export_step(a,p))

if __name__=="__main__":
    main()
