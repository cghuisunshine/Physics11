#!/usr/bin/env python3
"""Generate question and answer pictures for pulse and path-difference interference."""
from pathlib import Path
import os
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def build_interference_station_figures():
    os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'physics11-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'Physics11-interference-station'})
    ink, muted, first, second, total = '#182e3c', '#526875', '#086b72', '#ad4e16', '#183b78'
    x = np.linspace(0, 10, 1001)
    pulse = lambda centre: np.maximum(0, 1 - np.abs(x - centre) / 1.15)
    for answer in (False, True):
        fig, axes = plt.subplots(2, 2, figsize=(12, 11.6))
        for ax in axes.flat:
            ax.set_facecolor('#f1f7f8')
            ax.set(xticks=[], yticks=[])
            for spine in ax.spines.values(): spine.set_color('#c5d6da')

        for ax, sign, title in zip(axes[0], (1, -1), ('A · Same-sign spring pulses', 'B · Opposite-sign spring pulses')):
            amplitude, before = .7, 3.3
            ax.set(xlim=(0, 10), ylim=(-.8, 5.05))
            ax.set_title(title, loc='left', fontsize=14, fontweight='bold', pad=13, color=ink)
            ax.text(.3, 4.8, 'Before overlap', color=muted, fontsize=11)
            ax.axhline(before, color='#b6cbd1', linewidth=1)
            for centre, colour, direction in ((2.5, first, 1), (7.5, second, -1)):
                shape = before + amplitude * (sign if centre == 7.5 else 1) * pulse(centre)
                selected = np.abs(x - centre) <= 1.16
                ax.plot(x[selected], shape[selected], color=colour, linewidth=2.5)
                ax.annotate('', xy=(centre + .6 * direction, 4.47), xytext=(centre - .6 * direction, 4.47),
                            arrowprops={'arrowstyle': '->', 'color': colour, 'lw': 2})
            ax.text(2.5, 4.1, '+A', ha='center', color=first, fontsize=12, weight='bold')
            ax.text(7.5, 4.1 if sign == 1 else 2.25, '+A' if sign == 1 else '−A',
                    ha='center', color=second, fontsize=12, weight='bold')
            ax.text(.2, before + .08, '0', color=muted, fontsize=10)
            ax.text(.3, 1.95, 'At exact overlap', color=muted, fontsize=11)
            ax.axhline(0, color='#b6cbd1', linewidth=1)
            ax.text(.2, .08, '0', color=muted, fontsize=10)
            if answer:
                resultant = (1 + sign) * amplitude * pulse(5)
                ax.plot(x, resultant, color=total, linewidth=2.6)
                ax.text(5.25, 1.48 if sign == 1 else .22, '+2A' if sign == 1 else 'Zero displacement',
                        color=total, fontsize=12, weight='bold')
            else:
                ax.add_patch(Rectangle((3.4, -.35), 3.2, 1.95, facecolor='white', edgecolor='#8fa9b4',
                                       linestyle='--', linewidth=1.2))
                ax.text(5, .55, 'Sketch the\nresultant here', ha='center', va='center', color=muted, fontsize=11)
            ax.text(9.7, -.57, 'Position along spring', ha='right', fontsize=10, color=muted)
            caption = ('+A + (+A) = +2A' if sign == 1 else '+A + (−A) = 0') if answer else 'Add signed displacements at each position.'
            ax.text(.5, -.075, caption, transform=ax.transAxes, ha='center', va='top', fontsize=12, color=total)

        for ax, longer, title in zip(axes[1], (4, 4.5), ('C · Path difference = 1.0λ', 'D · Path difference = 1.5λ')):
            # Identical source separation in both pictures, with all lengths in wavelengths.
            # Solve two circle-distance constraints to locate the observation point.
            source1, source2, short = np.array([0., 1.5]), np.array([0., -1.5]), 3.
            py = (longer ** 2 - short ** 2) / 6
            point = np.array([np.sqrt(short ** 2 - (py - 1.5) ** 2), py])
            assert np.isclose(np.linalg.norm(point - source1), short)
            assert np.isclose(np.linalg.norm(point - source2), longer)
            ax.set(xlim=(-.7, 6), ylim=(-2.25, 2.85), aspect='equal')
            ax.set_title(title, loc='left', fontsize=14, fontweight='bold', pad=13, color=ink)
            ax.text(-.45, 2.48, 'S₁ and S₂ oscillate in phase.', fontsize=11, color=muted)
            for source, name, colour, length in ((source1, 'S₁', first, short), (source2, 'S₂', second, longer)):
                ax.plot(*source, marker='o', markersize=7, color=colour)
                ax.text(source[0] - .5, source[1] -.08, name, color=colour, fontsize=12, weight='bold')
                ax.plot([source[0], point[0]], [source[1], point[1]], color=colour, linewidth=1.9)
                along = source + .65 * (point - source)
                previous = source + .43 * (point - source)
                ax.annotate('', xy=along, xytext=previous, arrowprops={'arrowstyle': '->', 'lw': 1.9, 'color': colour})
                midpoint = (source + point) / 2
                offset = .26 if length == short else -.36
                label = f'r₁ = {short:g}λ' if length == short else f'r₂ = {longer:g}λ'
                ax.text(midpoint[0] -.12, midpoint[1] + offset, label, fontsize=11, color=colour,
                        bbox={'facecolor': '#f1f7f8', 'edgecolor': 'none', 'pad': 1.5})
            ax.plot(*point, marker='o', markersize=5, color=ink)
            ax.text(point[0] + .14, point[1] -.12, 'P', color=ink, fontsize=12, weight='bold')
            if answer:
                phases = ax.inset_axes([.61, .24, .36, .51])
                phases.set_facecolor('white')
                time = np.linspace(0, 2, 300)
                phases.plot(time, 1.4 + .28 * np.cos(2 * np.pi * time), color=first, linewidth=1.8)
                opposite = 1 if longer == 4 else -1
                phases.plot(time, .45 + opposite * .28 * np.cos(2 * np.pi * time), color=second, linewidth=1.8)
                phases.set(xlim=(0, 2), ylim=(-.05, 1.95), xticks=[], yticks=[])
                for spine in phases.spines.values(): spine.set_visible(False)
                phases.text(.05, 1.78, 'At P: wave 1', color=first, fontsize=9)
                phases.text(.05, .83, 'At P: wave 2', color=second, fontsize=9)
                phases.text(1, -.02, 'same time scale', ha='center', fontsize=8, color=muted)
                caption = 'Constructive: arrivals in phase.' if longer == 4 else 'Destructive: arrivals opposite in phase.'
            else:
                ax.text(4.65, .25, 'Reinforce\nor cancel?', ha='center', va='center', color=muted, fontsize=13,
                        bbox={'facecolor': 'white', 'edgecolor': '#c5d6da', 'boxstyle': 'round,pad=.5'})
                caption = 'Decide how the waves combine at P.'
            ax.text(.5, -.075, caption, transform=ax.transAxes, ha='center', va='top', fontsize=11, color=ink)

        fig.suptitle('Interference: pulses and two in-phase sources', x=.05, ha='left', y=.975,
                     fontsize=22, fontweight='bold', color=ink)
        fig.text(.05, .93, ('Worked answer' if answer else 'Question picture') +
                 ' · Spring graphs show displacement against position; lower diagrams show paths in water.',
                 fontsize=11, color=muted)
        fig.text(.05, .067, 'Pulses continue after overlap. Temporary cancellation does not destroy the pulses.', fontsize=11, color=muted)
        fig.text(.05, .029, 'Lower paths are illustrative. Complete cancellation needs equal arriving amplitudes at P.', fontsize=11, color=muted)
        fig.subplots_adjust(left=.05, right=.98, top=.875, bottom=.13, wspace=.16, hspace=.33)
        kind = 'answer' if answer else 'question'
        output = ROOT / f'assets/wave-motion-notes/interference-station-{kind}'
        fig.savefig(output.with_suffix('.svg'), metadata={'Date': None, 'Creator': 'Physics11 interference_station_figures.py'})
        svg = output.with_suffix('.svg')
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
        fig.savefig(output.with_suffix('.png'), dpi=150)
        plt.close(fig)
    print('Built interference-station question and answer SVG/PNG pictures.')


if __name__ == '__main__':
    build_interference_station_figures()
