#!/usr/bin/env python3
"""Generates Adwaita-style 128px app icons for the Craft App Suite into icons/, as SVGs plus
PNGs at every fixed hicolor size (rendered with Inkscape)."""
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent / "icons"
OUT = ROOT / "scalable" / "apps"
SIZES = [16, 24, 32, 48, 64, 128, 256, 512]

# Adwaita palette (GNOME HIG), plus the suite colours Adwaita has no close match for.
LIGHT = ["#ffffff", "#f6f5f4", "#deddda", "#c0bfbc", "#9a9996"]
DARK = ["#77767b", "#5e5c64", "#3d3846", "#241f31", "#000000"]
BLUE = ["#99c1f1", "#62a0ea", "#3584e4", "#1c71d8", "#1a5fb4"]
GREEN = ["#8ff0a4", "#57e389", "#33d17a", "#2ec27e", "#26a269"]
YELLOW = ["#f9f06b", "#f8e45c", "#f6d32d", "#f5c211", "#e5a50a"]
ORANGE = ["#ffbe6f", "#ffa348", "#ff7800", "#e66100", "#c64600"]
RED = ["#f66151", "#ed333b", "#e01b24", "#c01c28", "#a51d2d"]
PURPLE = ["#dc8add", "#c061cb", "#9141ac", "#813d9c", "#613583"]
BROWN = ["#cdab8f", "#b5835a", "#986a44", "#865e3c", "#63452c"]
PINK = ["#f7a1cb", "#ef6aa9", "#e3338a", "#c62275", "#9e1a5d"]
LIME = ["#cbeb8a", "#a8d84d", "#86c22b", "#6ea41f", "#558218"]
TEAL = ["#8adbe6", "#3fbfd2", "#1a9fb9", "#15849b", "#10687a"]
INDIGO = ["#a6b4f5", "#7088ec", "#4b63d9", "#3a4fbd", "#2c3d96"]

# Dark objects need a faint rim to stay visible on dark panels and docks.
RIM = 'stroke="#ffffff" stroke-opacity=".14" stroke-width="1.5"'


def slab(x, y, w, h, r, face, side, depth=8, extra=""):
    """A front-facing Adwaita base: a darker copy dropped by `depth` shows the object's thickness."""
    return (f'<rect x="{x}" y="{y + depth}" width="{w}" height="{h}" rx="{r}" fill="{side}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{face}" {extra}/>')


def lines(x, y, widths, gap, colour, thick=4):
    return "".join(f'<rect x="{x}" y="{y + i * gap}" width="{w}" height="{thick}" rx="{thick / 2}" fill="{colour}"/>'
                   for i, w in enumerate(widths))


def page(x, y, w, h, fold=20):
    """A sheet of paper with a folded top-right corner."""
    p = f"M{x + 6} {y}h{w - 6 - fold}l{fold} {fold}v{h - fold - 6}a6 6 0 0 1-6 6h{-(w - 12)}a6 6 0 0 1-6-6v{-(h - 12)}a6 6 0 0 1 6-6z"
    return (f'<path d="{p}" transform="translate(0 6)" fill="{LIGHT[3]}"/>'
            f'<path d="{p}" fill="{LIGHT[1]}"/>'
            f'<path d="M{x + w - fold} {y}v{fold - 4}a4 4 0 0 0 4 4h{fold - 4}z" fill="{LIGHT[2]}"/>')


