# CHANGELOG

## 2026-10-03 — Baseline import

### Added
- Project context và acceptance rules.
- Baseline dimensions/lessons cho RTL8367S, HFD4, XH2.54, VH3.96, CBB, SFP cage, AMC1200.

### Important corrections retained
- XH2.54/VH3.96: bỏ housing skeletal; chuyển sang molded solid.
- XH2.54/VH3.96: mở rộng color set lên 10 màu gồm brown/gray/purple.
- AMC1200: qua nhiều iteration; canonical geometry hiện là **V4 proportional**.
- RTL8367S: không scale model theo khoảng pad đo 14.4 mm; overall package lead span giữ 16 mm.
- CBB: tổ chức theo physical case size, không chỉ theo voltage.

### Canonical preference
- AMC1200: V4 proportional / V4 clean.
- XH2.54: V3 fixed, 10-color generation.
- VH3.96: V3 fixed, 10-color generation.

## 2026-10-03 — MORNSUN B1212S WR3
- Added B1212S-1WR3 (1 W) and B1212S-2WR3 (2 W) SIP STEP generators.
- 1 W body: 11.60 x 6.00 x 10.16 mm; pins 1,2,3,4 on 2.54 mm grid.
- 2 W body: 19.65 x 7.05 x 10.16 mm; single-output pins 1,2,4,6 on 2.54 mm grid.
- Pin row kept 0.90 mm from long edge; pin section 0.50 x 0.30 mm; pin length from body 4.10 mm.
- Both REALISTIC and CLEAN variants are generated.
## 2026-10-03 — MORNSUN B1212S-2WR3 orientation fix

- Corrected B1212S-2WR3 pin-row side after Altium visual check against the real part photo.
- 2WR3 pin row is now on the opposite long edge of the package (row_side = +1).
- 1WR3 keeps its previous orientation (row_side = -1).
- Pin grid/pitch and package dimensions are unchanged; this is an orientation correction only.



## 2026-10-03 — MORNSUN B_S WR3 pin-position correction

### B1212S-2WR3
- Official MORNSUN mechanical drawing checked.
- Single-output pin numbers: 1, 2, 4, 6.
- Grid: 2.54 mm.
- Pin 1 center starts 2.21 mm nominal from the left body edge.
- Correct pin spacings: 1→2 = 2.54 mm, 2→4 = 5.08 mm, 4→6 = 5.08 mm, 1→6 = 12.70 mm.
- Important: the 2WR3 pin group is **not centered** in the 19.65 mm body. Previous centered generator geometry was wrong.
- Pin row offset from long package edge remains 0.90 mm.
- Canonical baseline becomes regenerated B1212S-2WR3 after commit ec8a9d1.

### B1212S-1WR3
- Official drawing confirms pin 1 edge offset 1.99 mm; with 7.62 mm span inside 11.60 mm body this row is centered as expected.
