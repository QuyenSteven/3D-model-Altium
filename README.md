# 3D Model Altium

Thư viện model 3D STEP dùng cho Altium, tập trung vào model cơ khí thực dụng: đúng pitch / vị trí chân / envelope quan trọng cho PCB, đồng thời giữ tỷ lệ hình học nhìn tự nhiên trong 3D.

## Baseline hiện tại

- RTL8367S — LQFP-128
- Hongfa HFD4 — THT/DIP và Standard SMT
- XH2.54 clone-style — 2P..10P, 10 màu
- VH3.96 JST-style — 2P..10P, 10 màu
- CBB21/CBB22 radial film capacitor đỏ — common case sizes 100V..1200V
- Amphenol U77 / SFP 1x1 cage — 1.2 / 1.8 / 3.2 mm solder-tail variants
- TI AMC1200 / AMC1200B — DUB SOP-8

## Quy tắc dự án

1. Kích thước PCB-critical phải ưu tiên tuyệt đối: pitch, vị trí tâm chân, overall lead span, body length/width nếu có drawing chính thức.
2. Không scale toàn model để ép khớp footprint; phải sửa đúng nguyên nhân ở footprint hoặc hình học model.
3. Khi datasheet không quy định một kích thước duy nhất, ghi rõ model là generic/common envelope.
4. Housing connector phải là khối đúc chắc, không làm kiểu vách mỏng/skeletal khiến Altium hiển thị sai cảm giác thực tế.
5. Mọi STEP sau export phải được re-import và kiểm tra bounding box.
6. PCB plane mặc định là Z=0; chân hàn THT đi xuống Z<0; chân SMD đặt foot trên Z=0.
7. Với model cần cân tỷ lệ nhìn (ví dụ AMC1200 DUB), giữ các kích thước PCB-critical đúng và chỉ tinh chỉnh phần hình học không ảnh hưởng footprint.

Đọc `docs/PROJECT_CONTEXT.md` trước khi tạo/chỉnh model mới.