def launcher():
    tiles = [BLUE, ORANGE, GREEN, RED, PURPLE, YELLOW, TEAL, PINK, INDIGO]
    body = slab(12, 12, 104, 100, 16, DARK[2], DARK[3], extra=RIM)
    for i, c in enumerate(tiles):
        tx, ty = 22 + (i % 3) * 30, 21 + (i // 3) * 29
        body += slab(tx, ty, 24, 22, 6, c[2], c[4], depth=3)
    return body


def artcraft():
    palette = ("M64 22c28 0 52 15 52 36 0 13-11 15-20 15-8 0-12 5-8 12 4 8-4 17-24 17"
               "-28 0-52-16-52-40s24-40 52-40z")
    blobs = [(34, 52, RED), (54, 40, YELLOW), (78, 40, GREEN), (96, 54, BLUE), (62, 64, PURPLE)]
    body = (f'<path d="{palette}" transform="translate(0 6)" fill="{BROWN[3]}"/>'
            f'<path d="{palette}" fill="{BROWN[1]}"/>'
            f'<ellipse cx="44" cy="80" rx="9" ry="7" fill="{BROWN[3]}"/>'
            + "".join(f'<circle cx="{x}" cy="{y + 2}" r="9" fill="{c[4]}"/><circle cx="{x}" cy="{y}" r="9" fill="{c[2]}"/>'
                      for x, y, c in blobs))
    star = "M104 8c1.5 9 4 11.5 13 13-9 1.5-11.5 4-13 13-1.5-9-4-11.5-13-13 9-1.5 11.5-4 13-13z"
    return body + f'<path d="{star}" fill="{YELLOW[1]}"/>'


def photocraft():
    return (slab(26, 14, 88, 70, 8, BLUE[3], BLUE[4])
            + slab(14, 30, 92, 76, 8, LIGHT[1], LIGHT[3])
            + '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
              f'<stop offset="0" stop-color="{BLUE[2]}"/><stop offset="1" stop-color="{BLUE[0]}"/></linearGradient>'
              '<clipPath id="pic"><rect x="22" y="38" width="76" height="60" rx="3"/></clipPath></defs>'
            + '<g clip-path="url(#pic)"><rect x="22" y="38" width="76" height="60" fill="url(#sky)"/>'
            + f'<circle cx="80" cy="56" r="8" fill="{YELLOW[2]}"/>'
            + f'<path d="M14 100l26-34 18 22 12-12 30 24z" fill="{GREEN[4]}"/>'
            + f'<path d="M40 66l8 10-8-3-6 5z" fill="{LIGHT[0]}"/></g>')


def vectorcraft():
    curve = (f'<path d="M14 100C14 60 114 84 114 44" fill="none" stroke="{DARK[2]}" stroke-width="3"/>'
             f'<path d="M14 100V60M114 44v40" stroke="{DARK[0]}" stroke-width="2" fill="none"/>'
             + "".join(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" rx="2" fill="{LIGHT[0]}" stroke="{DARK[2]}" stroke-width="2.5"/>'
                       for x, y in [(14, 100), (114, 44)])
             + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{DARK[2]}"/>' for x, y in [(14, 60), (114, 84)]))
    nib = "M46 14h36v22l16 30-34 46-34-46 16-30z"
    return (curve
            + f'<path d="{nib}" transform="translate(0 6)" fill="{RED[4]}"/>'
            + f'<path d="{nib}" fill="{RED[2]}"/>'
            + f'<path d="M46 14h36v22H46z" fill="{RED[3]}"/>'
            + f'<path d="M64 66v46" stroke="{RED[4]}" stroke-width="3"/>'
            + f'<circle cx="64" cy="68" r="7" fill="{LIGHT[1]}"/><circle cx="64" cy="68" r="3" fill="{RED[4]}"/>')


def filmcraft():
    stripes = "".join(f'<path d="M{18 + i * 20} 0h10l-10 16h-10z" fill="{LIGHT[1]}"/>' for i in range(5))
    clapper = (f'<g transform="rotate(-12 14 44)"><rect x="12" y="30" width="100" height="18" rx="4" fill="{DARK[3]}"/>'
               f'<g transform="translate(12 31)">{stripes}</g></g>')
    return (slab(12, 48, 104, 60, 8, PURPLE[2], PURPLE[4])
            + f'<rect x="12" y="48" width="104" height="14" fill="{DARK[3]}"/>'
            + f'<g transform="translate(12 49)">{stripes}</g>'
            + clapper
            + f'<path d="M56 72v24l20-12z" fill="{LIGHT[0]}" stroke="{LIGHT[0]}" stroke-width="4" stroke-linejoin="round"/>')


def lightcraft():
    cx, cy, r = 64, 60, 38
    # Each blade is a half-plane 13px from the centre; six of them leave a hexagonal opening.
    shades = [YELLOW[3], ORANGE[1], YELLOW[4], ORANGE[2], YELLOW[3], ORANGE[1]]
    blades = "".join(f'<path d="M-13 13H60V60H-60z" transform="translate({cx} {cy}) rotate({i * 60})" '
                     f'fill="{c}" stroke="{ORANGE[4]}" stroke-width="1.5"/>' for i, c in enumerate(shades))
    return (f'<circle cx="{cx}" cy="{cy + 8}" r="52" fill="{DARK[3]}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="52" fill="{DARK[2]}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="44" fill="{DARK[3]}"/>'
            f'<clipPath id="lens"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<g clip-path="url(#lens)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="{DARK[4]}"/>{blades}</g>'
            f'<path d="M38 36a36 36 0 0 1 22-12" stroke="{LIGHT[0]}" stroke-opacity=".5" stroke-width="4" stroke-linecap="round" fill="none"/>')


def pdfcraft():
    shield = "M88 70l20 7v14c0 13-9 21-20 25-11-4-20-12-20-25V77z"
    return (page(18, 10, 82, 104)
            + f'<rect x="18" y="26" width="58" height="16" fill="{RED[3]}"/>'
            + lines(28, 52, [48, 56, 36, 44, 30], 10, LIGHT[3])
            + f'<path d="{shield}" transform="translate(0 4)" fill="{RED[4]}"/>'
            + f'<path d="{shield}" fill="{RED[2]}"/>'
            + f'<path d="M80 92l6 6 11-12" stroke="{LIGHT[0]}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')


def effectcraft():
    star = "M74 18l8 18 20 2-15 13 5 20-18-10-18 10 5-20-15-13 20-2z"
    trails = "".join(f'<path d="M{20 + i * 4} {44 + i * 12}h{30 - i * 6}" stroke="{PINK[1]}" stroke-opacity="{0.9 - i * 0.2:.1f}" stroke-width="5" stroke-linecap="round"/>'
                     for i in range(3))
    keys = "".join(f'<rect x="{x - 6}" y="{98 - 6}" width="12" height="12" rx="2" transform="rotate(45 {x} 98)" fill="{c}"/>'
                   for x, c in [(32, PINK[1]), (64, LIGHT[1]), (96, PINK[1])])
    return (slab(10, 10, 108, 102, 14, DARK[3], DARK[4], extra=RIM)
            + trails
            + f'<path d="{star}" transform="translate(0 4)" fill="{PINK[4]}"/>'
            + f'<path d="{star}" fill="{PINK[2]}" stroke="{PINK[2]}" stroke-width="4" stroke-linejoin="round"/>'
            + f'<rect x="20" y="96" width="88" height="4" rx="2" fill="{DARK[1]}"/>'
            + keys)


def designcraft():
    def spread(dy, fl, fr):
        return (f'<path d="M64 {28 + dy}c-14-6-32-8-52-6v72c20-2 38 0 52 6z" fill="{fl}"/>'
                f'<path d="M64 {28 + dy}c14-6 32-8 52-6v72c-20-2-38 0-52 6z" fill="{fr}"/>')
    return (spread(6, LIGHT[3], LIGHT[4])
            + spread(0, LIGHT[1], LIGHT[0])
            + f'<path d="M20 30c12-1 26 0 36 3v30c-10-3-24-4-36-3z" fill="{LIME[2]}"/>'
            + f'<circle cx="44" cy="42" r="5" fill="{LIME[0]}"/>'
            + f'<path d="M20 58l14-14 22 18v1c-10-3-24-4-36-3z" fill="{LIME[4]}"/>'
            + lines(20, 70, [36, 34, 36], 8, LIGHT[3], 3)
            + lines(72, 34, [36, 32, 36, 30, 36, 34, 22], 8, LIGHT[3], 3)
            + f'<rect x="72" y="92" width="36" height="5" rx="2.5" fill="{LIME[3]}"/>')


def figcraft():
    sel = 'fill="none" stroke="{}" stroke-width="2.5"'.format(GREEN[3])
    handles = "".join(f'<rect x="{x - 3.5}" y="{y - 3.5}" width="7" height="7" fill="{LIGHT[0]}" stroke="{GREEN[3]}" stroke-width="2"/>'
                      for x, y in [(56, 48), (100, 48), (56, 82), (100, 82)])
    cursor = "M86 70v36l9-9 7 15 7-3-7-15h13z"
    return (slab(10, 14, 108, 92, 10, LIGHT[1], LIGHT[3])
            + f'<path d="M20 14h88a10 10 0 0 1 10 10v8H10v-8a10 10 0 0 1 10-10z" fill="{GREEN[3]}"/>'
            + "".join(f'<circle cx="{22 + i * 10}" cy="23" r="3" fill="{LIGHT[0]}" fill-opacity=".8"/>' for i in range(3))
            + f'<rect x="20" y="42" width="26" height="54" rx="3" fill="{LIGHT[2]}"/>'
            + f'<rect x="56" y="48" width="44" height="34" rx="2" fill="{GREEN[0]}"/>'
            + f'<rect x="56" y="48" width="44" height="34" {sel}/>' + handles
            + lines(56, 90, [44], 0, LIGHT[2], 6)
            + f'<path d="{cursor}" fill="{DARK[3]}" stroke="{LIGHT[0]}" stroke-width="3" stroke-linejoin="round"/>')


def wordcraft():
    pen = '<g transform="rotate(40 90 86)">' \
          f'<rect x="84" y="40" width="14" height="44" rx="4" fill="{INDIGO[3]}"/>' \
          f'<rect x="84" y="40" width="7" height="44" rx="3" fill="{INDIGO[2]}"/>' \
          f'<rect x="83" y="76" width="16" height="6" fill="{YELLOW[3]}"/>' \
          f'<path d="M84 82h14l-7 22z" fill="{DARK[2]}"/></g>'
    return (page(16, 10, 84, 104)
            + f'<rect x="28" y="30" width="44" height="7" rx="3.5" fill="{INDIGO[2]}"/>'
            + lines(28, 46, [56, 60, 52, 58, 40, 50, 30], 9, LIGHT[3])
            + pen)


def soundcraft():
    heights = [10, 22, 36, 26, 48, 60, 40, 52, 30, 18, 34, 14]
    bars = "".join(f'<rect x="{22 + i * 7.6:.1f}" y="{60 - h / 2}" width="4.5" height="{h}" rx="2.25" fill="{LIGHT[1]}"/>'
                   for i, h in enumerate(heights))
    return (slab(10, 20, 108, 84, 14, TEAL[2], TEAL[4])
            + f'<rect x="18" y="58" width="92" height="4" fill="{TEAL[3]}"/>'
            + bars
            + f'<circle cx="100" cy="92" r="8" fill="{RED[4]}"/><circle cx="100" cy="90" r="8" fill="{RED[1]}"/>')


def deckcraft():
    return (f'<path d="M64 96v24M64 96l-26 24M64 96l26 24" stroke="{DARK[2]}" stroke-width="5" stroke-linecap="round"/>'
            + slab(10, 18, 108, 76, 6, LIGHT[1], LIGHT[3])
            + f'<rect x="6" y="12" width="116" height="12" rx="4" fill="{ORANGE[3]}"/>'
            + f'<rect x="58" y="4" width="12" height="10" rx="3" fill="{ORANGE[4]}"/>'
            + "".join(f'<rect x="{24 + i * 16}" y="{82 - h}" width="11" height="{h}" rx="2" fill="{c}"/>'
                      for i, (h, c) in enumerate([(18, ORANGE[2]), (32, DARK[2]), (44, ORANGE[2])]))
            + f'<circle cx="94" cy="56" r="14" fill="{ORANGE[1]}"/>'
            + f'<path d="M94 56V42a14 14 0 0 1 14 14z" fill="{ORANGE[3]}"/>'
            + f'<rect x="20" y="82" width="56" height="3" rx="1.5" fill="{DARK[2]}"/>')


def gridcraft():
    x, y, w, h = 14, 14, 100, 94
    grid = "".join(f'<path d="M{x} {y + 18 + i * 13}h{w}" stroke="{LIGHT[2]}" stroke-width="1.5"/>' for i in range(1, 6))
    grid += "".join(f'<path d="M{x + 20 + i * 27} {y}v{h}" stroke="{LIGHT[2]}" stroke-width="1.5"/>' for i in range(3))
    return (slab(x, y, w, h, 8, LIGHT[0], LIGHT[3])
            + f'<clipPath id="sheet"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/></clipPath>'
            + f'<g clip-path="url(#sheet)"><rect x="{x}" y="{y}" width="{w}" height="18" fill="{GREEN[4]}"/>'
            + f'<rect x="{x}" y="{y + 18}" width="20" height="{h}" fill="{GREEN[0]}" fill-opacity=".45"/>{grid}</g>'
            + f'<rect x="{x + 47}" y="{y + 44}" width="27" height="13" fill="{GREEN[1]}" fill-opacity=".35" stroke="{GREEN[4]}" stroke-width="3"/>'
            + f'<rect x="{x + 71}" y="{y + 54}" width="6" height="6" fill="{GREEN[4]}"/>')


def cadcraft():
    grid = "".join(f'<path d="M{14 + i * 10} 14v94M14 {14 + i * 10}h100" stroke="{LIGHT[0]}" stroke-opacity=".15" stroke-width="1"/>'
                   for i in range(1, 10))
    square = "M26 32v66h66zM38 62v24h24z"
    return (slab(10, 10, 108, 102, 12, TEAL[3], TEAL[4])
            + f'<clipPath id="bp"><rect x="10" y="10" width="108" height="102" rx="12"/></clipPath><g clip-path="url(#bp)">{grid}</g>'
            + f'<path d="{square}" fill="{LIGHT[1]}" fill-rule="evenodd"/>'
            + lines(29, 40, [5, 9, 5, 9, 5, 9, 5], 7, TEAL[3], 1.6)
            + f'<path d="M60 30a42 42 0 0 1 44 42" stroke="{DARK[3]}" stroke-width="4" stroke-linecap="round" fill="none"/>'
            + f'<circle cx="104" cy="74" r="6" fill="{ORANGE[2]}"/><circle cx="60" cy="30" r="5" fill="{DARK[3]}"/>')


def texturecraft():
    top, left, right = "M64 14l46 24-46 24-46-24z", "M18 38l46 24v52L18 90z", "M110 38L64 62v52l46-24z"
    stripes = "".join(f'<path d="M{-10 + i * 18} 0l40 140h8L{-2 + i * 18} 0z" fill="{DARK[3]}"/>' for i in range(9))
    out = ""
    for i, (shape, base) in enumerate([(top, LIGHT[0]), (left, LIGHT[2]), (right, BROWN[0])]):
        out += (f'<clipPath id="f{i}"><path d="{shape}"/></clipPath>'
                f'<g clip-path="url(#f{i})"><path d="{shape}" fill="{base}"/>{stripes}</g>')
    brush = (f'<g transform="rotate(35 96 92)"><rect x="90" y="56" width="12" height="40" rx="5" fill="{BROWN[2]}"/>'
             f'<rect x="88" y="92" width="16" height="10" fill="{LIGHT[3]}"/>'
             f'<path d="M88 102h16v6c0 8-4 14-8 16-4-2-8-8-8-16z" fill="{ORANGE[4]}"/></g>')
    return (f'<path d="M18 46l46 24 46-24v52l-46 24-46-24z" fill="{DARK[3]}"/>'
            + out
            + f'<path d="M18 38l46 24 46-24M64 62v52" stroke="{DARK[3]}" stroke-width="2" fill="none"/>'
            + brush)


def materialcraft():
    nodes = "".join(slab(8, y, 30, 18, 4, LIGHT[1], LIGHT[3], depth=3)
                    + f'<rect x="8" y="{y}" width="30" height="6" rx="3" fill="{c}"/>'
                    + f'<circle cx="38" cy="{y + 11}" r="3.5" fill="{c}"/>'
                    for y, c in [(20, TEAL[2]), (52, ORANGE[2]), (84, PURPLE[1])])
    wires = "".join(f'<path d="M38 {y}C56 {y} 52 64 66 64" stroke="{LIGHT[4]}" stroke-width="3" fill="none"/>'
                    for y in (31, 63, 95))
    return ('<defs><radialGradient id="ball" cx=".35" cy=".3" r=".75">'
            f'<stop offset="0" stop-color="{TEAL[0]}"/><stop offset=".45" stop-color="{TEAL[2]}"/>'
            f'<stop offset="1" stop-color="{TEAL[4]}"/></radialGradient></defs>'
            + wires + nodes
            + f'<ellipse cx="86" cy="110" rx="32" ry="8" fill="{DARK[4]}" fill-opacity=".25"/>'
            + '<circle cx="86" cy="68" r="36" fill="url(#ball)"/>'
            + f'<ellipse cx="74" cy="52" rx="10" ry="6" transform="rotate(-35 74 52)" fill="{LIGHT[0]}" fill-opacity=".75"/>')


def craft_anything():
    code = (f'<path d="M34 48l-12 14 12 14M74 48l12 14-12 14M60 42l-12 40" stroke="{BLUE[1]}" stroke-width="6" '
            'stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
    return (slab(10, 14, 100, 80, 10, DARK[3], DARK[4], extra=RIM)
            + f'<path d="M20 14h80a10 10 0 0 1 10 10v6H10v-6a10 10 0 0 1 10-10z" fill="{DARK[2]}"/>'
            + "".join(f'<circle cx="{20 + i * 9}" cy="22" r="2.8" fill="{c}"/>' for i, c in enumerate([RED[1], YELLOW[2], GREEN[2]]))
            + code
            + f'<path d="M100 96l18 18" stroke="{DARK[3]}" stroke-width="12" stroke-linecap="round"/>'
            + f'<path d="M100 96l18 18" stroke="{INDIGO[3]}" stroke-width="7" stroke-linecap="round"/>'
            + f'<circle cx="88" cy="84" r="22" fill="{BLUE[0]}" fill-opacity=".45" stroke="{INDIGO[3]}" stroke-width="7"/>'
            + f'<path d="M76 76a14 14 0 0 1 10-6" stroke="{LIGHT[0]}" stroke-width="3" stroke-linecap="round" fill="none"/>')


def iso_box(x0, y0, z0, dx, dy, dz, top, left, right, s=11, ox=64, oy=70):
    def p(x, y, z):
        return f"{ox + (x - y) * s * 0.866:.1f} {oy + (x + y) * s * 0.5 - z * s:.1f}"
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + dz
    return (f'<path d="M{p(x0, y1, z0)}L{p(x1, y1, z0)}L{p(x1, y1, z1)}L{p(x0, y1, z1)}z" fill="{left}"/>'
            f'<path d="M{p(x1, y0, z0)}L{p(x1, y1, z0)}L{p(x1, y1, z1)}L{p(x1, y0, z1)}z" fill="{right}"/>'
            f'<path d="M{p(x0, y0, z1)}L{p(x1, y0, z1)}L{p(x1, y1, z1)}L{p(x0, y1, z1)}z" fill="{top}"/>')


def solidcraft():
    # A stepped (L-profile) solid: a low slab with a taller block on its back half.
    return (iso_box(-2.5, -2.5, -1.4, 5, 5, 1.6, BLUE[0], BLUE[2], BLUE[4])
            + iso_box(-2.5, -2.5, 0.2, 5, 2.4, 2.4, BLUE[0], BLUE[2], BLUE[4]))


ICONS = {
    "ai.storyteller.artcraft-launcher": launcher,
    "ai.storyteller.artcraft": artcraft,
    "ai.storyteller.photocraft": photocraft,
    "ai.storyteller.vectorcraft": vectorcraft,
    "ai.storyteller.filmcraft": filmcraft,
    "ai.storyteller.lightcraft": lightcraft,
    "ai.storyteller.pdfcraft": pdfcraft,
    "ai.storyteller.effectcraft": effectcraft,
    "ai.storyteller.designcraft": designcraft,
    "ai.storyteller.figcraft": figcraft,
    "ai.storyteller.wordcraft": wordcraft,
    "ai.storyteller.soundcraft": soundcraft,
    "ai.storyteller.deckcraft": deckcraft,
    "ai.storyteller.gridcraft": gridcraft,
    "ai.storyteller.cadcraft": cadcraft,
    "ai.storyteller.texturecraft": texturecraft,
    "ai.storyteller.materialcraft": materialcraft,
    "ai.storyteller.craft-anything": craft_anything,
    "io.tangencylabs.solidcraft": solidcraft,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in ICONS.items():
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">{draw()}</svg>\n'
        path = OUT / f"{name}.svg"
        path.write_text(svg)
        for size in SIZES:
            png = ROOT / f"{size}x{size}" / "apps" / f"{name}.png"
            png.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["inkscape", path, "-w", str(size), "-h", str(size), "-o", png],
                           check=True, stderr=subprocess.DEVNULL)
    print(f"wrote {len(ICONS)} icons to {ROOT}")
