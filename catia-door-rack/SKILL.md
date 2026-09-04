---
name: catia-door-rack
description: Build, modify, regenerate, and export the CATIA V5 汽车车门转运车架 (car-door transport rack) welded-steel-frame project. Use when Codex needs to (1) rebuild the rack assembly from its scripts (11 top beams, 13 posts with corner handles, 10 V-beam door locators, 8 U-beam+post gate supports, 2 end tubes), (2) change any dimension/position or add a member, (3) regenerate the CAD part templates or assembly, (4) export a STEP, (5) generate the Word report, or (6) produce the A3 engineering drawing. Triggered by requests about this project's CATPart/CATProduct files, its build scripts under scripts/, its report (.docx), or its drawing. Also use when working in the CATIA V5 automation stack (pycatia + win32com) for hollow square-tube frames.
---

# CATIA Car-Door Transport Rack

## Overview

This skill lets an agent regenerate, modify, and export a CATIA V5 **car-door transport rack** (汽车车门转运车架) — a welded frame of hollow 40×40 square tube that stores car doors upright (each door's bottom edge drops into a V-groove). Everything is exposed as a single assembly `DoorRack3.CATProduct` composed of 11 part types, plus a Word report and an A3 engineering drawing.

It is **data-driven**: all geometry is described by scripts + a coordinates reference, so changes are parameter edits, not manual CATIA re-modeling.

## When to use

- Rebuild the whole model from scratch.
- Change a beam/post/V-beam/gate dimension or position.
- Add a new member (post, beam, connector, support).
- Regenerate the engineering drawing or the Word report.
- Export a STEP for downstream use.

## Prerequisites

- CATIA V5 running with `CATIA.Application` reachable via COM.
- Python interpreter with `pycatia`, `pywin32` (this project uses `C:\Users\Administrator\Documents\Codex\CATIClaude\.venv\Scripts\python.exe`).

## Model anatomy

| 部件 | 数量 | 说明 |
|---|---|---|
| 顶部纵向梁 | 11 | 40×40×920 空心方管，沿宽度方向 20cm 间距，形成 10 个车门存放槽 |
| 纵/横梁(顶/底) | 6 | 40×40×2360/920 空心方管，组成框架周界与内部梁 |
| 立柱 | 9 | 40×40×720 空心方管，支撑顶架 |
| 角柱(带把手) | 4 | 40×40×840，顶部伸出当作把手 |
| V 型定位小梁 | 10 | V 型截面，每槽一根，托住车门底边定位 |
| 连接短梁 | 4+2+4 | 40×40×{320,200,260}，底部 A/B/C 间隔连接梁 |
| 门架U型梁 | 8 | U 型截面 56宽×25高×3厚、长580 |
| 门架立柱 | 16 | 40×40×150，插在 U 梁内底面，顶面贴底部横梁下表面 |
| 端部水平方管 | 2 | 40×153×250 矩形空心管 |

关键装配关系：门架立柱 X 与 AC 间隔连接短梁对齐（700/1200/1700/2200）；U 型梁以两立柱中心对称；门架 U 梁底面贴地(Z=-153)、立柱顶面 Z=0 贴框架底梁下表面；总高 = 门架 153 + 框架 960。

## Workflow

1. **Rebuild** — run the builder scripts in order. They close all documents, rebuild part templates, build the assembly, place gates/end tubes.
2. **Modify** — edit the desired parameter in the corresponding script, re-run that step, then re-run dependent steps.
3. **Export** — run `scripts/export_step.py` for STEP; run `scripts/build_report.py` for the Word report; generate the A3 `.CATDrawing` in CATIA (details below).

```powershell
$py = "C:\Users\Administrator\Documents\Codex\CATIClaude\.venv\Scripts\python.exe"
& $py scripts/build_tubes.py
& $py scripts/build_assembly.py
& $py scripts/add_gate_parts.py
& $py scripts/add_endtubes.py
& $py scripts/export_step.py
& $py scripts/build_report.py
```

## Scripts

| 脚本 | 作用 |
|---|---|
| `build_tubes.py` | 建空心方管模板（外 Pad 40×40 + 内贯通 Pocket，`limit_mode=2`）与 U 梁/V 梁 |
| `build_assembly.py` | 建 `DoorRack3.CATProduct`，用"起点定位 + 旋转矩阵"放所有框架杆件 |
| `place_gates_final.py` / `add_gate_parts.py` | 加 8 个门架（U 梁+双立柱），立柱对齐 AC 短梁 X |
| `add_endtubes.py` / `build_endtubes.py` | 加 2 根端部水平方管（40×153×250） |
| `export_step.py` | 导出总装配 STEP |
| `build_report.py` | 用 python-docx 生成 Word 报告 |
| `gen_drawing2.py` / `render_iso.py` / `gen_2d_dims.py` | 生成 A3 工程图图样 / 整体轴测图 / 二维尺寸图 |

## Parameters & coordinates

All coordinates use X=length(0..2400), Y=width(±500), Z=height(0=frame bottom; gates hang to -153). The authoritative table lives in `references/dimensions.md` — treat it as the source of truth when editing, and update both the script and the reference together.

Defining rotation matrices (`position.set_components((*R, tx,ty,tz))`):

- `R_X = (0,0,-1, 0,1,0, 1,0,0)` — beam along length (X). `tx = start_x`, `ty/tz = cross center`.
- `R_Y = (-1,0,0, 0,0,1, 0,1,0)` — beam along width (Y), and makes a U-beam open upward. `ty = start_y`.
- `R_Z = (1,0,0, 0,1,0, 0,0,1)` — vertical post. `tz = start_z`.

## Engineering drawing (+BOM & balloons)

The native `.CATDrawing` must be generated in CATIA's Drafting workbench (not automatable here):

1. Open `DoorRack3.CATProduct`.
2. 文件→新建→Drawing → **A3** 纵向，比例 1:10 → 有 A3 图框/标题栏。
3. 插入 → 视图：主视图（正面长×高方向）→ 拖出俯视图/侧视图 → 再插等轴测视图，按图框调比例。
4. 插入 → 标注 → 零件序号(气球) → 在轴测图上点选零件。
5. 插入 → 表格 → BOM（材料清单）。
6. 另存为 `总装配图.CATDrawing`。

## Gotchas

- **Hollow parts** are Pad(outer) + through Pocket(inner). Must set `pkt.first_limit.limit_mode = 2`, else R20 offset pockets cut nothing.
- **Start-point positioning**, not center: for `X`/`Y` beams the translation component is the *start* of the long axis; the other two are the cross-section center.
- **File locks**: rebuilding a part file requires closing the assembly that references it, else `SaveAs` fails. Close all docs before template builds.
- **Sub-assembly links break** after many close/reopen cycles ("Check Product for broken links"). Prefer placing parts directly instead of via sub-assemblies.
- **Chinese in SKILL.md**: validate tools may read files as GBK on a zh-CN system; that's a tool limitation, not a skill defect.

## Example requests

- "Rebuild the CATIA door rack using this skill."
- "把门架 U 型梁长度改成 620，并让 8 个门架保持对称。"
- "Add 2 more support posts at X=900, Y=+480."
- "Export the assembly to STEP and regenerate the report."
