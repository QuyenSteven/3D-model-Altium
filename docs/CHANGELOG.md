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
