#!/usr/bin/env python3
"""Build apparent-depth rays, parallel-block rays, and the sine-index graph."""
from html import escape
from math import asin, atan, cos, radians, sin, tan
import os
from pathlib import Path
from tempfile import gettempdir

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/optics-notes'


def start(title, description, height=570):
    return [f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs><marker id="orange" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#b24c20"/></marker>
<marker id="teal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#086b72"/></marker>
<style>text{{font-family:Arial,Helvetica,sans-serif;font-size:20px;fill:#203440}}.title{{font-size:26px;font-weight:700;fill:#075d64}}.small{{font-size:17px}}.orange{{stroke:#b24c20;stroke-width:2.7;fill:none}}.teal{{stroke:#086b72;stroke-width:2.7;fill:none}}.guide{{stroke:#91a5ab;stroke-width:1.5;fill:none}}.normal{{stroke:#647a84;stroke-width:1.5;stroke-dasharray:7 5;fill:none}}.extension{{stroke:#8d315f;stroke-width:2;stroke-dasharray:7 5;fill:none}}</style></defs>
<rect width="960" height="{height}" fill="#fff"/><rect x="12" y="12" width="936" height="{height-24}" rx="12" fill="none" stroke="#cadbdd" stroke-width="2"/>
<text x="32" y="51" class="title">{escape(title)}</text>''']


def path(points, cls, arrow=False):
    d='M'+'L'.join(f'{x:.3f} {y:.3f}' for x,y in points)
    marker=f' marker-end="url(#{cls})"' if arrow else ''
    return f'<path d="{d}" class="{cls}"{marker}/>'


def directed(start_point, end_point, cls):
    a=tuple(start_point[i]+.38*(end_point[i]-start_point[i]) for i in (0,1))
    b=tuple(start_point[i]+.60*(end_point[i]-start_point[i]) for i in (0,1))
    return path([a,b],cls,True)


def build_apparent_depth():
    water_n, boundary, ox, oy = 1.33, 240., 350., 480.
    hits=(430.,460.)
    slopes=[tan(asin(water_n*sin(atan((x-ox)/(oy-boundary))))) for x in hits]
    depth=(hits[1]-hits[0])/(slopes[1]-slopes[0])
    vx,vy=hits[0]-slopes[0]*depth,boundary+depth
    svg=start('Why the underwater image looks shallower',
              'Two rays from a real underwater point refract away from the normal into air. '
              'Their dashed backward extensions meet at a shallower virtual image. '
              'The real object stays deeper. The displayed virtual position is for these two nearby rays.')
    svg += ['<text x="32" y="84" class="small">Trace solid light paths forward; trace the final directions backward to locate the image.</text>',
            '<rect x="14" y="240" width="932" height="290" fill="#eaf4f7"/>',
            '<path d="M14 240H946" stroke="#647a84" stroke-width="2"/>',
            '<text x="40" y="161">Air · n ≈ 1.00</text>',
            '<text x="40" y="282">Water · n = 1.33</text>',
            '<text x="746" y="229" class="small">Water surface</text>',
            '<path d="M430 146V325" class="normal"/>',
            '<text x="322" y="184" class="small">Normal</text>',
            '<text x="622" y="136">To observer</text>']
    for x,k in zip(hits,slopes):
        hit=(x,boundary);end=(x+k*(boundary-105),105)
        svg += [path([(ox,oy),hit],'orange'),directed((ox,oy),hit,'orange'),
                path([hit,end],'teal'),directed(hit,end,'teal'),
                path([hit,(vx,vy)],'extension')]
    svg += [f'<circle cx="{ox}" cy="{oy}" r="6" fill="#b24c20"/>',
            f'<circle cx="{vx:.3f}" cy="{vy:.3f}" r="7" stroke="#8d315f" stroke-width="2.5" stroke-dasharray="3 2" fill="#fff"/>',
            '<text x="40" y="365" fill="#8d315f">Apparent position</text>',
            '<text x="40" y="392" class="small">Virtual image · shallower</text>',
            path([(245,385),(vx-10,vy)],'guide'),
            '<text x="40" y="475">Actual object</text>',
            '<text x="40" y="502" class="small">Real position · deeper</text>',
            path([(220,480),(ox-12,oy)],'guide'),
            '<text x="548" y="385" class="small">Dashed: straight backward extensions</text>',
            '<text x="548" y="413" class="small">Light did not follow these lines in water.</text>',
            '<text x="32" y="550" class="small">Illustrative geometry calculated from Snell’s law. Apparent position depends on viewing direction.</text>',
            '</svg>']
    (ASSETS/'apparent-depth-rays.svg').write_text('\n'.join(svg)+'\n')


def build_parallel_block():
    incidence=radians(45.)
    inside=asin(sin(incidence)/1.5)
    top,bottom,entry_x=180.,340.,320.
    exit_x=entry_x+(bottom-top)*tan(inside)
    entry,exit=(entry_x,top),(exit_x,bottom)
    source=(entry_x-90,top-90);end=(exit_x+130,bottom+130)
    # The dashed reference has x-y = entry_x-top; shift is its perpendicular distance.
    p=(exit_x+80,bottom+80)
    half_gap=((entry_x-top)-(p[0]-p[1]))/2
    q=(p[0]+half_gap,p[1]-half_gap)
    svg=start('Parallel faces restore the direction, with a sideways shift',
              'A ray at 45 degrees in air bends to about 28.1 degrees in a glass slab of index 1.50. '
              'At its parallel second face it returns to 45 degrees in air. '
              'The emerging ray is parallel to a dashed straight continuation of the incoming ray, '
              'but displaced sideways. A short line marks the perpendicular gap.')
    svg += ['<rect x="14" y="180" width="932" height="160" fill="#eaf4f7"/>',
            '<path d="M14 180H946M14 340H946" stroke="#647a84" stroke-width="2"/>',
            '<text x="40" y="130">Air · n ≈ 1.00</text>',
            '<text x="40" y="267">Glass · n = 1.50</text>',
            '<text x="40" y="396">Air · n ≈ 1.00</text>',
            f'<path d="M{entry_x} 103V263M{exit_x} 272V459" class="normal"/>',
            '<text x="651" y="211">Faces and normals are parallel.</text>',
            '<text x="651" y="243" class="small">First bend: toward normal</text>',
            '<text x="651" y="275" class="small">Second bend: away from normal</text>',
            path([entry,(entry_x+290,top+290)],'normal'),
            path([source,entry],'orange'),directed(source,entry,'orange'),
            path([entry,exit],'teal'),directed(entry,exit,'teal'),
            path([exit,end],'orange'),directed(exit,end,'orange'),
            f'<path d="M{entry_x} {top-48}A48 48 0 0 0 {entry_x-48*sin(incidence)} {top-48*cos(incidence)}" class="orange"/>',
            f'<path d="M{entry_x} {top+48}A48 48 0 0 0 {entry_x+48*sin(inside)} {top+48*cos(inside)}" class="teal"/>',
            f'<path d="M{exit_x} {bottom+48}A48 48 0 0 0 {exit_x+48*sin(incidence)} {bottom+48*cos(incidence)}" class="orange"/>',
            path([p,q],'extension'),
            path([((p[0]+q[0])/2+8,(p[1]+q[1])/2),(603,401)],'guide'),
            '<text x="612" y="405">Sideways displacement</text>',
            '<text x="230" y="166">45.0°</text>',
            '<text x="419" y="244">28.1°</text>',
            f'<text x="{exit_x+40:.1f}" y="370">45.0°</text>',
            '<text x="610" y="486" class="small">Dashed grey: continuation without block</text>',
            '<text x="32" y="550" class="small">Illustrative angles from Snell’s law. Emerging and incoming directions are parallel.</text>',
            '</svg>']
    (ASSETS/'parallel-block-rays.svg').write_text('\n'.join(svg)+'\n')


def build_index_graph():
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/notes-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    style={'svg.fonttype':'none','svg.hashsalt':'physics11-index-slope','font.family':'DejaVu Sans',
           'font.size':13,'text.color':'#203440','axes.labelcolor':'#203440','axes.edgecolor':'#647a84'}
    with plt.rc_context(style):
        fig,ax=plt.subplots(figsize=(9.6,6.2))
        fig.subplots_adjust(left=.13,right=.96,bottom=.21,top=.80)
        fig.suptitle('Plot sine against sine: the slope gives the index ratio',x=.52,y=.96,
                     fontsize=16,fontweight='bold',color='#075d64')
        fig.text(.52,.89,'y = sin θ(air) · x = sin θ(material)',ha='center',fontsize=14)
        x=np.linspace(0,.65,201)
        ax.plot(x,1.5*x,color='#086b72',lw=3,label='Ideal line through the supplied point')
        ax.plot([0,.2],[0,0],color='#b24c20',lw=4)
        ax.plot([.2,.2],[0,.3],color='#b24c20',lw=2,linestyle=':')
        ax.plot([0,.2],[.3,.3],color='#91a5ab',lw=1.5,linestyle=':')
        ax.plot(.2,.3,'o',color='#b24c20',markersize=8)
        ax.annotate('(0.200, 0.300)',xy=(.2,.3),xytext=(.35,.32),fontsize=13,
                    bbox={'boxstyle':'round,pad=.35','fc':'white','ec':'#b24c20'},color='#b24c20',
                    arrowprops={'arrowstyle':'->','color':'#b24c20'})
        ax.text(.22,.12,'rise = 0.300',color='#b24c20',fontsize=11)
        ax.text(.1,.035,'run = 0.200',color='#b24c20',fontsize=11,ha='center')
        ax.set(xlim=(0,.65),ylim=(0,1),xticks=np.arange(0,.61,.1),yticks=np.arange(0,1.01,.2),
               xlabel='sin θ(material) — no units',ylabel='sin θ(air) — no units')
        ax.grid(alpha=.2);ax.legend(loc='upper left',fontsize=11,frameon=False)
        fig.text(.13,.075,'Slope = rise/run = n(material)/n(air). Use the sine values, not the angles.',fontsize=12)
        fig.text(.13,.025,'The line illustrates the supplied point and Snell’s law; it is not a measured data set.',fontsize=11,color='#526875')
        fig.savefig(ASSETS/'refractive-index-graph.svg',format='svg',metadata={'Date':None})
        fig.savefig(Path(gettempdir())/'physics11-refractive-index-graph.png',dpi=140)
        plt.close(fig)


def build_depth_figures():
    ASSETS.mkdir(exist_ok=True)
    build_apparent_depth();build_parallel_block();build_index_graph()
    print('Built apparent-depth rays, parallel-block rays, and refractive-index graph.')


if __name__=='__main__':
    build_depth_figures()
