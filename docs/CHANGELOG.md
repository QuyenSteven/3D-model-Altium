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
