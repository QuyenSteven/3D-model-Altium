# Generators

Các model nhiều biến thể không nên chỉnh thủ công từng STEP. Hãy sửa generator rồi regenerate để tránh lệch kích thước giữa các variant.

## Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy

```bash
cd generators
python generate_xh254.py
python generate_vh396.py
python generate_amc1200.py
python generate_rtl8367s.py
python generate_hfd4.py
python generate_cbb.py
python generate_sfp_u77.py
```

Output nằm trong `generated/`.

## Source of truth

- XH2.54: `generate_xh254.py` — V3 FIXED, 2P..10P, 10 colors.
- VH3.96: `generate_vh396.py` — V3 FIXED, 2P..10P, 10 colors.
- AMC1200: `generate_amc1200.py` — V4 proportional baseline.
- RTL8367S: `generate_rtl8367s.py` — LQFP-128 14x14 / 16x16 / 0.40 mm.
- HFD4: `generate_hfd4.py` — THT + standard SMT.
- CBB: `generate_cbb.py` + CSV case table.
- SFP U77: `generate_sfp_u77.py` — reconstructed EDA cage.

Trước khi chỉnh generator, đọc `docs/PROJECT_CONTEXT.md`.
