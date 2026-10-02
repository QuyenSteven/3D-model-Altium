import cadquery as cq
from common import ROOT, export_step

BLACK = cq.Color(0.055, 0.055, 0.055)
PIN_COLOR = cq.Color(0.73, 0.73, 0.76)
MARK_COLOR = cq.Color(0.90, 0.90, 0.90)

PIN_X = 0.50
PIN_Y = 0.30
PIN_PITCH = 2.54
PIN_ROW_FROM_EDGE = 0.90
BODY_STANDOFF = 0.50
PIN_LENGTH_FROM_BODY = 4.10
PIN_BOTTOM_Z = BODY_STANDOFF - PIN_LENGTH_FROM_BODY
PIN_EMBED_TOP = BODY_STANDOFF + 0.65

def make_body(L, D, H):
    body = (
        cq.Workplane("XY")
        .box(L, D, H, centered=(True, True, False))
        .translate((0, 0, BODY_STANDOFF))
    )
    try:
        body = body.edges("|Z").fillet(0.12)
        body = body.edges(">Z").chamfer(0.12)
    except Exception:
        pass
    return body

def make_pins(D, numbered_positions):
    raw = [idx * PIN_PITCH for _, idx in numbered_positions]
    center = (min(raw) + max(raw)) / 2
    y = -D/2 + PIN_ROW_FROM_EDGE
    shapes = []
    for pin_no, idx in numbered_positions:
        x = idx * PIN_PITCH - center
        p = (
            cq.Workplane("XY")
            .box(PIN_X, PIN_Y, PIN_EMBED_TOP - PIN_BOTTOM_Z, centered=(True, True, False))
            .translate((x, y, PIN_BOTTOM_Z))
        )
        try:
            p = p.edges("|Z").chamfer(0.02)
        except Exception:
            pass
        shapes.append(p.val())
    return cq.Compound.makeCompound(shapes)

def add_markings(assy, L, D, top_z, part_text):
    rows = [
        ("MORNSUN", 0.28*D, min(1.35, L/7.0)),
        (part_text, 0.02*D, min(1.05, L/9.0)),
        ("12V -> 12V", -0.28*D, min(0.78, L/11.0)),
    ]
    for i, (txt, yy, size) in enumerate(rows):
        try:
            m = (
                cq.Workplane("XY")
                .workplane(offset=top_z)
                .center(0, yy)
                .text(txt, size, 0.018, halign="center", valign="center")
            )
            assy.add(m, name=f"MARK_{i+1}", color=MARK_COLOR)
        except Exception:
            pass
    try:
        dot = (
            cq.Workplane("XY")
            .workplane(offset=top_z)
            .center(-L/2 + 1.10, -D/2 + 1.15)
            .circle(0.22)
            .extrude(0.020)
        )
        assy.add(dot, name="PIN1_DOT", color=MARK_COLOR)
    except Exception:
        pass

def build(name, L, D, H, pin_positions, marked):
    a = cq.Assembly(name=name.replace("-", "_"))
    a.add(make_body(L, D, H), name="BLACK_CASE", color=BLACK)
    a.add(make_pins(D, pin_positions), name="PINS", color=PIN_COLOR)
    if marked:
        add_markings(a, L, D, BODY_STANDOFF + H, name)
    return a

def main():
    out = ROOT / "generated" / "MORNSUN_B_S_WR3"
    variants = [
        ("B1212S-1WR3", 11.60, 6.00, 10.16, [(1,0),(2,1),(3,2),(4,3)]),
        ("B1212S-2WR3", 19.65, 7.05, 10.16, [(1,0),(2,1),(4,3),(6,5)]),
    ]
    for name, L, D, H, pins in variants:
        for marked, suffix in [(True, "REALISTIC"), (False, "CLEAN")]:
            p = out / f"{name}_{suffix}.step"
            print(p, export_step(build(name, L, D, H, pins, marked), p))

if __name__ == "__main__":
    main()
