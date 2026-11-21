#!/usr/bin/env python3
"""Build the standalone ripple-tank animation using only the Python standard library."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_ripple_tank_animation():
    template = (ROOT / 'tools/ripple-tank-animation-template.html').read_text()
    script = (ROOT / 'tools/ripple-tank-animation.js').read_text()
    assert template.count('{{ANIMATION_SCRIPT}}') == 1
    assert '</script' not in script.lower()
    page = template.replace('{{ANIMATION_SCRIPT}}', script)
    assert '{{' not in page
    (ROOT / 'ripple-tank-animation.html').write_text(page)
    print('Built ripple-tank-animation.html: offline wavefront and optical-projection animation.')


if __name__ == '__main__':
    build_ripple_tank_animation()
