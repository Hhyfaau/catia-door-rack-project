# Dimensions & coordinates (mm)

All coordinates use X = length (0..2400), Y = width (0-centered, ±500), Z = height (0 = frame bottom; gates hang to Z=-153). Tube cross-section 40×40×2.5 (hollow).

| Member | Type | Count | Size | Position (orient, start / center) |
|---|---|---|---|---|
| 顶部纵向梁 | 空心方管 | 11 | 40×40×920 | 'Y', X=i*240, start Y=-460, Z=780 |
| 顶部横梁(无立柱侧) | 空心方管 | 1 | 40×40×2360 | 'X', start X=20, Y=-480, Z=780 |
| 底部纵梁 | 空心方管 | 2 | 40×40×2360 | 'X', X=20..2380, Y=±480, Z=20 |
| 底部内梁 | 空心方管 | 2 | 40×40×2360 | 'X', X=40..2360, Y=±120, Z=20 |
| 底部端梁 | 空心方管 | 2 | 40×40×920 | 'Y', X=0/2400, Y=-460..460, Z=20 |
| 立柱 | 空心方管 | 9 | 40×40×720 | 'Z', X=240..2160, Y=+480, Z=40..760 |
| 角柱(把手) | 空心方管 | 4 | 40×40×840 | 'Z', X={0,2400}, Y=±480, Z=40..880 |
| V 型定位小梁 | V 型 | 10 | 600 长 | 'Y', X=(i+0.5)*240, start Y=-480, vertex Z=40, opening Z=70 |
| 连接短梁 | 空心方管 | 4+2+4 | 40×40×{320,200,260} | 'Y', A:700/1200/1700/2200 (start Y=-460); B:1500/2100 (start Y=-100); C:700/1200/1700/2200 (start Y=+140), Z=20 |
| 门架U型梁 | U 型 | 8 | 56 宽×25 高×3 厚, 长580 | 'Y', X=660/1660, Z=-153..-113 |
| 门架立柱 | 空心方管 | 16 | 40×40×150 | 'Z', X={700,1200} (gate 680) & {1700,2200} (gate 1680), Y=±480, Z=-150..0 |
| 端部水平方管 | 矩形空心 | 2 | 40×153×250 | 'X', X=120..370, Y=±120, Z=-153..0 |

## Key relationships

- 顶部 11 根纵梁沿宽度分 10 个槽，每个槽一根 V 型小梁定位车门底边。
- 底部 4 根纵梁 Y=-480/-120/+120/+420（+480 为边梁），门架立柱落在其下方。
- 门架立柱 X 与 AC 间隔连接短梁对齐（700/1200/1700/2200）；U 型梁以两立柱中心对称（580 长，左右各外探 40）。
- 门架 U 型梁底面贴地 (Z=-153)，立柱插于内底面(Z=-150)，立柱顶面 Z=0 贴框架底梁下表面。
- 总装配高度 = 门架 153 + 框架 960。

## Rotation conventions

- `R_X = (0,0,-1, 0,1,0, 1,0,0)` — local Z → world X (beam along length).
- `R_Y = (-1,0,0, 0,0,1, 0,1,0)` — local Z → world Y, local Y → world +Z (U-beam opens up, beams along width).
- `R_Z = (1,0,0, 0,1,0, 0,0,1)` — vertical post.
- `position.set_components((*R, tx, ty, tz))`; for `X`/`Y`/`Z` beams t = start of the long axis, other two = cross-section center.
