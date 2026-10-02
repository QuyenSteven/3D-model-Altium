from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]

COLORS = {
    "WHITE":  (0.94, 0.94, 0.91),
    "BLACK":  (0.055, 0.055, 0.055),
    "RED":    (0.84, 0.045, 0.035),
    "BLUE":   (0.045, 0.20, 0.80),
    "GREEN":  (0.045, 0.52, 0.11),
    "YELLOW": (0.95, 0.78, 0.025),
    "ORANGE": (0.95, 0.33, 0.025),
    "BROWN":  (0.34, 0.14, 0.055),
    "GRAY":   (0.42, 0.44, 0.47),
    "PURPLE": (0.43, 0.10, 0.58),
}

def export_step(assembly, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    assembly.save(str(path), exportType="STEP")
    return validate_step(path)

def validate_step(path):
    model = cq.importers.importStep(str(path))
    comp = cq.Compound.makeCompound(model.vals())
    b = comp.BoundingBox()
    return (round(b.xlen, 3), round(b.ylen, 3), round(b.zlen, 3),
            round(b.zmin, 3), round(b.zmax, 3))
