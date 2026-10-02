# MODEL INDEX

## Canonical / committed STEP

### IC
- `models/IC/AMC1200/AMC1200_DUB_SOP8_V4_PROPORTIONAL.step`
- `models/IC/AMC1200/AMC1200_DUB_SOP8_V4_CLEAN.step`

### Relay
- `models/Relay/HFD4/HFD4_THT_DIP.step`
- `models/Relay/HFD4/HFD4_SMT_STANDARD.step`

### Connectors / SFP
- `models/Connectors/SFP/U77-A1112-X0LX.step`
- `models/Connectors/SFP/U77-A1114-30L1.step`
- `models/Connectors/SFP/U77-A1113-X0LX.step`

### XH2.54 visual/color samples
- 2P WHITE / BROWN / GRAY / PURPLE V3 FIXED are committed under `models/Connectors/XH2.54/samples/`.
- Full 2P..10P × 10 colors is generated deterministically by `generators/generate_xh254.py`.
- Full variant table: `models/Connectors/XH2.54/MANIFEST_V3.csv`.

### VH3.96 visual/color samples
- 2P WHITE / BROWN / GRAY / PURPLE V3 FIXED are committed under `models/Connectors/VH3.96/samples/`.
- Full 2P..10P × 10 colors is generated deterministically by `generators/generate_vh396.py`.
- Full variant table: `models/Connectors/VH3.96/MANIFEST_V3.csv`.

## Generator-backed families

### RTL8367S
- Source: `generators/generate_rtl8367s.py`.
- Package: LQFP-128, body 14×14 mm, overall 16×16 mm, pitch 0.40 mm.
- Generator is source-of-truth because the assembly STEP is large.

### CBB red film capacitor
- Source: `generators/generate_cbb.py`.
- Case table: `models/Capacitors/CBB/CBB22_COMMON_CASES_100V-1200V.csv`.
- Voltage alone is not sufficient to choose case size.

## Why not commit every generated color/size STEP?

For large matrix families (XH/VH/CBB), the generator + manifest are the canonical source. This prevents 100+ near-duplicate STEP files from drifting apart and makes future corrections apply consistently to every variant.

If a generated variant becomes a production-critical model, copy that exact STEP into `models/` and note it in `docs/CHANGELOG.md`.
