# USER / DESIGN REQUIREMENTS

## General
- Model dùng trong Altium phải nhìn hợp lý ở cả top view và side view.
- Không chỉ đúng con số; tỷ lệ hình học phải giống linh kiện thật khi quan sát 3D.
- Tuy nhiên **khoảng cách chân / pitch / tâm chân / overall lead span phục vụ footprint là bất biến ưu tiên cao nhất**.
- Khi phải lựa chọn giữa height theo max datasheet và tỷ lệ nhìn thực tế, có thể hạ height nếu user yêu cầu, miễn không ảnh hưởng footprint; phải ghi rõ là proportional model.
- Tránh patch/scale toàn model. Luôn tìm kích thước sai và sửa tại nguồn.
- STEP CLEAN được ưu tiên cho Altium nếu lettering làm nặng hoặc render xấu.

## Connectors
- XH2.54: dùng pitch 2.54 mm theo clone-style thực tế user đang dùng, không tự đổi sang 2.50 mm.
- VH3.96: pitch 3.96 mm.
- XH/VH phải có housing molded solid, không được chỉ có thin outer shell.
- Pin matrix: 2P..10P.
- Màu chuẩn hiện tại: white, black, red, blue, green, yellow, orange, brown, gray, purple.

## AMC1200
- Dùng DUB SOP-8.
- User ưu tiên chân/pitch đúng; body height có thể điều chỉnh cho tỷ lệ thực tế.
- Baseline hiện tại: V4 proportional.
- Nếu chỉnh tiếp, bắt đầu từ V4, không quay về V1/V2/V3.

## Workflow
- Mỗi thay đổi lớn phải cập nhật `docs/CHANGELOG.md`.
- Mỗi family phải có generator hoặc source dimensions.
- Re-import STEP và kiểm tra bounding box trước khi coi là xong.
- Nếu user gửi screenshot Altium, lấy screenshot đó làm validation visual và sửa nguyên nhân.
