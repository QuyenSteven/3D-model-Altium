import cadquery as cq
from common import ROOT, export_step

L=10.0
W=6.5
XPOS=[-3.8,-0.6,1.6,3.8]
PIN_W=0.40

def rounded_body(z0,z1):
    b=cq.Workplane("XY").box(L,W,z1-z0,centered=(True,True,False)).translate((0,0,z0))
    try: b=b.edges().fillet(0.12)
    except Exception: pass
    return b

def build_tht():
    z0=0.30; z1=5.70; bottom=-3.30; row=5.08/2
    pins=[]
    for x in XPOS:
        for y in (-row,row):
            p=cq.Workplane("XY").box(PIN_W,PIN_W,z0-bottom,centered=(True,True,False)).translate((x,y,bottom))
            pins.append(p.val())
    a=cq.Assembly(name="HFD4_THT")
    a.add(rounded_body(z0,z1),name="RELAY_BODY",color=cq.Color(0.93,0.93,0.90))
    a.add(cq.Compound.makeCompound(pins),name="TERMINALS_8",color=cq.Color(0.72,0.72,0.74))
    return a

def build_smt():
    ztop=5.65; z0=0.48; root=5.08/2; tip=7.50/2; t=0.10
    body=rounded_body(z0,ztop)
    prof=[(root-0.10,0.62),(root+0.24,0.62),(root+0.42,0.12),
          (tip,0.12),(tip,0.00),(root+0.31,0.00),(root+0.12,0.50),(root-0.10,0.50)]
    def lead(sign):
        pts=prof if sign>0 else [(-y,z) for y,z in reversed(prof)]
        w=cq.Workplane("YZ").moveTo(*pts[0])
        for p in pts[1:]: w=w.lineTo(*p)
        return w.close().extrude(PIN_W/2,both=True)
    lp,ln=lead(1),lead(-1)
    pins=[]
    for x in XPOS:
        pins += [lp.translate((x,0,0)).val(),ln.translate((x,0,0)).val()]
    a=cq.Assembly(name="HFD4_STANDARD_SMT")
    a.add(body,name="RELAY_BODY",color=cq.Color(0.93,0.93,0.90))
    a.add(cq.Compound.makeCompound(pins),name="TERMINALS_8",color=cq.Color(0.72,0.72,0.74))
    return a

if __name__=="__main__":
    out=ROOT/"generated"/"HFD4"
    print(export_step(build_tht(),out/"HFD4_THT_DIP.step"))
    print(export_step(build_smt(),out/"HFD4_SMT_STANDARD.step"))
