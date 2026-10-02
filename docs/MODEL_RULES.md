# MODEL RULES / ACCEPTANCE CHECKLIST

Model chỉ được coi là hoàn thành khi:

- [ ] Pitch đúng drawing / yêu cầu user.
- [ ] Số pin đúng.
- [ ] Pin-1 orientation đúng.
- [ ] Body X/Y đúng hoặc có note rõ nếu là generic.
- [ ] SMD foot nằm tại Z=0.
- [ ] THT tail xuống dưới Z=0.
- [ ] STEP re-import thành công.
- [ ] Bounding box được ghi lại.
- [ ] Không có detached solids ngoài ý muốn.
- [ ] Không có housing dạng skeletal nếu linh kiện thực là molded body.
- [ ] Side-view trong Altium nhìn cân đối.
- [ ] Nếu có chỉnh tỷ lệ thẩm mỹ, tuyệt đối không thay pitch/tâm chân.
- [ ] Model canonical và model cũ được phân biệt rõ.

## Naming

Ưu tiên:
`<FAMILY>_<PART>_<VARIANT>[_Vn][_CLEAN|FIXED|PROPORTIONAL].step`

Với tụ:
`CBB22_<voltage>_W<...>_H<...>_T<...>_P<...>_D<...>.step`
