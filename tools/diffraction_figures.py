"""Generate the model diffraction intensity plot used by the optional tutorial."""
from pathlib import Path
import os
import tempfile


def build_pattern():
    os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'physics11-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.fonttype': 'path'})
    angles = np.linspace(-90, 90, 4001)
    fig, ax = plt.subplots(figsize=(9.6, 5.8))
    for ratio, colour, style in [(0.5, '#087cff', '-'), (1, '#086b72', '--'), (5, '#bd4b24', '-')]:
        # numpy.sinc(x) = sin(pi*x)/(pi*x), including its limiting value at zero.
        intensity = np.sinc(ratio * np.sin(np.deg2rad(angles))) ** 2
        ax.plot(angles, intensity, color=colour, linestyle=style, linewidth=2.4,
                label=f'b/λ = {ratio:g}')
    first = np.rad2deg(np.arcsin(1 / 5))
    ax.plot([-first, first], [0, 0], 'o', color='#bd4b24', markersize=5)
    ax.annotate('b = 5λ: first minimum at 11.5°', xy=(first, 0), xytext=(25, .23),
                fontsize=10, color='#9b3a19', arrowprops={'arrowstyle': '->', 'color': '#bd4b24'},
                bbox={'boxstyle': 'round,pad=.3', 'facecolor': 'white', 'edgecolor': 'none', 'alpha': .95})
    ax.set(xlim=(-90, 90), ylim=(-.025, 1.05), xlabel='Angle θ from the normal (degrees)',
           ylabel='Normalized intensity I(θ)/I(0)', xticks=np.arange(-90, 91, 30))
    ax.grid(alpha=.2)
    ax.legend(loc='upper right', framealpha=.95)
    ax.spines[['top', 'right']].set_visible(False)
    fig.suptitle('Smaller b/λ gives a broader angular pattern', fontsize=17, fontweight='bold', y=.98)
    fig.text(.5, .905, 'Ideal scalar single-slit model · each curve is normalized to its own central maximum',
             ha='center', fontsize=10, color='#526875')
    fig.text(.5, .02, 'Model calculations, not measured ripple-tank data. Width changes the pattern shape.',
             ha='center', fontsize=10, color='#526875')
    fig.tight_layout(rect=(0, .055, 1, .90))
    output = Path(__file__).resolve().parents[1] / 'assets/wave-motion-notes/diffraction-width-pattern.svg'
    fig.savefig(output, metadata={'Date': None, 'Creator': 'Physics11 diffraction_figures.py'})
    output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines()) + '\n')
    plt.close(fig)
    return output


if __name__ == '__main__':
    print(build_pattern())
