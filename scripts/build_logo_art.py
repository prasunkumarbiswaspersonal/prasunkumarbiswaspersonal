#!/usr/bin/env python3
"""Generate a full-color vector logo footer; Python standard library only."""
from html import escape
from pathlib import Path
import argparse
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'Assets' / 'profile'
ET.register_namespace('', 'http://www.w3.org/2000/svg')

# Update the icon list to your tech stack
tech_stack = [
    "python",
    "c",
    "cplusplus",
    "kotlin",
    "javascript",
    "react",
    "arduino",
    "linux",
    "github",
    "git"
]

CYCLE = float(len(tech_stack) * 2)


def text(x, y, value, size=12, cls='name', anchor='middle'):
    return f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" font-size="{size}">{escape(value)}</text>'


def vector(icon, size):
    """Keep paths, colors, transforms and gradients from the source SVG."""
    root = ET.fromstring(icon['svg'])
    for key in ('width', 'height', 'style', 'class', 'role', 'aria-labelledby'):
        root.attrib.pop(key, None)
    root.set('width', str(size))
    root.set('height', str(size))
    ids = {e.get('id'): icon['id'] + '-' + e.get('id') for e in root.iter() if e.get('id')}
    for node in root.iter():
        for key, value in list(node.attrib.items()):
            if key == 'id':
                node.set(key, ids[value])
            else:
                for old, new in ids.items():
                    value = value.replace('url(#' + old + ')', 'url(#' + new + ')')
                    if value == '#' + old:
                        value = '#' + new
                node.set(key, value)
    return ET.tostring(root, encoding='unicode')


def underline_opacity(t, index):
    phase = ((t - index * 2) % CYCLE) / CYCLE
    keys = ((0, 1), (.10, 1), (.143, 0), (.95, 0), (1, 1))
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t0 <= phase <= t1:
            return v0 + (v1 - v0) * (phase - t0) / (t1 - t0)
    return 0


def build(mobile=False, frame=None):
    all_icons = json.loads((ART / 'toolbox-logos.json').read_text(encoding='utf-8'))
    icon_map = {icon['id']: icon for icon in all_icons}
    icons = [icon_map[tech] for tech in tech_stack if tech in icon_map]

    w, h = (420, 328) if mobile else (850, 202)
    parts = [
        text(w / 2, 25, 'TOOLBOX', 10, 'heading'),
        f'<path class="rule" d="M22 21H{w/2-65:g}M{w/2+65:g} 21H{w-22}"/>'
    ]
    css = []
    n = len(icons)
    for i, icon in enumerate(icons):
        if mobile:
            size = 46
            if icon['id'] == 'linux':
                size += 6
            row = i // 5
            col = i % 5
            cx = 58 + col * 76
            cy = 88 + row * 130
            label_y = 138 + row * 130
        else:
            size = 48
            if icon['id'] == 'linux':
                size += 6
            step = 76
            start_x = (w - (n - 1) * step) / 2
            cx = start_x + i * step
            cy = 98
            label_y = 154

        x = cx - size / 2
        y = cy - size / 2
        cls = 'logo ink' if icon.get('monochrome') else 'logo'
        parts += [
            f'<g class="{cls}" id="brand-{icon["id"]}">',
            f'<g transform="translate({x:g} {y:g})"><g class="float f{i}">',
            vector(icon, size),
            '</g></g>',
            text(cx, label_y, icon['label'], 10 if mobile else 11),
            f'<path class="underline u{i}" d="M{cx-9:g} {label_y+13:g}h18"/>',
            '</g>'
        ]
        css += [
            f'.f{i}{{animation-delay:{-i*.6:g}s}}',
            f'.u{i}{{animation-delay:{i*2-CYCLE:g}s}}'
        ]
        if frame is not None:
            phase = ((frame + i * .6) / 7) % 1
            dy = -3 * (1 - abs(phase * 2 - 1))
            css += [
                f'.f{i}{{animation:none;transform:translateY({dy:.4f}px)}}',
                f'.u{i}{{animation:none;opacity:{underline_opacity(frame,i):.4f}}}'
            ]
    parts.append(text(w / 2, 318 if mobile else 197, 'BUILD. COMMIT. REPEAT.', 9, 'signature'))
    names = ", ".join(icon['label'].title() for icon in icons)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(names)}</title>
<desc id="desc">Animated tech stack icons for {escape(names)} with a slow float and a travelling underline.</desc>
<style>
text{{font-family:ui-monospace,'DejaVu Sans Mono',Consolas,monospace;font-weight:400}}
.heading{{fill:#a0a8b2;letter-spacing:3px}}.name{{fill:#e6edf3;letter-spacing:.6px}}.signature{{fill:#68737d;letter-spacing:1.7px}}.rule{{fill:none;stroke:#29313a}}.ink{{color:#f5f5f5}}
.underline{{fill:none;stroke:#a7c9aa;stroke-width:1.5;opacity:0;animation:underline {CYCLE:g}s linear infinite}}
.float{{animation:float 7s linear infinite}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-3px)}}}}
@keyframes underline{{0%,10%{{opacity:1}}14.3%,95%{{opacity:0}}100%{{opacity:1}}}}
@media(prefers-color-scheme:light){{.heading{{fill:#64707a}}.name{{fill:#24292f}}.signature{{fill:#78838b}}.rule{{stroke:#d8dee4}}.ink{{color:#181717}}.underline{{stroke:#526d5b}}}}
{''.join(css)}
@media(prefers-reduced-motion:reduce){{.float,.underline{{animation:none;transform:none}}.underline{{opacity:0}}}}
</style>
{''.join(parts)}
</svg>
'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frame', type=float, help='Static animation time for previews')
    p.add_argument('--output', type=Path, help='Preview directory; defaults to Assets/profile')
    args = p.parse_args()
    out = args.output or ART
    out.mkdir(parents=True, exist_ok=True)
    for mobile in (False, True):
        suffix = '-mobile' if mobile else ''
        dest = out / f'toolbox-footer{suffix}.svg'
        dest.write_text(build(mobile, args.frame), encoding='utf-8')
        print(f"Generated {dest}")


if __name__ == '__main__':
    main()
