# SOURCE NOTES

Các model trong repo được dựng từ mechanical drawing / datasheet / ảnh thực tế do user cung cấp trong quá trình làm việc.

## RTL8367S
- Mechanical package section: LQFP-128.
- Critical: body 14×14 mm, overall lead span 16×16 mm, pitch 0.40 mm.

## Hongfa HFD4
- User supplied `HFD4.pdf`.
- Critical: 10×6.5 mm body; THT and SMT variants; 5.08 mm THT row; ~7.5 mm SMT terminal span.

## XH2.54
- Generic clone-style 2.54 mm system used by the user.
- Do not replace with official JST XH 2.50 mm dimensions unless explicitly requested.

## VH3.96
- JST VH-style top-entry geometry, pitch 3.96 mm.
- User requires 2P..10P and 10 body colors.

## CBB
- Generic red CBB21/CBB22-style radial film capacitor.
- Use physical W/H/T/P/d, not voltage alone, to select model.

## Amphenol U77 SFP cage
- Drawing provided by user:
  https://cdn.amphenol-cs.com/media/wysiwyg/files/drawing/u77a111xx0lx.pdf
- Current cage is reconstructed for EDA; not claimed to be the official vendor STEP.

## AMC1200 / AMC1200B
- TI DUB SOP-8 mechanical drawing and user screenshots used.
- User explicitly prefers correct lead pitch/position and visually proportional body.
- Current canonical: V4 proportional; do not revert to earlier tall-body versions.
