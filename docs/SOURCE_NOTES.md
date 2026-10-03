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
- Pin row is intentionally offset in housing depth: for the 5.80 mm clone body, use Y=+0.55 mm from body center, corresponding to 2.35 mm from the rear/plain edge. This follows the XH top-entry mechanical relationship rather than centering the pins.

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

## MORNSUN B1212S WR3
- Product pages: B1212S-1WR3 and B1212S-2WR3 from MORNSUN.
- Datasheet dimensions used: B_S-1WR3 = 11.60 x 6.00 x 10.16 mm; B_S-2WR3 = 19.65 x 7.05 x 10.16 mm.
- Recommended layout is on a 2.54 mm grid. B_S-2WR3 single-output pin set is 1,2,4,6.

## JST VH3.96 standard top-entry header
- Official source: JST VH catalog eVH.pdf, page 3: https://www.jst-mfg.com/product/pdf/eng/eVH.pdf
- Standard top-entry family: B2P-VH ... B10P-VH.
- Critical: pitch 3.96 mm; A=(N-1)*3.96; B=A+3.90; square post 1.14 mm.
- Current active geometry uses mating contact 7.70 mm, solder post 3.70 mm, overall contact 14.60 mm; embedded/wafer pin-axis thickness = 3.20 mm.
- Do not model this family as XH-style shrouded housing. It is a standard locking header with exposed posts.
