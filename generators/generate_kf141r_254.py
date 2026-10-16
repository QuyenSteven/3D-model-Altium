import cadquery as cq
import shutil
from common import ROOT, export_step

PITCH=2.54
BODY_D=13.80
BODY_H=11.50
BUTTON_TOP=12.765
TAIL_Z_MIN=-3.50
PIN_X_W=0.50
PIN_Y_MAIN=0.70
PIN_Y_TIP=0.55

# Extracted from exact EasyEDA/LCSC C475132 reference STEP.
PIN_ROW_FRONT_Y=-1.053145
PIN_ROW_REAR_Y=4.027003
PIN_FIRST_FROM_LEFT=0.95

GREEN=cq.Color(0.18,0.58,0.27)
ORANGE=cq.Color(0.96,0.40,0.04)
TIN=cq.Color(0.72,0.72,0.76)

def body_len(n):
    return (n+1)*PITCH

def pole_xs(n):
    L=body_len(n)
    left=-L/2
    return [left+PIN_FIRST_FROM_LEFT+i*PITCH for i in range(n)]

def make_body(n):
    L=body_len(n)
    body=cq.Workplane("XY").box(L,BODY_D,BODY_H,centered=(True,True,False))
    try:
        body=body.edges("|Z").fillet(0.10)
        body=body.edges(">Z").chamfer(0.10)
    except Exception:
        pass
    cap=(cq.Workplane("XY").box(L,2.00,0.65,centered=(True,True,False))
         .translate((0,BODY_D/2-1.00,BODY_H-0.65)))
    body=body.union(cap)
    for x in pole_xs(n):
        port=(cq.Workplane("XY").box(1.55,1.45,1.65,centered=(True,True,False))
              .translate((x,-BODY_D/2+0.725,3.45)))
        body=body.cut(port)
    for i in range(n-1):
        x=(pole_xs(n)[i]+pole_xs(n)[i+1])/2
        seam=(cq.Workplane("XY").box(0.055,0.30,8.7,centered=(True,True,False))
              .translate((x,-BODY_D/2+0.15,1.10)))
        body=body.cut(seam)
    return body

def make_button(x):
    pts=[(-6.45,10.00),(-6.45,11.45),(-5.90,12.65),(-5.15,BUTTON_TOP),
         (-3.55,12.00),(-3.20,10.25),(-3.65,9.95)]
    w=cq.Workplane("YZ").moveTo(*pts[0])
    for p in pts[1:]:
        w=w.lineTo(*p)
    return w.close().extrude(0.72,both=True).translate((x,0,0))

def make_pin(x,y):
    lower=(cq.Workplane("XY").workplane(offset=TAIL_Z_MIN)
           .center(x,y).rect(PIN_X_W,PIN_Y_TIP)
           .workplane(offset=0.80).rect(PIN_X_W,PIN_Y_MAIN)
           .loft(combine=True))
    shank=(cq.Workplane("XY").box(PIN_X_W,PIN_Y_MAIN,3.55,centered=(True,True,False))
           .translate((x,y,-2.70)))
    return lower.union(shank)

def make_pins(n):
    vals=[]
    for x in pole_xs(n):
        vals.append(make_pin(x,PIN_ROW_FRONT_Y).val())
        vals.append(make_pin(x,PIN_ROW_REAR_Y).val())
    return cq.Compound.makeCompound(vals)

def make_contacts(n):
    vals=[]
    for x in pole_xs(n):
        c=(cq.Workplane("XY").box(1.00,0.18,0.52,centered=(True,True,False))
           .translate((x,-BODY_D/2+1.42,3.93)))
        vals.append(c.val())
    return cq.Compound.makeCompound(vals)

def build(n):
    a=cq.Assembly(name=f"KF141R_2_54_{n}P")
    a.add(make_body(n),name="GREEN_HOUSING",color=GREEN)
    a.add(make_pins(n),name=f"SOLDER_PINS_{2*n}",color=TIN)
    a.add(make_contacts(n),name="FRONT_CONTACTS",color=TIN)
    for i,x in enumerate(pole_xs(n),1):
        a.add(make_button(x),name=f"BUTTON_{i}",color=ORANGE)
    return a

def main():
    out=ROOT/"generated"/"KF141R-2.54"
    if out.exists():
        shutil.rmtree(out)
    for n in range(2,11):
        p=out/f"KF141R-2.54-{n}P.step"
        print(p,export_step(build(n),p))

if __name__=="__main__":
    main()
