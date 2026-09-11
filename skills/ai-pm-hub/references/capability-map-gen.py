#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai-pm-hub 能力地图 SVG 生成器（v3 · 自动换行 + 动态行高）
==============================================================

读 capability-map-data.json → 生成 capability-map.svg

v3 关键改动：
  - 文本按像素宽度自动换行（中文 1em / 拉丁 0.55em 估算），不再硬截断
  - 行高按该段实际内容动态计算（内容多的段自动变高）
  - 段名、覆盖文档、段内顺序、产出物、ref 文件列表全部可多行

同步更新：编辑 capability-map-data.json → python3 capability-map-gen.py
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
DATA_FILE = HERE / "capability-map-data.json"
OUT_FILE  = HERE / "capability-map.svg"

# ----- 配色 -----
SKILL_COLOR = {
    "mi":  "#7c3aed",
    "uv":  "#2563eb",
    "vb":  "#0891b2",
    "pd":  "#059669",
    "prd": "#dc2626",
}
TEACH_COLOR = "#ea580c"
DEEP_BG  = "#f8fafc"
CARD_BG  = "#ffffff"
BORDER   = "#e5e7eb"
TEXT     = "#1f2937"
TEXT_2   = "#4b5563"
MUTED    = "#6b7280"
TAG_TEXT = "#ffffff"

# ----- 布局常量 -----
W = 1280
PADDING       = 32
LEFT_NUMBER_W = 88
GAP           = 20
COL_SKILL = 168
COL_COVER = 344
COL_FLOW  = 268
COL_DEL   = 284
CARD_X = PADDING + LEFT_NUMBER_W
CARD_W = W - 2*PADDING - LEFT_NUMBER_W
_inner = COL_SKILL + GAP*3 + COL_COVER + COL_FLOW + COL_DEL
assert _inner <= CARD_W, f"列宽超出: {_inner} > {CARD_W}"

HEADER_H  = 104
ROW_GAP   = 12
TEACH_H   = 132
FOOTER_H  = 88

# 字号与行高
FS_LABEL = 10
FS_COVER = 12.5
FS_FLOW  = 12
FS_DEL   = 12.5
FS_REF   = 10
FS_SEG   = 19
LINE_COVER = 17
LINE_FLOW  = 17
LINE_DEL   = 17
LINE_SEG   = 25
LINE_REF   = 15

# ----- 数据 -----
data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
title, subtitle = data["title"], data["subtitle"]
skills, segments, teaching, deps = data["skills"], data["segments"], data["teaching_assets"], data["dependencies"]
n_seg = len(segments)

