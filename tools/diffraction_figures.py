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

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.fonttype': 'path', 'svg.hashsalt': 'Physics11-diffraction'})
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


def build_wavefronts():
    """Propagate an in-phase opening with the scalar angular-spectrum model."""
    os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'physics11-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11, 'svg.fonttype': 'path', 'svg.hashsalt': 'Physics11-diffraction'})
    # Distances are in wavelengths. Padding keeps periodic replicas far from the displayed region.
    count = 8192
    y = (np.arange(count) - count // 2) / 32
    x = np.linspace(.08, 10, 450)
    transverse_k = 2 * np.pi * np.fft.fftfreq(count, d=1/32)
    forward_k = np.sqrt((2 * np.pi) ** 2 - transverse_k ** 2 + 0j)
    propagation = np.exp(1j * x[:, None] * forward_k[None, :])
    visible = np.abs(y) <= 6
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 8), sharex=True, sharey=True)
    for ax, ratio in zip(axes, [.5, 5]):
        # Fractional edge cells approximate a uniform top-hat aperture without a width-rounding bias.
        aperture = np.clip((ratio / 2 - np.abs(y)) * 32 + .5, 0, 1)
        field = np.fft.ifft(propagation * np.fft.fft(aperture)[None, :], axis=1)[:, visible]
        scale = np.max(np.abs(field))
        displacement = field.real / scale
        ax.pcolormesh(x, y[visible], displacement.T, shading='auto', cmap='RdBu_r',
                      vmin=-.55, vmax=.55, rasterized=True)
        # Imaginary part zero with positive real part marks equal crest phase, not trough phase.
        crests = np.ma.masked_where(field.real < .025 * scale, field.imag)
        ax.contour(x, y[visible], crests.T, levels=[0], colors='#182e3c', linewidths=.65)
        ax.plot([0, 0], [-6, -ratio/2], color='#182e3c', linewidth=6, clip_on=False)
        ax.plot([0, 0], [ratio/2, 6], color='#182e3c', linewidth=6, clip_on=False)
        ax.set_title(f'b = {ratio:g}λ', fontsize=16, fontweight='bold', pad=12)
        ax.set(xlim=(0, 10), ylim=(-6, 6), xlabel='Distance beyond opening x/λ',
               xticks=np.arange(0, 11, 2), yticks=np.arange(-6, 7, 2))
        ax.set_aspect('equal')
        ax.spines[['top', 'right']].set_visible(False)
    axes[0].set_ylabel('Position across opening y/λ')
    fig.suptitle('Same wavelength: curved crests versus a nearly straight centre',
                 fontsize=16, fontweight='bold', y=.98)
    fig.text(.5, .92, 'Calculated scalar-wave snapshots · black curves mark crest phase', ha='center', fontsize=11)
    fig.text(.5, .065, 'Red = positive displacement; blue = negative. Colour scales are normalized separately.',
             ha='center', fontsize=10, color='#526875')
    fig.text(.5, .035, 'The wide opening also has curved edge waves. These are model fields, not tank measurements.',
             ha='center', fontsize=10, color='#526875')
    fig.tight_layout(rect=(0, .15, 1, .90))
    output = Path(__file__).resolve().parents[1] / 'assets/wave-motion-notes/diffraction-wavefront-shapes.svg'
    fig.savefig(output, dpi=180, metadata={'Date': None, 'Creator': 'Physics11 diffraction_figures.py'})
    output.write_text('\n'.join(line.rstrip() for line in output.read_text().splitlines()) + '\n')
    plt.close(fig)
    return output


if __name__ == '__main__':
    print(build_pattern())
    print(build_wavefronts())
