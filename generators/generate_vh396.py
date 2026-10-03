import cadquery as cq
import shutil
from common import ROOT, COLORS, export_step

PITCH=3.96
BODY_D=9.40
BODY_H=8.50
PIN_SQ=1.14
TAIL=3.20
POST_TOP=7.70
FLOOR_H=1.55
PIN_ROW_Y=-1.40  # toward latch/front side; official B2P-VH fab relation is 2.0 mm front vs 4.8 mm rear

def body_len(n):
    return (n-1)*PITCH + 3.90

def box(L,D,H,x=0,y=0,z=0):
    return cq.Workplane("XY").box(L,D,H,centered=(True,True,False)).translate((x,y,z))

def make_housing(n):
    L=body_len(n)
    side_wall=1.05; back_wall=1.15; front_wall=1.10; front_wall_h=4.05
    h=box(L,BODY_D,FLOOR_H)
    h=h.union(box(L,back_wall,BODY_H-FLOOR_H,y=BODY_D/2-back_wall/2,z=FLOOR_H))
    side_depth=BODY_D-back_wall
    h=h.union(box(side_wall,side_depth,BODY_H-FLOOR_H,x=-L/2+side_wall/2,y=-back_wall/2,z=FLOOR_H))
    h=h.union(box(side_wall,side_depth,BODY_H-FLOOR_H,x=L/2-side_wall/2,y=-back_wall/2,z=FLOOR_H))
    h=h.union(box(L,front_wall,front_wall_h-FLOOR_H,y=-BODY_D/2+front_wall/2,z=FLOOR_H))
    cheek_w=min(1.15,L/4)
    for sx in (-1,1):
        h=h.union(box(cheek_w,1.35,BODY_H-front_wall_h,
                      x=sx*(L/2-cheek_w/2),y=-BODY_D/2+0.675,z=front_wall_h))
    bridge_w=min(2.60,max(1.80,L*0.28))
    h=h.union(box(bridge_w,1.45,2.00,y=-BODY_D/2+1.25,z=3.20))
    h=h.union(box(bridge_w*0.80,1.95,0.72,y=-BODY_D/2+1.58,z=5.05))
    slot_xs=[-PITCH/2,PITCH/2] if n==2 else [-L/2+1.55,L/2-1.55]
    for x in slot_xs:
        h=h.cut(box(1.20,0.78,0.85,x=x,y=-BODY_D/2+0.39,z=0))
    h=h.cut(box(min(1.45,L*0.22),0.75,0.80,y=-BODY_D/2+0.38,z=front_wall_h-0.25))
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
            body,L=make_housing(n); pins=make_pins(n)
            a=cq.Assembly(name=f"VH3_96_{n}P_{color}")
            a.add(body,name="HOUSING",color=cq.Color(*rgb))
            a.add(pins,name=f"PINS_{n}",color=cq.Color(0.74,0.74,0.77))
            p=out/color/f"VH3.96_{n}P_{color}_V4_LOCKSIDE_FIXED.step"
            print(p, export_step(a,p))

if __name__=="__main__":
    main()
