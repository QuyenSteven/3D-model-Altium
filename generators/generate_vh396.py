import cadquery as cq
import shutil
from common import ROOT, COLORS, export_step

PITCH=3.96
BODY_D=9.40
BODY_H=8.50
PIN_SQ=1.14
TAIL=3.20
POST_TOP=7.45
FLOOR_H=1.55

# Latch/front side is -Y. Pin row is offset toward the latch.
PIN_ROW_Y=-1.40

def body_len(n):
    return (n-1)*PITCH + 3.90

def box(L,D,H,x=0,y=0,z=0):
    return cq.Workplane("XY").box(L,D,H,centered=(True,True,False)).translate((x,y,z))

def make_housing(n):
    L=body_len(n)

    # Same molded-body architecture as corrected XH2.54, scaled to VH.
    side_wall=1.12
    back_wall=1.20
    front_wall=1.08
    front_wall_h=3.70

    h=box(L,BODY_D,FLOOR_H)
    h=h.union(box(L,back_wall,BODY_H-FLOOR_H,
                  y=BODY_D/2-back_wall/2,z=FLOOR_H))

    side_depth=BODY_D-back_wall
    h=h.union(box(side_wall,side_depth,BODY_H-FLOOR_H,
                  x=-L/2+side_wall/2,y=-back_wall/2,z=FLOOR_H))
    h=h.union(box(side_wall,side_depth,BODY_H-FLOOR_H,
                  x=L/2-side_wall/2,y=-back_wall/2,z=FLOOR_H))

    h=h.union(box(L,front_wall,front_wall_h-FLOOR_H,
                  y=-BODY_D/2+front_wall/2,z=FLOOR_H))

    shoulder_w=min(1.35,L/4)
    shoulder_d=1.30
    for sx in (-1,1):
        h=h.union(box(shoulder_w,shoulder_d,BODY_H-front_wall_h,
                      x=sx*(L/2-shoulder_w/2),
                      y=-BODY_D/2+shoulder_d/2,
                      z=front_wall_h))

    latch_w=min(2.55,max(1.80,L*0.24))
    h=h.union(box(latch_w,1.55,1.55,
                  y=-BODY_D/2+1.25,z=front_wall_h-0.35))
    h=h.union(box(latch_w*0.78,1.95,0.58,
                  y=-BODY_D/2+1.55,z=front_wall_h+0.95))

    slot_xs=[-PITCH/2,PITCH/2] if n==2 else [-L/2+1.70,L/2-1.70]
    for x in slot_xs:
        h=h.cut(box(1.35,0.85,0.90,
                    x=x,y=-BODY_D/2+0.425,z=0))

    h=h.cut(box(min(1.60,max(1.05,L*0.16)),0.82,0.78,
                y=-BODY_D/2+0.41,z=front_wall_h-0.18))

    try: h=h.edges("|Z").fillet(0.10)
    except Exception: pass
    try: h=h.combine(clean=True)
    except Exception: pass
    return h,L

def make_pins(n):
    solids=[]
    for i in range(n):
        x=(i-(n-1)/2)*PITCH
        p=cq.Workplane("XY").box(PIN_SQ,PIN_SQ,POST_TOP+TAIL,centered=(True,True,False)).translate((x,PIN_ROW_Y,-TAIL))
        solids.append(p.val())
    return cq.Compound.makeCompound(solids)

def main():
    out=ROOT/"generated"/"VH3.96"
    if out.exists():
        shutil.rmtree(out)

    for color,rgb in COLORS.items():
        for n in range(2,11):
            body,L=make_housing(n)
            pins=make_pins(n)
            a=cq.Assembly(name=f"VH3_96_{n}P_{color}_V5_XHSTYLE")
            a.add(body,name="HOUSING",color=cq.Color(*rgb))
            a.add(pins,name=f"PINS_{n}",color=cq.Color(0.74,0.74,0.77))
            p=out/color/f"VH3.96_{n}P_{color}_V5_XHSTYLE.step"
            print(p,export_step(a,p))

if __name__=="__main__":
    main()
