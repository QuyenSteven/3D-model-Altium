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

def pin_x_positions(L, numbered_positions, pin1_from_left):
    # MORNSUN drawings define the first pin by a package-edge offset.
    # Do NOT center the pin group automatically; 2WR3 is intentionally asymmetric.
    return {
        pin_no: -L/2 + pin1_from_left + idx * PIN_PITCH
        for pin_no, idx in numbered_positions
    }

def make_pins(L, D, numbered_positions, pin1_from_left, row_side):
    y = row_side * (D/2 - PIN_ROW_FROM_EDGE)
    xpos = pin_x_positions(L, numbered_positions, pin1_from_left)
    shapes = []
    for pin_no, _ in numbered_positions:
        p = (
            cq.Workplane("XY")
            .box(PIN_X, PIN_Y, PIN_EMBED_TOP - PIN_BOTTOM_Z, centered=(True, True, False))
            .translate((xpos[pin_no], y, PIN_BOTTOM_Z))
        )
        try:
            p = p.edges("|Z").chamfer(0.02)
        except Exception:
            pass
        shapes.append(p.val())
    return cq.Compound.makeCompound(shapes), xpos

def add_markings(assy, L, D, top_z, part_text, pin1_x, row_side):
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
            .center(pin1_x, row_side * (D/2 - 1.15))
            .circle(0.22)
            .extrude(0.020)
        )
        assy.add(dot, name="PIN1_DOT", color=MARK_COLOR)
    except Exception:
        pass

def build(name, L, D, H, pin_positions, pin1_from_left, marked, row_side):
    a = cq.Assembly(name=name.replace("-", "_"))
    a.add(make_body(L, D, H), name="BLACK_CASE", color=BLACK)
    pins, xpos = make_pins(L, D, pin_positions, pin1_from_left, row_side)
    a.add(pins, name="PINS", color=PIN_COLOR)
    if marked:
        add_markings(a, L, D, BODY_STANDOFF + H, name, xpos[1], row_side)
    return a

def main():
    out = ROOT / "generated" / "MORNSUN_B_S_WR3"
    variants = [
        # B_S-1WR3 official drawing:
        # pin 1 edge offset = 1.99 mm; pins 1-2-3-4 at 2.54 mm grid.
        ("B1212S-1WR3", 11.60, 6.00, 10.16,
         [(1,0),(2,1),(3,2),(4,3)], 1.99, -1),

        # B_S-2WR3 official drawing:
        # pin 1 edge offset = 2.21 mm nominal; single-output pins 1-2-4-6.
        # This group is NOT centered inside the 19.65 mm body.
        ("B1212S-2WR3", 19.65, 7.05, 10.16,
         [(1,0),(2,1),(4,3),(6,5)], 2.21, +1),
    ]

    for name, L, D, H, pins, pin1_from_left, row_side in variants:
        for marked, suffix in [(True, "REALISTIC"), (False, "CLEAN")]:
            p = out / f"{name}_{suffix}.step"
            print(
                p,
                export_step(
                    build(name, L, D, H, pins, pin1_from_left, marked, row_side),
                    p,
                ),
            )

if __name__ == "__main__":
    main()
