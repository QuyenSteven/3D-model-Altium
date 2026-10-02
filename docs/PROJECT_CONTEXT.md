# PROJECT CONTEXT — 3D Model Altium

File này là ngữ cảnh bắt buộc cho các lần làm việc sau. Mục tiêu là tránh lặp lại các lỗi đã sửa trong quá trình dựng model.

## 1. Nguyên tắc chung

### Ưu tiên kích thước
- Ưu tiên tuyệt đối: **pitch chân, tâm chân, khoảng cách hàng chân, overall lead span, body X/Y theo drawing**.
- Không thu/phóng toàn model để ép khớp footprint nếu pitch đang đúng.
- Nếu footprint sai, sửa footprint; nếu model sai, sửa hình học model từ nguồn.
- Có thể điều chỉnh chiều cao / bevel / fillet / tỷ lệ hình học không ảnh hưởng footprint nếu model nhìn mất cân đối trong Altium.

### Hệ tọa độ
- PCB top surface: **Z = 0**.
- SMD solder feet: chạm Z=0.
- THT solder tails: kéo xuống Z<0.
- Origin ưu tiên tại tâm package/connector để dễ align trong Altium.

### Validation
Sau khi export:
1. Re-import STEP.
2. Đọc bounding box X/Y/Z.
3. So với datasheet / drawing.
4. Kiểm tra số lượng pin.
5. Kiểm tra pin-1 orientation.
6. Kiểm tra bằng góc nhìn ngang trong Altium, vì nhiều lỗi tỷ lệ chỉ thấy rõ ở side view.

## 2. Những lỗi đã gặp và không được lặp lại

### XH2.54 / VH3.96
Bản đầu tiên dựng housing bằng outer shell - cavity quá lớn nên nhìn như wireframe / vách mỏng trong Altium.

**Yêu cầu cố định từ nay:**
- Housing phải là **molded solid construction**: floor + rear wall + side walls + lower front wall + guide/latch features.
- Không dùng shell mỏng làm hình chính.
- XH2.54 clone giữ pitch **2.54 mm** (không tự đổi sang JST XH 2.50 mm).
- VH giữ pitch **3.96 mm**.
- Bộ màu hiện tại: WHITE, BLACK, RED, BLUE, GREEN, YELLOW, ORANGE, BROWN, GRAY, PURPLE.
- Dải pin: 2P..10P.

### AMC1200 / AMC1200B DUB SOP-8
Bản đầu thân quá cao và chân gull-wing dài/dốc, nhìn không tương xứng.

**Baseline hiện tại: V4 proportional**
- Pin pitch: **2.54 mm** — giữ đúng.
- Overall lead span: **10.40 mm** — giữ đúng.
- Body length: **9.285 mm** — giữ đúng.
- Flat lead foot: khoảng **1.30 mm**.
- Body width dùng: **6.50 mm**.
- Body bottom: khoảng **0.34 mm** trên PCB.
- Body top: khoảng **3.45 mm**.
- Body height khoảng **3.11 mm**.
- Chân gull-wing: shoulder thấp, bend ngắn, foot phẳng trên PCB.
- Mục tiêu: đúng footprint và nhìn cân đối; không ép theo 4.85 mm max nếu làm hình quá cao.

### RTL8367S LQFP-128
- Datasheet package: LQFP-128, body **14 x 14 mm**, overall lead span **16 x 16 mm**, pitch **0.40 mm**.
- Nếu footprint đo pad-to-pad khoảng 14.4 mm thì không được scale STEP xuống 14.4; đó không phải overall lead span.
- Pin-1 dot phải đúng góc và nhìn nhất quán giữa 2D/3D.

### HFD4 relay
- Có cả THT/DIP và Standard SMT.
- Body nominal: **10 x 6.5 mm**.
- Standard SMT overall terminal span khoảng **7.5 mm**, body height khoảng **5.65 mm**.
- THT row spacing khoảng **5.08 mm**.
- Dáng chân có thể giản lược nếu drawing không cho bend radius, nhưng vị trí chân và envelope phải giữ.

### CBB đỏ
- Không suy ra kích thước chỉ từ điện áp.
- Cùng 400V/630V/... kích thước còn phụ thuộc capacitance và manufacturer.
- Naming phải chứa W/H/T/P/d để chọn model theo kích thước thực tế.
- Dải library hiện tại: 100V, 160V, 250V, 400V, 450V, 630V, 800V, 1000V, 1200V.

### SFP cage Amphenol U77
- Model hiện là reconstructed EDA model, không phải official vendor STEP.
- Có variants solder tail 1.2 / 1.8 / 3.2 mm.
- Fine formed-sheet features có thể giản lược, nhưng body envelope và mouth/cage placement phải giữ.

## 3. Quy ước phiên bản

- `V1`: initial draft.
- `V2/V3`: correction iterations.
- `FIXED`: đã sửa lỗi hình học nghiêm trọng.
- `CLEAN`: không lettering, ưu tiên tương thích Altium.
- `PROPORTIONAL`: giữ PCB-critical dimensions nhưng điều chỉnh tỷ lệ nhìn theo yêu cầu.
- Khi có bản mới tốt hơn, **không xóa context cũ**; ghi vào CHANGELOG và đánh dấu bản canonical.

## 4. Cách làm cho model mới

1. Lấy mechanical drawing/datasheet.
2. Trích bảng kích thước thành một block constants.
3. Dựng body.
4. Dựng pin/terminal riêng.
5. Dựng pin-1/orientation mark.
6. Export STEP.
7. Re-import và validate bbox.
8. Tạo note: nguồn, dimension assumptions, phần nào exact, phần nào visual approximation.
9. Nếu user gửi screenshot Altium, ưu tiên sửa từ nguyên nhân thay vì scale/vá.

### MORNSUN B1212S WR3
- Current family: B1212S-1WR3 (1 W) and B1212S-2WR3 (2 W), SIP.
- PCB-critical dimensions: 2.54 mm grid; 1 W pins 1-4 consecutive; 2 W single-output uses pins 1,2,4,6.
- Body dimensions from MORNSUN datasheets: 1 W = 11.60 x 6.00 x 10.16 mm; 2 W = 19.65 x 7.05 x 10.16 mm.
- Pin row is 0.90 mm from long case edge; pins approx. 0.50 x 0.30 mm; exposed length from case 4.10 mm.
- Use CLEAN in Altium when top text is unnecessary; REALISTIC adds MORNSUN/part marking and pin-1 dot.
