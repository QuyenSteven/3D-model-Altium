import csv
import cadquery as cq
from common import ROOT, export_step

RED=cq.Color(0.72,0.025,0.025)
TIN=cq.Color(0.72,0.72,0.76)
BODY_CLEARANCE=1.8
TAIL=3.0

def body(W,T,H):
    b=cq.Workplane("XY").box(W,T,H,centered=(True,True,False)).translate((0,0,BODY_CLEARANCE))
    try: b=b.edges().fillet(min(0.65,W/10,T/4,H/8))
    except Exception: pass
    return b

def leads(P,d,H):
    ztop=BODY_CLEARANCE+min(2.0,H*0.25)
    solids=[]
    for x in (-P/2,P/2):
        p=cq.Workplane("XY").center(x,0).circle(d/2).extrude(ztop+TAIL).translate((0,0,-TAIL))
        solids.append(p.val())
    return cq.Compound.makeCompound(solids)

def main():
    table=ROOT/"models"/"Capacitors"/"CBB"/"CBB22_COMMON_CASES_100V-1200V.csv"
    out=ROOT/"generated"/"CBB"
    with table.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            V=int(float(row["voltage_V"]))
            W=float(row["W_mm"]); H=float(row["H_mm"]); T=float(row["T_mm"])
            P=float(row["pitch_P_mm"]); d=float(row["lead_d_mm"])
            a=cq.Assembly(name=f"CBB22_{V}V")
            a.add(body(W,T,H),name="RED_BODY",color=RED)
            a.add(leads(P,d,H),name="TINNED_LEADS",color=TIN)
            fn=f"CBB22_{V}V_W{W:g}_H{H:g}_T{T:g}_P{P:g}_D{d:g}.step"
            print(out/f"{V}V"/fn, export_step(a,out/f"{V}V"/fn))

if __name__=="__main__":
    main()
