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

## 2026-10-03 — XH2.54 pin-row correction

- Rà lại XH2.54 top-entry header: hàng chân không nằm đúng tâm theo chiều sâu housing.
- Giữ nguyên pitch 2.54 mm và vị trí X của các pin.
- Với body depth 5.80 mm, đặt pin-row Y = +0.55 mm, tương đương cách rear/plain edge 2.35 mm.
- Áp dụng cho toàn bộ 2P..10P và 10 màu.
- Không thay đổi body envelope, màu, hoặc pitch.

## 2026-10-03 — XH2.54 latch-side pin-row correction

- V4 đặt pin-row lệch đúng độ lớn nhưng **sai phía**: gần lưng kín.
- Housing generator quy ước latch/front ở Y âm, nên pin-row đúng phải là Y = -0.55 mm.
- Giữ khoảng cách từ latch/front edge đến pin-row = 2.35 mm với body depth 5.80 mm.
- Áp dụng toàn bộ 2P..10P, 10 màu; canonical mới: V5_LOCKSIDE_FIXED.
- Generator xóa thư mục generated/XH2.54 cũ trước khi regenerate để tránh lẫn version stale.

## 2026-10-03 — VH3.96 pin-row / latch-side correction

- Rà lại BxP-VH top-entry theo JST drawing + footprint reference: hàng chân không nằm giữa theo chiều sâu housing.
- Trong quy ước generator, latch/front ở Y âm; pin-row canonical chuyển sang Y = -1.40 mm.
- Lý do: footprint B2P-VH chuẩn thể hiện main body từ Y=-2.0 đến +4.8 mm, latch protrusion tới Y=-3.7 mm; pad row ở Y=0 nên rõ ràng gần phía khóa hơn phía lưng.
- Giữ nguyên pitch X = 3.96 mm và toàn bộ vị trí X theo số chân.
- Áp dụng 2P..10P, 10 màu; canonical mới: V4_LOCKSIDE_FIXED.
- Generator xóa generated/VH3.96 cũ trước khi regenerate để tránh lẫn version stale.

## 2026-10-03 — VH3.96 housing rebuilt to XH-style architecture

- User reference image confirms the real VH3.96 header should visually match the XH2.54 molded housing family, scaled up for 3.96 mm pitch.
- Previous V4 housing geometry had an exaggerated latch/roof and is deprecated.
- Canonical housing now uses the same architecture as XH: floor, rear wall, side walls, lower front wall, guide shoulders, compact latch/key.
- Kept PCB-critical values: pitch 3.96 mm, body depth 9.40 mm, body height 8.50 mm, pin square 1.14 mm, pin row Y=-1.40 mm toward latch/front.
- Canonical new version: V5_XHSTYLE for 2P..10P, 10 colors.

## 2026-10-03 — VH3.96 rebuilt from JST page 3

- Các bản VH V3/V4/V5 trước sai kiến trúc housing: đã dựng giống XH/shrouded body.
- User cung cấp ảnh thực tế và catalog JST eVH.pdf trang 3; canonical family là standard top-entry B2P-VH ... B10P-VH.
- Rebuild V6_STANDARD_TOP với wafer thấp và post vuông xuyên qua wafer, đúng kiểu linh kiện thật.
- Kích thước PCB-critical: pitch 3.96 mm, post 1.14 mm, B = A + 3.90 mm, A=(N-1)*3.96.
- Theo drawing: mating post 7.70 mm, wafer/body theo trục pin 3.20 mm, solder tail 3.70 mm, tổng từ PCB tới đỉnh post 10.90 mm.
- Main depth 8.50 mm, overall lock-side depth xấp xỉ 9.40 mm, pin-row 2.00 mm từ lock/front side.
- Áp dụng 2P..10P, 10 màu. Canonical mới: V6_STANDARD_TOP.

## 2026-10-04 — VH3.96 full-width top ear added

