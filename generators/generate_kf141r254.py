import cadquery as cq
from common import ROOT, export_step

PITCH=2.54
BODY_D=13.80
BODY_H=11.50
BUTTON_TOP=12.765
PIN_ROW_FRONT_Y=-1.053145
PIN_ROW_REAR_Y=4.027003
FIRST_POLE_FROM_LEFT=0.95
PIN_X_W=0.50
PIN_Y_MAIN=0.70
PIN_Y_TIP=0.55
PIN_Z_MIN=-3.50
PIN_Z_SHOULDER=-2.70
PIN_Z_TOP=0.90
FRONT_FACE_Y=-BODY_D/2
WIRE_HOLE_Z=4.10
WIRE_HOLE_D=1.95
REAR_RAIL_DEPTH=2.00
TOP_OPEN_Z=8.55

GREEN=cq.Color(0.23,0.62,0.31)
ORANGE=cq.Color(1.00,0.42,0.02)
TIN=cq.Color(0.74,0.74,0.77)
DARK=cq.Color(0.28,0.30,0.30)

def body_len(n):
    return (n+1)*PITCH

def pole_xs(n):
    L=body_len(n)
    left=-L/2
    return [left+FIRST_POLE_FROM_LEFT+i*PITCH for i in range(n)]

def make_housing(n):
    L=body_len(n)
    lower=cq.Workplane("XY").box(L,BODY_D,TOP_OPEN_Z,centered=(True,True,False))
    front_upper=(cq.Workplane("XY").box(L,2.45,BODY_H-TOP_OPEN_Z,centered=(True,True,False))
                 .translate((0,FRONT_FACE_Y+1.225,TOP_OPEN_Z)))
    rear_rail=(cq.Workplane("XY").box(L,REAR_RAIL_DEPTH,BODY_H-TOP_OPEN_Z,centered=(True,True,False))
               .translate((0,BODY_D/2-REAR_RAIL_DEPTH/2,TOP_OPEN_Z)))
    cheek_w=0.72
    cheek_depth=BODY_D-2.45-REAR_RAIL_DEPTH
    cheek_y=FRONT_FACE_Y+2.45+cheek_depth/2
    left=(cq.Workplane("XY").box(cheek_w,cheek_depth,BODY_H-TOP_OPEN_Z,centered=(True,True,False))
          .translate((-L/2+cheek_w/2,cheek_y,TOP_OPEN_Z)))
    right=(cq.Workplane("XY").box(cheek_w,cheek_depth,BODY_H-TOP_OPEN_Z,centered=(True,True,False))
           .translate((L/2-cheek_w/2,cheek_y,TOP_OPEN_Z)))
    h=lower.union(front_upper).union(rear_rail).union(left).union(right)
    for x in pole_xs(n):
        hole=(cq.Workplane("XZ",origin=(0,FRONT_FACE_Y-0.05,0)).center(x,WIRE_HOLE_Z)
              .circle(WIRE_HOLE_D/2).extrude(2.20))
        h=h.cut(hole)
    xs=pole_xs(n)
    for i in range(n-1):
        x=(xs[i]+xs[i+1])/2
        seam=(cq.Workplane("XY").box(0.055,0.35,6.6,centered=(True,True,False))
              .translate((x,FRONT_FACE_Y+0.175,1.00)))
        h=h.cut(seam)
    try: h=h.edges("|Z").fillet(0.10)
    except Exception: pass
    return h

def make_button(x):
    pts=[(-5.95,8.50),(-5.55,10.10),(-4.55,11.80),(-3.65,12.55),
         (-2.95,12.55),(-3.05,11.45),(-3.60,9.75),(-4.55,8.25)]
    w=cq.Workplane("YZ").moveTo(*pts[0])
    for p in pts[1:]: w=w.lineTo(*p)
    arm=w.close().extrude(0.60,both=True).translate((x,0,0))
    pad=(cq.Workplane("XY").box(1.32,2.05,0.72,centered=(True,True,False))
         .translate((x,-3.95,11.72)))
    try:
        slot=(cq.Workplane("XY").box(0.62,1.10,0.40,centered=(True,True,False))
              .translate((x,-3.95,12.08)))
        pad=pad.cut(slot)
    except Exception: pass
    return arm.union(pad)

def make_pin(x,y):
    lower=(cq.Workplane("XY").workplane(offset=PIN_Z_MIN).center(x,y)
           .rect(PIN_X_W,PIN_Y_TIP)
           .workplane(offset=PIN_Z_SHOULDER-PIN_Z_MIN).rect(PIN_X_W,PIN_Y_MAIN)
           .loft(combine=True))
    shank=(cq.Workplane("XY").box(PIN_X_W,PIN_Y_MAIN,PIN_Z_TOP-PIN_Z_SHOULDER,centered=(True,True,False))
           .translate((x,y,PIN_Z_SHOULDER)))
    return lower.union(shank)

def make_pins(n):
    vals=[]
    for x in pole_xs(n):
        vals.append(make_pin(x,PIN_ROW_FRONT_Y).val())
        vals.append(make_pin(x,PIN_ROW_REAR_Y).val())
    return cq.Compound.makeCompound(vals)

def build(n):
    a=cq.Assembly(name=f"KF141R_2_54_{n}P_V2")
    a.add(make_housing(n),name="GREEN_HOUSING",color=GREEN)
    a.add(make_pins(n),name=f"THT_PINS_{2*n}",color=TIN)
    for i,x in enumerate(pole_xs(n),1):
        a.add(make_button(x),name=f"ORANGE_BUTTON_{i}",color=ORANGE)
    return a

if __name__=="__main__":
    out=ROOT/"generated"/"KF141R-2.54"
    out.mkdir(parents=True,exist_ok=True)
    for n in range(2,11):
        p=out/f"KF141R-2.54-{n}P_V2_PHOTO_MATCHED.step"
        print(p,export_step(build(n),p))
