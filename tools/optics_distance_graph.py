#!/usr/bin/env python3
"""Compare concave and convex mirrors using one signed mirror equation."""
import os
from pathlib import Path
from tempfile import gettempdir

ROOT = Path(__file__).resolve().parents[1]


def build_distance_graph():
    os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/notes-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    output = ROOT / 'assets/optics-notes/mirror-distance-graph.svg'
    preview = Path(gettempdir()) / 'physics11-mirror-distance-graph.png'
    style = {
        'svg.fonttype': 'none', 'svg.hashsalt': 'physics11-mirror-distance',
        'font.family': 'DejaVu Sans', 'font.size': 13,
        'text.color': '#203440', 'axes.labelcolor': '#203440',
        'axes.edgecolor': '#647a84', 'xtick.color': '#203440', 'ytick.color': '#203440',
    }
    with plt.rc_context(style):
        fig, ax = plt.subplots(figsize=(9.6, 7.2))
        fig.subplots_adjust(left=.13, right=.96, bottom=.19, top=.79)
        fig.suptitle('One equation works for both mirror shapes', x=.52, y=.97,
                     fontsize=17, fontweight='bold', color='#075d64')
        fig.text(.52, .915, '1/f = 1/dₒ + 1/dᵢ     →     dᵢ = f dₒ / (dₒ − f)',
                 ha='center', fontsize=14)
        f = 20.0
        ax.set(xlim=(0, 120), ylim=(-90, 130),
               xlabel='Object distance dₒ (cm), measured from V',
               ylabel='Signed image distance dᵢ (cm), measured from V',
               xticks=np.arange(0, 121, 20), yticks=np.arange(-80, 121, 20))
        ax.axhspan(0, 130, color='#eef7f5', zorder=0)
        ax.axhspan(-90, 0, color='#fcf1ed', zorder=0)
        ax.grid(alpha=.22)
        ax.axhline(0, color='#647a84', lw=1.3)
        ax.axvline(f, color='#647a84', lw=1.5, linestyle=(0, (5, 4)))
        # Never draw a connecting segment across the undefined value dₒ = f.
        for index, x in enumerate((np.linspace(.05, 19.95, 1500),
                                   np.linspace(20.05, 120, 1800))):
            y = f*x/(x-f)
            ax.plot(x, y, color='#086b72', lw=3, clip_on=True,
                    label='Concave: f = +20.0 cm' if index == 0 else None)
        convex_x = np.linspace(.05, 120, 1800)
        convex_f = -20.0
        ax.plot(convex_x, convex_f*convex_x/(convex_x-convex_f),
                color='#8d315f', lw=3, linestyle='--', label='Convex: f = −20.0 cm')
        fig.legend(loc='center', bbox_to_anchor=(.54, .855), ncol=2,
                   fontsize=12, frameon=False, handlelength=3)
        ax.text(66, 113, 'dᵢ > 0: real image in front', ha='center',
                fontsize=13, color='#075d64')
        ax.text(73, -76, 'dᵢ < 0: virtual image behind', ha='center',
                fontsize=13, color='#944322')
        ax.text(36, 94, 'Concave: object at F\nNo finite image', ha='left', va='top',
                fontsize=11, color='#526875')
        for x, focal_length, label, location, color in (
            (100, 20., 'Concave: (100, +25.0)', (77, 65), '#086b72'),
            (100, -20., 'Convex: (100, −16.7)', (84, -50), '#8d315f'),
            (10, 20., 'Concave: (10.0, −20.0)', (44, -35), '#086b72'),
        ):
            y = focal_length*x/(x-focal_length)
            ax.plot(x, y, 'o', color=color, markersize=8)
            ax.plot([x, x], [0, y], color=color, lw=1, linestyle=':')
            ax.plot([0, x], [y, y], color=color, lw=1, linestyle=':')
            ax.annotate(label, xy=(x, y), xytext=location, ha='center', fontsize=12,
                        color=color, bbox={'boxstyle': 'round,pad=.35', 'fc': 'white', 'ec': color},
                        arrowprops={'arrowstyle': '->', 'color': color, 'lw': 1.2})
        fig.text(.13, .085, 'Labelled points: (object distance, image distance), both in cm.', fontsize=12)
        fig.text(.13, .048, 'Grey vertical line: dₒ = +20.0 cm; only the concave curve is undefined there.',
                 fontsize=11, color='#526875')
        fig.text(.13, .015, 'Model graph for real objects (dₒ > 0). Curves continue beyond the range shown.',
                 fontsize=11, color='#526875')
        output.parent.mkdir(exist_ok=True)
        fig.savefig(output, format='svg', metadata={'Date': None})
        fig.savefig(preview, dpi=140)
        plt.close(fig)
    print('Built mirror-distance graph SVG and temporary PNG preview.')


if __name__ == '__main__':
    build_distance_graph()
