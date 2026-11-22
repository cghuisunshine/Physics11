#!/usr/bin/env python3
"""Draw a qualitative, same-scale crest comparison for diffraction Station 5."""
from pathlib import Path
import os
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def build_diffraction_openings_obstacles():
    os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'physics11-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'Physics11-diffraction-obstacles'})
    # A scalar transmission-plane illustration. Internal coordinates use wavelengths;
    # the student figure gives only the qualitative Physics 11 interpretation.
    count, samples_per_wavelength = 8192, 48
    y = (np.arange(count) - count // 2) / samples_per_wavelength
    x = np.linspace(.04, 9, 380)
    transverse_k = 2 * np.pi * np.fft.fftfreq(count, d=1 / samples_per_wavelength)
    forward_k = np.sqrt((2 * np.pi) ** 2 - transverse_k ** 2 + 0j)
    propagation = np.exp(1j * x[:, None] * forward_k[None, :])
    visible = np.abs(y) <= 4.5
    figure, axes = plt.subplots(2, 2, figsize=(12, 10.8))
    cases = [
        ('opening', 1, 'A · 2.0 cm opening: width = λ',
         'Broad spreading beyond the opening.'),
        ('opening', 5, 'B · 10 cm opening: width = 5λ',
         'More forward travel; edges still spread.'),
        ('obstacle', 5, 'C · Large obstacle: several λ wide',
         'A clearer shadow, with bending at the edges.'),
        ('obstacle', .25, 'D · Very small obstacle: width < λ',
         'Waves spread around it; little lasting shadow.'),
    ]
    for ax, (kind, width, title, caption) in zip(axes.flat, cases):
        aperture = np.clip((width / 2 - np.abs(y)) * samples_per_wavelength + .5, 0, 1)
        transmission = aperture if kind == 'opening' else 1 - aperture
        field = np.fft.ifft(propagation * np.fft.fft(transmission)[None, :], axis=1)[:, visible]
        ax.set_facecolor('#edf6f8')
        if kind == 'obstacle' and width > 1:
            ax.add_patch(Rectangle((0, -width / 2), 9, width, color='#dce3e6', zorder=0))
        # Only the positive real branch is crest phase. Suppress very weak fields,
        # where phase lines would falsely suggest prominent visible crests.
        crest_phase = np.ma.masked_where(field.real < .08, field.imag)
        ax.contour(x, y[visible], crest_phase.T, levels=[0], colors='#086b72', linewidths=1.25)
        for position in (-3, -2, -1):
            ax.plot([position, position], [-4.5, 4.5], color='#086b72', linewidth=1.25)
        if kind == 'opening':
            for bottom, top in [(-4.5, -width / 2), (width / 2, 4.5)]:
                ax.plot([0, 0], [bottom, top], color='#182e3c', linewidth=7, solid_capstyle='butt')
        else:
            ax.plot([0, 0], [-width / 2, width / 2], color='#182e3c', linewidth=8,
                    solid_capstyle='butt', zorder=5)
        ax.annotate('', xy=(-.45, 3.5), xytext=(-3.25, 3.5),
                    arrowprops={'arrowstyle': '->', 'color': '#a54d12', 'lw': 2})
        ax.text(-3.2, 3.95, 'Incoming', color='#a54d12', fontsize=10,
                bbox={'facecolor': '#edf6f8', 'edgecolor': 'none', 'pad': 1})
        if kind == 'obstacle' and width > 1:
            ax.text(1.2, .35, 'Shadow', fontsize=12, color='#354d59', weight='bold',
                    bbox={'facecolor': '#dce3e6', 'edgecolor': 'none', 'pad': 2})
            ax.text(1.2, -.35, '(weaker waves)', fontsize=10, color='#354d59',
                    bbox={'facecolor': '#dce3e6', 'edgecolor': 'none', 'pad': 2})
        ax.set(xlim=(-3.5, 9), ylim=(-4.5, 4.5), xticks=[], yticks=[])
        ax.set_aspect('equal')
        for spine in ax.spines.values():
            spine.set_color('#bdcfd5')
        ax.set_title(title, loc='left', fontsize=13, fontweight='bold', pad=13, color='#182e3c')
        ax.text(.5, -.08, caption, ha='center', va='top', transform=ax.transAxes,
                fontsize=11, color='#182e3c')

    figure.suptitle('Diffraction: openings and obstacles', x=.05, ha='left', y=.975,
                   fontsize=23, fontweight='bold', color='#182e3c')
    figure.text(.05, .922, 'Top views · same wavelength λ = 2.0 cm · same water depth · same scale',
                fontsize=12, color='#526875')
    figure.text(.05, .054, 'Teal lines mark crests; arrows show incoming travel. Dark bars are barriers or obstacles.',
                fontsize=11, color='#526875')
    figure.text(.05, .025, 'Illustrative wave model. A shadow has weaker waves, not necessarily zero waves. Reflections are omitted.',
                fontsize=10, color='#526875')
    figure.subplots_adjust(left=.05, right=.98, top=.875, bottom=.12, wspace=.16, hspace=.34)
    output = ROOT / 'assets/wave-motion-notes/diffraction-openings-obstacles'
    figure.savefig(output.with_suffix('.svg'), metadata={'Date': None, 'Creator': 'Physics11 diffraction_openings_obstacles.py'})
    svg = output.with_suffix('.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines()) + '\n')
    figure.savefig(output.with_suffix('.png'), dpi=150)
    plt.close(figure)
    print('Built diffraction-openings-obstacles.svg and .png.')


if __name__ == '__main__':
    build_diffraction_openings_obstacles()
