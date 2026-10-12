"""Reproducible illustrations of an ideal spring's deformation and force."""
from pathlib import Path
import base64
import html
import io
import os

ROOT = Path(__file__).resolve().parents[1]

def build_spring_graphs():
    os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/forces-notes-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'svg.fonttype': 'none', 'font.size': 11, 'text.color': '#182e3c',
        'axes.labelcolor': '#182e3c', 'axes.edgecolor': '#526875'})
    outputs = ROOT / 'assets/forces-notes'
    previews = ROOT / 'tmp/forces-spring-graphs'
    outputs.mkdir(parents=True, exist_ok=True)
    previews.mkdir(parents=True, exist_ok=True)

    def save(fig, name, alt, caption):
        plt.rcParams['svg.hashsalt'] = name
        stream = io.BytesIO()
        fig.savefig(stream, format='svg', metadata={'Date': None})
        data = stream.getvalue()
        (outputs / (name + '.svg')).write_bytes(data)
        fig.savefig(previews / (name + '.png'), dpi=150)
        plt.close(fig)
        return '<figure class="diagram spring-visual"><img src="data:image/svg+xml;base64,' + base64.b64encode(data).decode() + '" alt="' + html.escape(alt, quote=True) + '" loading="lazy"><figcaption>' + caption + '</figcaption></figure>'

    fig, ax = plt.subplots(figsize=(7.4, 4.1), layout='constrained')
    ax.set(xlim=(-.7, 18), ylim=(-.85, 2.7))
    ax.axis('off')
    ax.set_title('One ideal spring: relaxed, extended, and compressed', pad=15)
    ax.axvline(10, ymin=.12, ymax=.84, color='#859b9c', linestyle='--', linewidth=1)
    ax.text(10, 2.48, 'Relaxed end position', ha='center', fontsize=10, color='#526875')
    for row, end, label, color in [(2, 10, 'Relaxed: L = 10 cm\nx = 0', '#526875'),
                                  (1, 14, 'Extended: L = 14 cm\nx = +4 cm', '#086b72'),
                                  (0, 6, 'Compressed: L = 6 cm\nx = −4 cm', '#bc493e')]:
        ax.plot([0, 0], [row-.25, row+.25], color='#526875', lw=4)
        t = np.linspace(0, 1, 401)
        ax.plot(.4+(end-.8)*t, row+.12*np.sin(2*np.pi*10*t), color=color, lw=2)
        ax.plot([0, .4], [row, row], color=color, lw=2)
        ax.plot([end-.4, end], [row, row], color=color, lw=2)
        ax.plot(end, row, 'o', color=color, markersize=5)
        ax.text(15.2, row, label, va='center', fontsize=10, color=color)
        if end != 10:
            ax.annotate('', (end, row-.3), (10, row-.3), arrowprops={'arrowstyle':'->','color':color,'lw':1.5})
            ax.text((end+10)/2, row-.48, 'x = +4 cm' if end>10 else 'x = −4 cm', ha='center', fontsize=10, color=color)
    ax.text(0, -.76, 'Fixed end', fontsize=10, ha='center', color='#526875')
    ax.text(10, -.76, 'x = L − L₀; positive x is to the right', fontsize=10, ha='center')
    states = save(fig, 'spring-extension-compression',
        'Three drawings of the same spring: relaxed length 10 cm, stretched length 14 cm with x plus 4 cm, and compressed length 6 cm with x minus 4 cm. A dashed line marks the relaxed end position.',
        'Illustrative spring states. Extension and compression are measured from the relaxed length L₀, not from the fixed end. The same number of coils is shown in each state.')

    fig, ax = plt.subplots(figsize=(7.4, 4.6), layout='constrained')
    x_cm = np.linspace(-4, 4, 161)
    applied = 100*(x_cm/100)
    ax.axvspan(-4, 0, color='#f9eeee', alpha=.75)
    ax.axvspan(0, 4, color='#edf6f4', alpha=.75)
    ax.axhline(0, color='#526875', lw=1)
    ax.axvline(0, color='#526875', lw=1)
    ax.plot(x_cm, applied, color='#086b72', lw=2.5, label='External holding force (+kx)')
    ax.plot(x_cm, -applied, color='#bc493e', lw=2.5, linestyle='--', label='Spring restoring force (−kx)')
    ax.set(xlim=(-4, 4), ylim=(-4.7, 4.7), xticks=np.arange(-4, 5), yticks=np.arange(-4, 5, 2),
        xlabel='Signed deformation x (cm):  negative = compression; positive = extension',
        ylabel='Signed force on the free end (N)')
    fig.suptitle('Force and deformation: example k = 100 N/m', fontsize=13)
    ax.text(-2, 4.35, 'Compression', ha='center', fontsize=10, color='#bc493e')
    ax.text(2, 4.35, 'Extension', ha='center', fontsize=10, color='#086b72')
    ax.grid(alpha=.18)
    ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.02), fontsize=9, frameon=False)
    forces = save(fig, 'spring-force-deformation',
        'Signed spring force graph for k equal to 100 N per metre. The holding force increases from minus 4 N at minus 4 cm compression to plus 4 N at plus 4 cm extension. The restoring force has the opposite sign and slope.',
        'Illustrative ideal-spring graph, not measured textbook data. For k = 100 N/m (1 N/cm), the holding-force slope is +k and the restoring-force slope is −k. At rest these forces balance. Use metres when substituting into F = kx.')
    return {'Seeing extension and compression': states, 'Signed force graph: extension and compression': forces}