- User pointed out the missing upper locking ear/shelf visible in JST VH catalog page 3 side view.
- V7 adds a full-width top ear across dimension B, projecting toward latch/front side, plus a small hooked leading lip.
- Pin pitch, pin-row position and all X pin centers are unchanged from V6.
- Ear dimensions are visual approximations because page 3 does not separately dimension this molded feature.
- Canonical visual model: V7_TOP_EAR_FIXED.

## 2026-10-04 — VH3.96 V8 proportion tuning

- User compared V6/V7 against a real BxP-VH photo and asked to prioritize visual proportion of the plastic lock rather than exact lock dimensions.
- V7 full-width thin ear looked too large/flat.
- Rebuilt the lock as a compact vertical support + shorter/thicker upper tongue + small front nose, while preserving all PCB-critical pin geometry.
- Preserved: pitch 3.96 mm, pin square 1.14 mm, pin row toward latch side, B=(N-1)*3.96+3.90 mm.
- Canonical visual baseline is now V8_PROPORTION_TUNED.

## 2026-10-04 — VH3.96 V9 exact-reference rebuild

- Dừng sử dụng các shape V6/V7/V8 đoán tay cho VH3.96.
- User cung cấp GrabCAD references và exact LCSC part C5379868; repo đã fetch nguyên bản EasyEDA STEP cho SHOU HAN VH3.96 2P..10P (C5379868..C5379876).
- Dùng C5379870 (4P) làm reference sạch để trích center YZ plastic profile và pin-center section.
- Exact observed family bboxes: 4P 15.84 × 8.20 × 13.60 mm; 5P 19.80 × 8.20 × 13.60 mm; 9P 35.64 × 8.20 × 13.60 mm; 10P 39.60 × 8.20 × 13.60 mm.
- Pin exact section: row center Y=+1.35 mm; full square ≈1.13 mm; tapered tip ≈0.53 mm; Z=-3.50..10.10 mm.
- Plastic center profile is copied directly from C5379870 section; generator canonical is now V9_EXACT_PROFILE.
- V6/V7/V8 are historical only and must not be used as baseline.

## 2026-10-04 — NENGWI QDX05GXXXX-B / QDX12GXXXX-B

- Added generator for the two user-supplied dual isolated gate-driver module families.
- Both supplied V1.3 mechanical drawings use the same package geometry: 30 x 15 x 12 mm.
- Physical pins are 1,2,3,4,6,7,8,9; pin 5 is intentionally absent.
- Pin 1 center is 2.63 mm from the left case edge; pin 1 to pin 9 span is 24.74 mm.
- Adjacent pitch inside each 4-pin group is 2.54 mm; center gap between pins 4 and 6 is 9.50 mm.
- Pin row is 0.64 mm from the front package edge; pin section modeled as 0.70 x 0.70 mm; tail length 4.10 mm.
- CLEAN and REALISTIC variants generated for both 5 V-input and 12 V-input families.

## 2026-10-04 — NENGWI QDX pin-span override

- User corrected the physical pin layout for QDX05/QDX12: Pin1-to-Pin9 center span = 27.74 mm across a 30.00 mm body.
- This intentionally differs from the supplied datasheet drawing, which visually shows 24.74 mm and 2.63 mm edge offset.
- Canonical user-target geometry now uses edge-to-Pin1 = 1.13 mm, within-group pitch = 2.54 mm, and Pin4-to-Pin6 center gap = 12.50 mm.
- Applies to both QDX05GXXXX-B and QDX12GXXXX-B.
\n## 2026-10-04 — HI-LINK HLK-10M 10W series\n\n- Added HLK-10M03 / 05 / 09 / 12 / 15 / 24 STEP generator.\n- Mechanical envelope: 46.9 x 27.8 x 21.8 mm.\n- Exact pin centers and 0.8 mm square pin section were extracted from the EasyEDA STEP for LCSC C403746 (HLK-10M12): P1/P2 at X=-21.25,Y=±3.90; P3/P4 at X=+21.25,Y=±11.40 mm.\n- PCB plane is body bottom Z=0; tail length 5.02 mm.\n- Same package geometry is reused across the six voltage variants; marking changes by model.\n