def esc(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def ch_w(ch, fs):
    """单字符估算宽度：CJK 全角 1em，拉丁/数字 0.55em，空格 0.3em。"""
    o = ord(ch)
    if ch == " ":
        return fs * 0.30
    if o > 0x2E80 or o in (0x3000,):      # CJK、全角标点
        return fs * 1.00
    if ch in "→←⟶·—":
        return fs * 1.00
    return fs * 0.55

# 行首禁则：这些字符不能出现在行首，需回挂到上一行
NO_LINE_START = set("，。、；：？！）】》」』…%·")

def wrap(text, max_px, fs, max_lines=None):
    """按像素宽度换行，返回行列表。"""
    text = str(text).strip()
    if not text:
        return [""]
    lines, cur, curw = [], "", 0.0
    for ch in text:
        w = ch_w(ch, fs)
        if curw + w > max_px and cur:
            # 禁则处理：若当前字符不该作行首，挤进上一行
            if ch in NO_LINE_START:
                cur += ch
                lines.append(cur)
                cur, curw = "", 0.0
                continue
            lines.append(cur)
            cur, curw = ch, w
        else:
            cur += ch
            curw += w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        head = lines[:max_lines]
        tail = "".join(lines[max_lines:])
        head[-1] = head[-1] + tail
        lines = head
    return lines

# ============================================================
# 内容预计算（用于动态行高）
# ============================================================
def build_content(seg):
    """返回该段 4 列各自的渲染行（含类型标记），供布局与高度计算共用。"""
    skill = next(s for s in skills if s["id"] == seg["skill"])
    c = {}
    # 列 1：段名多行 + ref 计数
    c["seg_lines"]   = wrap(seg["name"], COL_SKILL - 12, FS_SEG)
    c["ref_count"]   = f'含 {len(seg["ref_files"])} 份框架'
    c["skill_short"] = skill.get("short", skill["name"])
    c["skill_refs"]  = f'{skill["refs"]} 份 reference'
    # 列 2：覆盖文档（· 分隔的段落流，比 bullet 省一半高度；6 行内装完）
    c["cover_lines"] = wrap(" · ".join(seg["covers"]), COL_COVER - 6, FS_COVER, max_lines=6)
    # 列 3：段内顺序
    flow_raw = seg["internal_flow"]
    c["flow_lines"] = []
    for part in flow_raw.split("\n"):
        c["flow_lines"].extend(wrap(part, COL_FLOW - 6, FS_FLOW))
    # 列 4：产出物 + ref 文件（最多列 5 个，其余折叠为 +N 个文件）
    c["del_lines"] = wrap(seg["deliverable"], COL_DEL - 6, FS_DEL)
    files = [rf.replace(".md","").replace(".html","").replace(".py","") for rf in seg["ref_files"]]
    c["ref_files"] = files[:5]
    c["ref_more"]  = len(files) - len(c["ref_files"])
    return c

CONTENT = [build_content(s) for s in segments]

def row_height(c):
    h1 = 34 + 46 + 10 + len(c["seg_lines"])*LINE_SEG + 6 + 14
    h2 = 34 + len(c["cover_lines"])*LINE_COVER
    h3 = 34 + len(c["flow_lines"])*LINE_FLOW
    h4 = 34 + len(c["del_lines"])*LINE_DEL + 12 + (len(c["ref_files"]) + (1 if c["ref_more"] else 0))*LINE_REF
    return max(h1, h2, h3, h4) + 28   # 上下内边距

ROW_H = [row_height(c) for c in CONTENT]
ROW_Y = []
_acc = HEADER_H
for h in ROW_H:
    ROW_Y.append(_acc)
    _acc += h + ROW_GAP

BODY_END = _acc
H = BODY_END + TEACH_H + FOOTER_H

# ============================================================
# 渲染
# ============================================================
def segment_row(i, seg, c):
    color = SKILL_COLOR[seg["skill"]]
    y = ROW_Y[i]
    rh = ROW_H[i]
    cy = y + rh//2
    parts = []

    # 段位编号 + 竖向连接线
    num_cx = PADDING + 32
    parts.append(
      f'<line x1="{num_cx}" y1="{y-8}" x2="{num_cx}" y2="{y+rh+8}" '
      f'stroke="{BORDER}" stroke-width="2" stroke-dasharray="3,3"/>'
    )
    parts.append(
      f'<circle cx="{num_cx}" cy="{cy}" r="26" fill="{color}"/>'
      f'<text x="{num_cx}" y="{cy+1}" font-size="20" font-weight="700" '
      f'fill="{TAG_TEXT}" text-anchor="middle" dominant-baseline="middle">{seg["no"]}</text>'
    )

    # 卡片
    card_y = y + 4
    card_h = rh - 8
    parts.append(
      f'<rect x="{CARD_X}" y="{card_y}" width="{CARD_W}" height="{card_h}" '
      f'rx="10" fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>'
    )
    parts.append(
      f'<rect x="{CARD_X}" y="{card_y}" width="5" height="{card_h}" rx="2.5" fill="{color}"/>'
    )

    inner_x = CARD_X + 20
    label_y = card_y + 22

    # ---------- 列 1：归属 ----------
    c1 = inner_x
    parts.append(
      f'<text x="{c1}" y="{label_y}" font-size="{FS_LABEL}" font-weight="700" '
      f'letter-spacing="1.1" fill="{MUTED}">归属</text>'
    )
    chip_y = card_y + 30
    chip_h = 46
    chip_w = COL_SKILL - 10
    parts.append(
      f'<rect x="{c1}" y="{chip_y}" width="{chip_w}" height="{chip_h}" rx="7" '
      f'fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-width="1.2"/>'
    )
    parts.append(f'<circle cx="{c1+14}" cy="{chip_y+16}" r="4.5" fill="{color}"/>')
    parts.append(
      f'<text x="{c1+25}" y="{chip_y+16}" font-size="13" font-weight="600" '
      f'fill="{color}" dominant-baseline="middle">{esc(c["skill_short"])}</text>'
    )
    parts.append(
      f'<text x="{c1+14}" y="{chip_y+34}" font-size="10" fill="{MUTED}" '
      f'dominant-baseline="middle">{esc(c["skill_refs"])}</text>'
    )
    # 段名（多行）
    ny = chip_y + chip_h + 24
    for ln in c["seg_lines"]:
        parts.append(
          f'<text x="{c1}" y="{ny}" font-size="{FS_SEG}" font-weight="700" '
          f'fill="{TEXT}">{esc(ln)}</text>'
        )
        ny += LINE_SEG
    parts.append(
      f'<text x="{c1}" y="{ny+2}" font-size="10.5" fill="{MUTED}">{esc(c["ref_count"])}</text>'
    )

    # ---------- 列 2：覆盖文档（段落流，自动换行） ----------
    c2 = c1 + COL_SKILL + GAP
    parts.append(
      f'<text x="{c2}" y="{label_y}" font-size="{FS_LABEL}" font-weight="700" '
      f'letter-spacing="1.1" fill="{MUTED}">覆盖文档</text>'
    )
    by = card_y + 40
    for ln in c["cover_lines"]:
        parts.append(
          f'<text x="{c2}" y="{by}" font-size="{FS_COVER}" fill="{TEXT_2}">{esc(ln)}</text>'
        )
        by += LINE_COVER

    # ---------- 列 3：段内顺序（可换行） ----------
    c3 = c2 + COL_COVER + GAP
    parts.append(
      f'<text x="{c3}" y="{label_y}" font-size="{FS_LABEL}" font-weight="700" '
      f'letter-spacing="1.1" fill="{MUTED}">段内顺序</text>'
    )
    fy = card_y + 40
    for ln in c["flow_lines"]:
        parts.append(
          f'<text x="{c3}" y="{fy}" font-size="{FS_FLOW}" fill="{TEXT_2}">{esc(ln)}</text>'
        )
        fy += LINE_FLOW

    # ---------- 列 4：产出物（可换行） ----------
    c4 = c3 + COL_FLOW + GAP
    parts.append(
      f'<text x="{c4}" y="{label_y}" font-size="{FS_LABEL}" font-weight="700" '
      f'letter-spacing="1.1" fill="{MUTED}">产出物</text>'
    )
    dy = card_y + 40
    for ln in c["del_lines"]:
        parts.append(
          f'<text x="{c4}" y="{dy}" font-size="{FS_DEL}" font-weight="600" '
          f'fill="{TEXT}">{esc(ln)}</text>'
        )
        dy += LINE_DEL
    dy += 12
    for rf in c["ref_files"]:
        parts.append(
          f'<text x="{c4}" y="{dy}" font-size="{FS_REF}" '
          f'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" '
          f'fill="{MUTED}">{esc(rf)}</text>'
        )
        dy += LINE_REF
    if c["ref_more"]:
        parts.append(
          f'<text x="{c4}" y="{dy}" font-size="{FS_REF}" fill="{MUTED}">'
          f'+{c["ref_more"]} 个文件（详见技能目录）</text>'
        )

    return "\n".join(parts)

# ============================================================
# 段间依赖箭头（沿编号圆左侧的竖向虚线 + 箭头）
# ============================================================
def dep_arrows():
    parts = []
    cy = {seg["no"]: ROW_Y[i] + ROW_H[i]//2 for i, seg in enumerate(segments)}
    x1 = PADDING + 32 - 30
    for d in deps:
        y1, y2 = cy[d["from"]] + 28, cy[d["to"]] - 28
        if y2 - y1 < 10:
            continue
        parts.append(
          f'<line x1="{x1}" y1="{y1}" x2="{x1}" y2="{y2-7}" '
          f'stroke="{TEACH_COLOR}" stroke-width="1.4" stroke-dasharray="2,2" opacity="0.5"/>'
        )
        parts.append(
          f'<polygon points="{x1-4},{y2-7} {x1+4},{y2-7} {x1},{y2}" '
          f'fill="{TEACH_COLOR}" opacity="0.65"/>'
        )
    return "\n".join(parts)

# ============================================================
# 头部
# ============================================================
def header():
    parts = [
      f'<text x="{PADDING}" y="42" font-size="22" font-weight="800" fill="{TEXT}">{esc(title)}</text>',
      f'<text x="{PADDING}" y="66" font-size="13" fill="{MUTED}">{esc(subtitle)} · 数据版本 {esc(data["version"])}</text>',
    ]
    stats = [
        ("子技能", len(skills), SKILL_COLOR["pd"]),
        ("段位",   n_seg,       SKILL_COLOR["uv"]),
        ("reference", sum(s["refs"] for s in skills), SKILL_COLOR["vb"]),
        ("教学",   len(teaching), TEACH_COLOR),
    ]
    cw, ch, sp = 82, 58, 8
    sx0 = W - PADDING - (4*cw + 3*sp)
    for i,(k,v,c) in enumerate(stats):
        sx = sx0 + i*(cw+sp)
        parts.append(f'<rect x="{sx}" y="24" width="{cw}" height="{ch}" rx="8" fill="{c}" fill-opacity="0.08"/>')
        parts.append(f'<text x="{sx+cw/2}" y="45" font-size="10" fill="{MUTED}" text-anchor="middle">{esc(k)}</text>')
        parts.append(f'<text x="{sx+cw/2}" y="69" font-size="22" font-weight="800" fill="{c}" text-anchor="middle">{v}</text>')
    return "\n".join(parts)

# ============================================================
# 教学素材带
# ============================================================
def teaching_band():
    y0 = BODY_END + 12
    parts = [
      f'<text x="{PADDING}" y="{y0+18}" font-size="13" font-weight="700" fill="{TEACH_COLOR}">教学素材</text>',
      f'<text x="{PADDING+76}" y="{y0+18}" font-size="11" fill="{MUTED}">PM 新人友好入口 — 说「直播课件」「产品设计七层」「SWOT 提示词」时调取</text>',
    ]
    n = len(teaching)
    cw = (W - 2*PADDING - 16*(n-1)) // n
    cy = y0 + 30
    ch = TEACH_H - 44
    for i, t in enumerate(teaching):
        cx = PADDING + i*(cw+16)
        parts.append(
          f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="8" '
          f'fill="{TEACH_COLOR}" fill-opacity="0.06" stroke="{TEACH_COLOR}" stroke-width="1.2"/>'
        )
        parts.append(
          f'<text x="{cx+14}" y="{cy+22}" font-size="12" font-weight="700" fill="{TEACH_COLOR}">{esc(t["name"])}</text>'
        )
        ty = cy + 42
        for ln in wrap(t["title"], cw-28, 11.5, max_lines=2):
            parts.append(f'<text x="{cx+14}" y="{ty}" font-size="11.5" fill="{TEXT_2}">{esc(ln)}</text>')
            ty += 16
        parts.append(
          f'<text x="{cx+14}" y="{cy+ch-12}" font-size="10.5" fill="{MUTED}">覆盖：{esc(t["covers"])}</text>'
        )
    return "\n".join(parts)

# ============================================================
# 页脚
# ============================================================
def footer():
    y0 = H - FOOTER_H
    parts = [
      f'<text x="{PADDING}" y="{y0+18}" font-size="11" font-weight="700" fill="{TEXT}">同步更新约定</text>',
      f'<text x="{PADDING}" y="{y0+36}" font-size="10.5" fill="{MUTED}">编辑 capability-map-data.json → python3 capability-map-gen.py → 检查 SVG 无溢出（本图文本自动换行、行高按内容自适应）</text>',
      f'<text x="{PADDING}" y="{y0+54}" font-size="10.5" fill="{MUTED}">段间依赖：1→2→3→4→5、4→6/7、6→7/8、7→8 — 完整清单见 data 文件 dependencies 字段</text>',
    ]
    lx = W - PADDING - 340
    ly = y0 + 22
    parts.append(f'<text x="{lx}" y="{ly}" font-size="11" font-weight="700" fill="{TEXT}">子技能配色</text>')
    for i, s in enumerate(skills):
        px = lx + 78 + i*56
        parts.append(f'<circle cx="{px}" cy="{ly-4}" r="5" fill="{SKILL_COLOR[s["id"]]}"/>')
        parts.append(f'<text x="{px+9}" y="{ly}" font-size="10" fill="{TEXT_2}">{esc(s["id"])}</text>')
    return "\n".join(parts)

# ============================================================
# 拼装
# ============================================================
out = [
  f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'font-family="-apple-system, BlinkMacSystemFont, PingFang SC, Microsoft YaHei, sans-serif">',
  f'<rect width="{W}" height="{H}" fill="{DEEP_BG}"/>',
  header(),
  dep_arrows(),
]
for i, seg in enumerate(segments):
    out.append(segment_row(i, seg, CONTENT[i]))
out.append(teaching_band())
out.append(footer())
out.append('</svg>')

OUT_FILE.write_text("\n".join(out), encoding="utf-8")
print(f"✅ {OUT_FILE.name} ({W}×{H}) · {n_seg} 段 · 行高 {min(ROW_H)}–{max(ROW_H)}px（动态自适应）")
print(f"   列宽 归属{COL_SKILL} 覆盖{COL_COVER} 顺序{COL_FLOW} 产出{COL_DEL} · 全部文本按像素宽度自动换行")
