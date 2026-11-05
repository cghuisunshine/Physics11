"""Collapsed worked answers and embedded, reproducible solution figures."""
from pathlib import Path
from html import escape
import io
import math
import os
import re

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'tmp/notes-matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

TEAL, BLUE, RED = '#086b72', '#2464ad', '#bc493e'
plt.rcParams.update({'font.size': 10, 'svg.fonttype': 'none', 'axes.spines.top': False,
                     'axes.spines.right': False, 'axes.labelcolor': '#19333d',
                     'text.color': '#19333d', 'axes.edgecolor': '#82949a'})


def axes(title, xlabel, ylabel, equal=False):
    fig, ax = plt.subplots(figsize=(6.4, 3.9), layout='constrained')
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(alpha=.2)
    ax.set_axisbelow(True)
    if equal:
        ax.set_aspect('equal', adjustable='box')
        ax.axhline(0, color='#82949a', lw=.8)
        ax.axvline(0, color='#82949a', lw=.8)
    return fig, ax


def arrow(ax, start, end, color, label='', offset=(5, 8)):
    ax.annotate('', xy=end, xytext=start,
                arrowprops={'arrowstyle': '-|>', 'color': color, 'lw': 2, 'mutation_scale': 15})
    if label:
        ax.annotate(label, xy=((start[0]+end[0])/2, (start[1]+end[1])/2),
                    xytext=offset, textcoords='offset points', color=color, fontsize=9,
                    bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': .85, 'pad': 1.5})


def curve(ax, t, y, color=TEAL, label=None):
    ax.plot(t, y, color=color, lw=2.5, label=label)
    ax.plot([t[0], t[-1]], [y[0], y[-1]], 'o', color=color, ms=4)


def save_figure(fig, key, description):
    """Keep standalone export files and also embed the exact SVG in the HTML."""
    out = ROOT / 'output/notes-answer-graphs'
    out.mkdir(parents=True, exist_ok=True)
    matplotlib.rcParams['svg.hashsalt'] = key
    stream = io.StringIO()
    fig.savefig(stream, format='svg', metadata={'Date': None})
    svg = stream.getvalue()
    svg = svg[svg.index('<svg'):]
    # Matplotlib repeats group IDs such as figure_1 across separate SVGs.
    # Prefix every ID and local reference so embedded figures stay independent.
    for ident in re.findall(r'\bid="([^"]+)"',svg):
        unique=key+'-'+ident
        svg=svg.replace('id="'+ident+'"','id="'+unique+'"')
        svg=svg.replace('href="#'+ident+'"','href="#'+unique+'"')
        svg=svg.replace('url(#'+ident+')','url(#'+unique+')')
    svg = svg.replace('<svg ', '<svg role="img" aria-label="'+escape(description, quote=True)+'" ', 1)
    svg = re.sub(r'(<svg\b[^>]*>)', lambda m: m[1]+'<title>'+escape(description)+'</title>', svg, count=1)
    svg = '\n'.join(line.rstrip() for line in svg.splitlines())+'\n'
    (out / f'{key}.svg').write_text(svg)
    fig.savefig(out / f'{key}.png', dpi=130)
    plt.close(fig)
    return '<figure class="solution-figure">'+svg+'<figcaption>'+escape(description)+'</figcaption></figure>'


def figure(subject, topic, number):
    key = f'{subject}-{topic}-{number}'
    if subject == 'vectors':
        fig, ax = axes('Vector components and resultant', 'East component', 'North component', True)
        if topic == 2 and number == 0:
            x, y = 350*math.cos(math.pi/6), 175
            ax.set(title='Vancouver to Kamloops', xlabel='East (km)', ylabel='North (km)', xlim=(-30,370), ylim=(-30,240))
            arrow(ax,(0,0),(x,0),TEAL,'303 km east',(0,-18))
            arrow(ax,(x,0),(x,y),BLUE,'175 km north',(7,0))
            arrow(ax,(0,0),(x,y),RED,'350 km, 30° north of east',(-45,12))
            caption = 'The east and north components form a right triangle with the 350 km displacement.'
        elif topic == 2:
            x, y = -56*math.sin(math.radians(25)), -56*math.cos(math.radians(25))
            ax.set(title='56 m/s, 25° west of south', xlabel='East component (m/s)', ylabel='North component (m/s)', xlim=(-43,12), ylim=(-64,10))
            arrow(ax,(0,0),(x,0),TEAL,'23.7 m/s west',(-36,8))
            arrow(ax,(x,0),(x,y),BLUE)
            ax.text(-28,-25,'50.8 m/s south',rotation=90,ha='center',va='center',
                    color=BLUE,fontsize=9,bbox={'facecolor':'white','edgecolor':'none','alpha':.85,'pad':1.5})
            arrow(ax,(0,0),(x,y),RED,'56 m/s',(6,-8))
            angle = np.linspace(math.radians(245),math.radians(270),30)
            ax.plot(13*np.cos(angle),13*np.sin(angle),color='#526875',lw=1)
            ax.text(-7,-16,'25°',fontsize=9)
            caption = 'East and north are positive. Both components are negative for a vector west of south.'
        elif topic in (3,4):
            x, y = 2.5+3*math.cos(math.radians(35)),3*math.sin(math.radians(35))
            ax.set(title="Aaron's total displacement", xlabel='East (km)', ylabel='North (km)', xlim=(-.5,6.2), ylim=(-.6,2.6))
            arrow(ax,(0,0),(2.5,0),TEAL,'2.5 km east',(0,-18))
            arrow(ax,(2.5,0),(x,y),BLUE,'3.0 km at 35°',(5,-14))
            arrow(ax,(0,0),(x,y),RED,'5.2 km at 19°',(-25,14))
            ax.plot([x,x,0],[0,y,y],':',color='#82949a')
            caption = 'Head-to-tail addition and component addition give the same displacement: 5.2 km, 19° north of east.'
        elif topic == 5:
            x, y = 10/math.sqrt(2),10/math.sqrt(2)
            ax.set(title="The dog's change in position", xlabel='East (m)', ylabel='North (m)', xlim=(-1,10), ylim=(-1,9))
            arrow(ax,(0,0),(5,0),TEAL)
            arrow(ax,(0,0),(x,y),BLUE)
            arrow(ax,(5,0),(x,y),RED)
            ax.scatter([0,5,x],[0,0,y],color=['#19333d',TEAL,BLUE],s=20)
            ax.annotate('Observer',(0,0),xytext=(5,-18),textcoords='offset points',fontsize=9)
            ax.annotate('Initial: 5.0 m east',(5,0),xytext=(-35,-18),textcoords='offset points',fontsize=9)
            ax.annotate('Final position',(x,y),xytext=(-15,8),textcoords='offset points',fontsize=9)
            ax.legend([Line2D([],[],color=c,lw=2) for c in (TEAL,BLUE,RED)],['Initial position','Final position','Displacement: final − initial'],loc='upper left',fontsize=8)
            caption = 'The red arrow joins the initial and final positions: 7.4 m, 16° east of north.'
        elif topic == 7:
            ax.set(title='Boat aimed south: velocity relative to shore', xlabel='East component (km/h)', ylabel='North component (km/h)', xlim=(-11,6), ylim=(-13,3))
            arrow(ax,(0,0),(0,-10),BLUE,'Boat: 10.0 south',(8,0))
            arrow(ax,(0,-10),(-4,-10),TEAL,'Current: 4.0 west',(-44,-18))
            arrow(ax,(0,0),(-4,-10),RED,'Resultant: 10.8',(-106,5))
            caption = 'For the southward heading, add the current head-to-tail. The shore velocity is 10.8 km/h, 22° west of south.'
        else:
            raise ValueError(key)
    elif topic == 1:
        fig, ax = axes('Route and displacement around the block','Rightward position (m)','Upward position (m)',True)
        ax.set(xlim=(-15,125),ylim=(-15,125))
        arrow(ax,(0,0),(0,100),BLUE)
        arrow(ax,(0,100),(100,100),BLUE,'Route: 100 m + 100 m',(-70,9))
        arrow(ax,(0,0),(100,100),RED,'Displacement: 141 m',(-20,12))
        ax.plot([0,100,100,0,0],[0,0,100,100,0],':',color='#82949a')
        ax.annotate('Start',(0,0),xytext=(5,-15),textcoords='offset points',fontsize=9)
        ax.annotate('Finish',(100,100),xytext=(0,-20),textcoords='offset points',fontsize=9)
        caption = 'The route follows two sides (200 m). The red displacement is the diagonal, directed 45° up and right.'
    elif topic == 2:
        if number == 1:
            fig, ax = axes('Sunlight travelling to Earth','Time (s)','Distance travelled (million km)')
            curve(ax,[0,510],[0,153])
            ax.set(xticks=[0,120,240,360,510],xlim=(0,550),ylim=(0,175))
            ax.annotate('Earth: 153 million km',(510,153),xytext=(-150,10),textcoords='offset points',fontsize=9)
            caption = 'At constant light speed, distance increases linearly. After 510 s, light has travelled 1.53 × 10¹¹ m.'
        else:
            fig, ax = axes('Four laps: distance and displacement','Elapsed time (s)','Cumulative distance (m)')
            ax.plot([0,390],[0,1600],'--',color=TEAL,lw=2,label='Line representing average speed')
            ax.scatter([0,390],[0,1600],color=TEAL,s=30)
            ax.set(xlim=(0,430),ylim=(0,1850))
            ax.text(20,1650,'Four laps: 1600 m travelled\nFinish = start: displacement 0 m',fontsize=10)
            caption = 'The dashed slope is the average speed, 4.1 m/s. Instantaneous speed is unspecified; only the start and end data are given.'
    elif topic == 4:
        if number == 1:
            a=1.1; end=math.sqrt(200/a); t=np.linspace(0,end,100)
            fig, ax=axes('Sprinter accelerating through 100 m','Time (s)','Velocity along the track (m/s)')
            curve(ax,t,a*t)
            ax.fill_between(t,0,a*t,color=TEAL,alpha=.12)
            ax.text(end*.45,3,'Area = 100 m',color=TEAL)
            caption='The velocity-time slope is 1.1 m/s². The triangular area is 100 m; final velocity is approximately 15 m/s.'
        elif number == 2:
            t=np.linspace(0,7,100)
            fig, ax=axes('Rammus accelerating from rest','Time (s)','Distance travelled (m)')
            curve(ax,t,.5*1.4*t*t)
            caption='Constant acceleration produces a curved distance-time graph: d = ½at². At 7.0 s, distance is 34.3 m.'
        else:
            fig, ax=axes('Police car increasing speed','Time (s)','Velocity along the road (m/s)')
            curve(ax,[0,2.5],[50/3.6,90/3.6])
            ax.set(ylim=(0,29))
            caption='The speed change is 11.11 m/s over 2.5 s. The straight-line slope is 4.44 m/s² under a uniform-acceleration model.'
    elif topic == 5:
        if number == 1:
            t=np.linspace(0,2,100)
            fig, ax=axes('Hammer dropped from rest','Time (s)','Downward distance (m)')
            curve(ax,t,.5*9.8*t*t)
            caption='With downward distance positive, d = ½gt². The hammer falls 19.6 m in 2.0 s.'
        elif number == 2:
            t=np.linspace(0,700/9.8,150)
            fig, ax=axes('Bullet rising in the ideal free-fall model','Time after launch (s)','Height above launch (km)')
            curve(ax,t,(700*t-.5*9.8*t*t)/1000)
            ax.annotate('Peak: 25 km',(t[-1],25),xytext=(-100,-25),textcoords='offset points',fontsize=10)
            caption='The curve flattens at the peak, where vertical velocity is zero. This model neglects air resistance and treats gravity as constant.'
        else:
            end=30/9.8;t=np.linspace(0,end,150)
            fig, ax=axes('Ball thrown upward and returning to the hand','Time (s)','Height above the hand (m)')
            curve(ax,t,15*t-.5*9.8*t*t)
            ax.axvline(end/2,color='#82949a',ls=':',lw=1)
            ax.set(xticks=[0,end/2,end],xticklabels=['0','1.53','3.06'])
            caption='The ball rises and falls for equal times, returning to the launch height after 3.06 s.'
    elif topic == 6:
        fig, ax=axes('Piecewise position-time motion','Time (s)','Position (m)')
        curve(ax,[0,2,4,8],[0,20,20,5])
        ax.set(xlim=(0,8.5),ylim=(0,25))
        for x,y,label in [(0.7,11,'+10 m/s'),(2.3,21.5,'0 m/s'),(5,15,'≈ −3.75 m/s')]:
            ax.text(x,y,label,fontsize=9,bbox={'facecolor':'white','edgecolor':'none','alpha':.9,'pad':1})
        caption='Each segment slope gives velocity: +10 m/s, 0 m/s, and approximately −3.75 m/s.'
    elif topic == 7:
        fig, ax=axes('Instantaneous and average velocity','Time (s)','Position (m)')
        t=np.linspace(0,8,200)
        ax.plot(t,22.5*(1-3**(-t/4)),color=BLUE,lw=2.5,label='Approximation to the source curve')
        ax.plot([2,6],[11,19],color=RED,lw=2,label='Tangent at 4 s: approximately 2 m/s')
        ax.plot([0,8],[0,20],'--',color=TEAL,label='Secant: average 2.5 m/s')
        ax.scatter([0,4,8],[0,15,20],color=BLUE,s=22)
        ax.legend(loc='lower right',fontsize=8)
        caption='Illustrative smooth curve following the handwritten graph. The tangent and endpoint readings are approximate, not an exact function supplied by the question.'
    elif topic == 8:
        fig, ax=axes('Signed areas on the velocity-time graph','Time (s)','Velocity (m/s)')
        t=np.linspace(0,14,281);v=np.interp(t,[0,8,12,14],[10,-10,-10,0])
        curve(ax,t,v,color=BLUE)
        ax.fill_between(t,0,v,where=v>=0,color=TEAL,alpha=.25,interpolate=True)
        ax.fill_between(t,0,v,where=v<=0,color=RED,alpha=.18,interpolate=True)
        ax.axhline(0,color='#526875',lw=1)
        ax.set(xticks=[0,4,8,12,14],ylim=(-14,13))
        for x,y,label in [(1,2,'+20 m'),(5,-3,'−20 m'),(9,-5,'−40 m'),(12,-2,'−10 m')]:ax.text(x,y,label,fontsize=9)
        caption='Signed area gives −50 m displacement. Adding all area magnitudes gives 90 m distance; the initial slope is −2.5 m/s².'
    elif topic in (10,11):
        cliff=topic==10
        vx=20 if cliff else 6
        vy=0 if cliff else 12*math.sin(math.pi/3)
        height=100 if cliff else 0
        end=math.sqrt(200/9.8) if cliff else 2*vy/9.8
        t=np.linspace(0,end,150);x=vx*t;y=height+vy*t-.5*9.8*t*t
        fig, ax=axes('Horizontal launch from a cliff' if cliff else 'Ball launched at 60°','Horizontal distance (m)','Height above the ground (m)',True)
        curve(ax,x,y,color=TEAL)
        ax.axhline(0,color='#82949a',lw=1)
        scale=.35 if cliff else .2
        arrow(ax,(0,height),(scale*vx,height+scale*vy),BLUE)
        arrow(ax,(x[-1],0),(x[-1]+scale*vx,scale*(vy-9.8*end)),RED)
        if cliff:
            ax.plot([0,0],[0,100],color='#82949a',lw=3)
            ax.set(xlim=(-10,115),ylim=(-22,125))
            ax.text(12,109,'Launch: 20 m/s right',fontsize=9,color=BLUE)
            ax.text(25,-17,'Impact: 49 m/s\n66° below horizontal',fontsize=9,color=RED)
            caption='The path curves downward while horizontal velocity stays constant. Arrows show launch and impact velocity; flight time is 4.52 s and range is 90.35 m.'
        else:
            ax.set(xlim=(-1,16),ylim=(-3,8))
            ax.text(.2,6.8,'Launch: 12 m/s at 60°',fontsize=9,color=BLUE)
            ax.text(5.3,-2.6,'Impact: 12 m/s at −60°',fontsize=9,color=RED)
            caption='Flight time is 2.12 s and range is 12.73 m. Velocity arrows show equal launch and impact speeds with opposite vertical components.'
    else:
        raise ValueError(key)
    return save_figure(fig,key,caption)


def disclosure(solution, visual, ident):
    return ('<details class="answer-disclosure" id="'+ident+'"><summary>'
            '<span class="show-answer-label">Show answer</span>'
            '<span class="hide-answer-label">Hide answer</span></summary>'
            '<div class="answer-body"><h4>Worked answer</h4>'+solution+visual+'</div></details>')


def decorate_answers(body, subject, topic):
    count=0
    def wrap(match):
        nonlocal count
        count+=1
        return disclosure(match[1],figure(subject,topic,count),f'answer-{subject}-{topic}-{count}')
    body=re.sub(r'<p><strong>Worked answer</strong></p>\s*(.*?)(?=\s*<h3>|\Z)',wrap,body,flags=re.S)
    expected={'vectors':{2:1,3:1,4:1,5:1,7:1},
              'kinematics':{1:1,2:2,4:3,5:3,6:1,7:1,8:1}}
    assert count==expected[subject].get(topic,0), f'Missing answer boundary in {subject} topic {topic}'
    if subject=='vectors' and topic==2:
        body,n=re.subn(r'(<h3>Worked example: Vancouver to Kamloops</h3>\s*<p>.*?</p>)\s*(.*?)(?=\s*<h3>|\Z)',
                      lambda m:m[1]+disclosure(m[2],figure(subject,topic,0),'answer-vectors-2-example'),body,count=1,flags=re.S)
        assert n==1
    if subject=='kinematics' and topic in (10,11):
        marker='<h3>Direction convention and givens</h3>' if topic==10 else '<h3>Worked answer: components</h3>'
        prefix,found,solution=body.partition(marker)
        assert found
        body=prefix+disclosure(marker+solution,figure(subject,topic,0),f'answer-kinematics-{topic}-0')
    return body
