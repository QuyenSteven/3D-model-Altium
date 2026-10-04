import cadquery as cq
from common import ROOT, export_step

BODY_X=46.90
BODY_Y=27.80
BODY_Z=21.80
PIN_SQ=0.80
PIN_TAIL=5.02
PIN_EMBED=0.75

PIN_POS={
    1:(-21.25,-3.90),
    2:(-21.25,+3.90),
    3:(+21.25,+11.40),
    4:(+21.25,-11.40),
}

MODELS=[
    ("HLK-10M03","3.3V"),
    ("HLK-10M05","5V"),
    ("HLK-10M09","9V"),
    ("HLK-10M12","12V"),
    ("HLK-10M15","15V"),
    ("HLK-10M24","24V"),
]

CASE=cq.Color(0.065,0.085,0.105)
PIN_COLOR=cq.Color(0.72,0.72,0.76)
MARK=cq.Color(0.86,0.87,0.88)

def body():
    b=cq.Workplane("XY").box(BODY_X,BODY_Y,BODY_Z,centered=(True,True,False))
    try:
        b=b.edges("|Z").fillet(0.28)
        b=b.edges(">Z").chamfer(0.18)
    except Exception:
        pass
    return b

def pins():
    vals=[]
    for n,(x,y) in PIN_POS.items():
        p=(cq.Workplane("XY")
           .box(PIN_SQ,PIN_SQ,PIN_TAIL+PIN_EMBED,centered=(True,True,False))
           .translate((x,y,-PIN_TAIL)))
        vals.append(p.val())
    return cq.Compound.makeCompound(vals)

def mark(txt,y,size,h=0.018):
    return (cq.Workplane("XY").workplane(offset=BODY_Z)
            .center(0,y).text(txt,size,h,halign="center",valign="center"))

def build(model,voltage,realistic=False):
    a=cq.Assembly(name=model)
    a.add(body(),name="MOLDED_CASE",color=CASE)
    a.add(pins(),name="PINS_1_2_3_4",color=PIN_COLOR)
    if realistic:
        try:
            a.add(mark("HI-LINK",4.5,3.6),name="MARK_BRAND",color=MARK)
            a.add(mark(model,0.0,2.5),name="MARK_MODEL",color=MARK)
            a.add(mark(f"10W  {voltage}",-4.2,1.9),name="MARK_OUTPUT",color=MARK)
        except Exception:
            pass
    return a

def main():
    out=ROOT/"generated"/"HI_LINK"/"HLK-10M"
    for model,voltage in MODELS:
        for suffix,realistic in (("REALISTIC",True),("CLEAN",False)):
            p=out/f"HI-LINK_{model}_{suffix}.step"
            print(p, export_step(build(model,voltage,realistic),p))

if __name__=="__main__":
    main()
