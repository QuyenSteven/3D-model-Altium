import cadquery as cq
from pathlib import Path
import shutil
from common import ROOT, COLORS, export_step

PITCH=2.54
BODY_D=5.80
BODY_H=7.10
PIN_SQ=0.64
TAIL=3.20
POST_TOP=5.65
FLOOR_H=1.35
PIN_ROW_FROM_LOCK_EDGE=2.35
PIN_ROW_Y=-BODY_D/2+PIN_ROW_FROM_LOCK_EDGE  # -0.55 mm: toward latch/lock side

def body_len(n):
    return 7.50 + (n-2)*PITCH

def box(L,D,H,x=0,y=0,z=0):
    return cq.Workplane("XY").box(L,D,H,centered=(True,True,False)).translate((x,y,z))

def make_housing(n):
    L=body_len(n)
    side_wall=0.95; back_wall=1.00; front_wall=0.95; front_wall_h=3.10
    floor=box(L,BODY_D,FLOOR_H)
    back=box(L,back_wall,BODY_H-FLOOR_H,y=BODY_D/2-back_wall/2,z=FLOOR_H)
    side_depth=BODY_D-back_wall
    left=box(side_wall,side_depth,BODY_H-FLOOR_H,x=-L/2+side_wall/2,y=-back_wall/2,z=FLOOR_H)
    right=box(side_wall,side_depth,BODY_H-FLOOR_H,x=L/2-side_wall/2,y=-back_wall/2,z=FLOOR_H)
    front=box(L,front_wall,front_wall_h-FLOOR_H,y=-BODY_D/2+front_wall/2,z=FLOOR_H)
    h=floor.union(back).union(left).union(right).union(front)
    shoulder_w=min(1.05,L/4)
    for sx in (-1,1):
        h=h.union(box(shoulder_w,1.05,BODY_H-front_wall_h,
                      x=sx*(L/2-shoulder_w/2),y=-BODY_D/2+0.525,z=front_wall_h))
    bridge_w=min(1.75,max(1.20,L*0.22))
    h=h.union(box(bridge_w,1.15,1.50,y=-BODY_D/2+0.95,z=2.55))
    h=h.union(box(bridge_w*0.80,1.50,0.55,y=-BODY_D/2+1.22,z=3.82))
    slot_xs=[-PITCH/2,PITCH/2] if n==2 else [-L/2+1.40,L/2-1.40]
    for x in slot_xs:
        h=h.cut(box(1.05,0.70,0.75,x=x,y=-BODY_D/2+0.35,z=0))
    h=h.cut(box(min(1.20,max(0.85,L*0.17)),0.70,0.72,
                y=-BODY_D/2+0.35,z=front_wall_h-0.15))
    try: h=h.edges("|Z").fillet(0.08)
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
    out=ROOT/"generated"/"XH2.54"
    if out.exists():
        shutil.rmtree(out)
    for color,rgb in COLORS.items():
        for n in range(2,11):
            body,L=make_housing(n); pins=make_pins(n)
            a=cq.Assembly(name=f"XH2_54_{n}P_{color}")
            a.add(body,name="HOUSING",color=cq.Color(*rgb))
            a.add(pins,name=f"PINS_{n}",color=cq.Color(0.74,0.74,0.77))
            p=out/color/f"XH2.54_{n}P_{color}_V5_LOCKSIDE_FIXED.step"
            print(p, export_step(a,p))

if __name__=="__main__":
    main()
