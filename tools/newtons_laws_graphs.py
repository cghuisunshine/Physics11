"""Generate illustrative SI graphs for the Newton's second-law investigation."""
from pathlib import Path
import base64
import html
import os

ROOT = Path(__file__).resolve().parents[1]


def build_graphs():
    os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/newtons-notes-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'svg.fonttype': 'none', 'svg.hashsalt': 'newtons-notes',
                         'font.size': 12, 'text.color': '#182e3c', 'axes.labelcolor': '#182e3c'})
    assets = ROOT / 'assets/newtons-laws-notes'
    previews = ROOT / 'tmp/newtons-notes'
    assets.mkdir(parents=True, exist_ok=True)
    previews.mkdir(parents=True, exist_ok=True)
    force = np.linspace(0, 8, 100)
    mass = np.linspace(1, 4, 100)
    reciprocal = np.linspace(0, 1, 100)
    specifications = [
        ('acceleration-force', force, force / 1.00,
         'Fixed mass: m = 1.00 kg', 'Net force (N)', 'Acceleration (m/s²)',
         'Acceleration versus net force for fixed mass 1.00 kg: a straight line from 0 N and 0 m/s² to 8 N and 8 m/s².',
         'Illustrative ideal values: the slope is 1/m = 1.00 kg⁻¹. Doubling net force doubles acceleration.'),
        ('acceleration-mass', mass, 2.00 / mass,
         'Fixed net force: F = 2.00 N', 'Total moving mass (kg)', 'Acceleration (m/s²)',
         'Acceleration versus mass at fixed net force 2.00 N: a decreasing curve, with 2.00 m/s² at 1.00 kg and 0.500 m/s² at 4.00 kg.',
         'Illustrative ideal values: a = 2.00 N / m. Doubling mass halves acceleration; the graph is a curve.'),
        ('acceleration-reciprocal-mass', reciprocal, 2.00 * reciprocal,
         'Fixed net force: F = 2.00 N', 'Reciprocal mass, 1/m (kg⁻¹)', 'Acceleration (m/s²)',
         'Acceleration versus reciprocal mass for fixed net force 2.00 N: a straight line through the origin with slope 2.00 N.',
         'Illustrative ideal values: a = (2.00 N)(1/m). The slope is the net force, 2.00 N. The origin is a limiting extrapolation as mass increases without bound.'),
    ]
    figures = []
    for name, x, y, title, xlabel, ylabel, alt, caption in specifications:
        fig, ax = plt.subplots(figsize=(8, 3.6), constrained_layout=True)
        ax.plot(x, y, color='#086b72', linewidth=2.5)
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
        ax.set_xlim(x.min(), x.max())
        ax.set_ylim(0, y.max() * 1.08)
        ax.grid(True, color='#dce4e7')
        ax.spines[['top', 'right']].set_visible(False)
        fig.savefig(assets / f'{name}.svg', metadata={'Date': None})
        svg_path = assets / f'{name}.svg'
        svg_path.write_text('\n'.join(line.rstrip() for line in svg_path.read_text().splitlines()) + '\n')
        fig.savefig(previews / f'{name}.png', dpi=130)
        plt.close(fig)
        data = base64.b64encode((assets / f'{name}.svg').read_bytes()).decode()
        figures.append(f'<figure class="diagram law-graph"><img src="data:image/svg+xml;base64,{data}" '
                       f'alt="{html.escape(alt, quote=True)}" loading="lazy">'
                       f'<figcaption>{html.escape(caption)}</figcaption></figure>')
    return ''.join(figures)
