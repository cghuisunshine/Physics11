#!/usr/bin/env python3
"""Illustrate Grade 11 Snell refraction and plot the air-to-glass angle mapping."""
from html import escape
from math import asin, cos, degrees, radians, sin
import os
from pathlib import Path
from tempfile import gettempdir

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/optics-notes'


def build_direction_figure():
    a = radians(35)
    b = asin(sin(a)/1.5)
    svg = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="570" viewBox="0 0 1000 570" role="img" aria-labelledby="title desc">
<title id="title">Refraction toward and away from the normal</title>
<desc id="desc">Two reversed light paths at a horizontal air-glass boundary. Air to glass: incident angle 35.0 degrees becomes 22.5 degrees, toward the normal. Glass to air: incident angle 22.5 degrees becomes 35.0 degrees, away from the normal. All angles are measured from a dashed perpendicular normal, not the surface.</desc>
<defs><marker id="incoming" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#b24c20"/></marker>
<marker id="outgoing" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#086b72"/></marker>
<style>text{font-family:Arial,Helvetica,sans-serif;font-size:19px;fill:#203440}.title{font-size:25px;font-weight:700;fill:#075d64}.small{font-size:17px}.medium{font-weight:700}.in{stroke:#b24c20;stroke-width:3;fill:none}.out{stroke:#086b72;stroke-width:3;fill:none}.normal{stroke:#647a84;stroke-width:1.5;stroke-dasharray:7 5;fill:none}</style></defs>
<rect width="1000" height="570" fill="#fff"/>
<text x="24" y="38" class="title">The same Snell’s law, in either direction</text>''']
    for index, (title, n1, n2, t1, t2) in enumerate((
        ('Air → glass', 1., 1.5, a, b), ('Glass → air', 1.5, 1., b, a),
    )):
        left, top = 14+index*494, 64
        x, y = left+230, 275
        upper = '#fafcfb' if n1==1 else '#eaf4f7'
        lower = '#fafcfb' if n2==1 else '#eaf4f7'
        med1, med2 = ('Air','Glass') if n1==1 else ('Glass','Air')
        svg += [f'<rect x="{left}" y="{top}" width="480" height="472" rx="12" fill="#fff" stroke="#cadbdd" stroke-width="2"/>',
                f'<text x="{left+18}" y="{top+34}" class="title">{escape(title)}</text>',
                f'<rect x="{left+2}" y="110" width="476" height="165" fill="{upper}"/>',
                f'<rect x="{left+2}" y="275" width="476" height="210" fill="{lower}"/>',
                f'<path d="M{left+2} {y}H{left+478}" stroke="#647a84" stroke-width="2"/>',
                f'<text x="{left+18}" y="{y-11}" class="small">Boundary</text>',
                f'<path d="M{x} 113V475" class="normal"/>',
                f'<text x="{x+13}" y="136" class="small">Normal</text>',
                f'<text x="{left+17}" y="175" class="medium">{med1} · n₁ = {n1:.2f}</text>',
                f'<text x="{left+17}" y="330" class="medium">{med2} · n₂ = {n2:.2f}</text>']
        source = (x-175*sin(t1),y-175*cos(t1))
        end = (x+175*sin(t2),y+175*cos(t2))
        svg += [f'<path d="M{source[0]:.3f} {source[1]:.3f}L{x} {y}" class="in"/>',
                f'<path d="M{x} {y}L{end[0]:.3f} {end[1]:.3f}" class="out"/>']
        for cls, p, q in (('in',source,(x,y)),('out',(x,y),end)):
            u=tuple(p[i]+.38*(q[i]-p[i]) for i in (0,1))
            v=tuple(p[i]+.60*(q[i]-p[i]) for i in (0,1))
            marker='incoming' if cls=='in' else 'outgoing'
            svg.append(f'<path d="M{u[0]:.3f} {u[1]:.3f}L{v[0]:.3f} {v[1]:.3f}" class="{cls}" marker-end="url(#{marker})"/>')
        r=65
        svg += [f'<path d="M{x} {y-r}A{r} {r} 0 0 0 {x-r*sin(t1):.3f} {y-r*cos(t1):.3f}" class="in"/>',
                f'<path d="M{x} {y+r}A{r} {r} 0 0 0 {x+r*sin(t2):.3f} {y+r*cos(t2):.3f}" class="out"/>',
                f'<text x="{x-164}" y="{y-38}">θ₁ = {degrees(t1):.1f}°</text>',
                f'<text x="{x+100}" y="{y+100}">θ₂ = {degrees(t2):.1f}°</text>',
                f'<text x="{left+18}" y="514" class="medium">'+('Higher n → slower → toward normal' if n2>n1 else 'Lower n → faster → away from normal')+'</text>']
    svg += ['<text x="24" y="559" class="small">Frequency stays the same across the stationary boundary. Partial reflection is omitted.</text>','</svg>']
    ASSETS.mkdir(exist_ok=True)
    (ASSETS/'refraction-directions.svg').write_text('\n'.join(svg)+'\n')


def build_angle_graph():
    os.environ.setdefault('MPLCONFIGDIR',str(ROOT/'tmp/notes-matplotlib'))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    style={'svg.fonttype':'none','svg.hashsalt':'physics11-snell-angle',
           'font.family':'DejaVu Sans','font.size':13,'text.color':'#203440',
           'axes.labelcolor':'#203440','axes.edgecolor':'#647a84'}
    with plt.rc_context(style):
        fig,ax=plt.subplots(figsize=(9.6,6.2))
        fig.subplots_adjust(left=.13,right=.96,bottom=.20,top=.80)
        fig.suptitle('Air → glass: the refracted angle is smaller',x=.52,y=.96,
                     fontsize=17,fontweight='bold',color='#075d64')
        fig.text(.52,.89,'n₁ = 1.00, n₂ = 1.50 · n₁ sin θ₁ = n₂ sin θ₂',ha='center',fontsize=14)
        angles=np.linspace(0,80,401)
        refracted=np.degrees(np.arcsin(np.sin(np.radians(angles))/1.5))
        ax.plot(angles,angles,'--',color='#87979d',lw=1.8,label='Equal angles: θ₂ = θ₁')
        ax.plot(angles,refracted,color='#086b72',lw=3,label='Snell’s law: air → glass')
        ax.set(xlim=(0,80),ylim=(0,80),xticks=np.arange(0,81,10),yticks=np.arange(0,81,10),
               xlabel='Incident angle θ₁ (degrees from the normal)',
               ylabel='Refracted angle θ₂ (degrees from the normal)')
        ax.grid(alpha=.2)
        b=degrees(asin(sin(radians(35))/1.5))
        ax.plot([35,35],[0,b],':',color='#b24c20',lw=1.5)
        ax.plot([0,35],[b,b],':',color='#b24c20',lw=1.5)
        ax.plot(35,b,'o',color='#b24c20',markersize=8)
        ax.annotate('35.0° → 22.5°',xy=(35,b),xytext=(47,13),fontsize=13,
                    color='#b24c20',bbox={'boxstyle':'round,pad=.35','fc':'white','ec':'#b24c20'},
                    arrowprops={'arrowstyle':'->','color':'#b24c20'})
        ax.legend(loc='upper left',fontsize=12,frameon=False)
        fig.text(.13,.075,'The curve is below the equal-angle line: light bends toward the normal.',fontsize=12)
        fig.text(.13,.025,'Model graph of angles, not the ray path. Both axes are measured from the normal.',fontsize=11,color='#526875')
        fig.savefig(ASSETS/'snell-angle-graph.svg',format='svg',metadata={'Date':None})
        fig.savefig(Path(gettempdir())/'physics11-snell-angle-graph.png',dpi=140)
        plt.close(fig)


def build_refraction_figures():
    build_direction_figure()
    build_angle_graph()
    print('Built refraction direction diagrams and Snell angle graph.')


if __name__=='__main__':
    build_refraction_figures()
