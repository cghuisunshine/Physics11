from pathlib import Path
import re, json
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import ArrayObject, NameObject, TextStringObject
from pypdf.generic import Fit

source = Path('output/pdf/bc_science_physics_11_bookmarked.pdf')
output = Path('output/pdf/bc_science_physics_11_interactive.pdf')
entries = json.loads(Path('tmp/pdfs/bookmarks_verified.json').read_text())[1:]
s = Path('/private/tmp/physics11-toc-bbox.html').read_text()
lines = []
for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', s, re.S):
    x0, y0, x1, y1 = map(float, m.groups()[:4])
    if 110 < y0 < 680:
        lines.append((x0, y0, x1, y1))
rows = []
for line in sorted(lines, key=lambda r: r[1]):
    if not rows or abs(line[1] - rows[-1][1]) >= 2:
        rows.append(list(line))
    else:
        row = rows[-1]
        row[0], row[1], row[2], row[3] = min(row[0],line[0]), min(row[1],line[1]), max(row[2],line[2]), max(row[3],line[3])
assert len(rows) == len(entries) == 41
reader = PdfReader(source)
writer = PdfWriter()
writer.clone_document_from_reader(reader)
page_height = float(writer.pages[3].mediabox.height)
centers = [(r[1] + r[3])/2 for r in rows]
for i, ((title, page_index, depth), row) in enumerate(zip(entries, rows)):
    top = (centers[i-1]+centers[i])/2 if i else row[1]-2
    bottom = (centers[i]+centers[i+1])/2 if i+1<len(rows) else row[3]+2
    assert top <= row[1] and bottom >= row[3]
    rect = (59, page_height-bottom, 550, page_height-top)
    annotation = Link(rect=rect, target_page_index=page_index, fit=Fit.fit(), border=[0,0,0])
    annotation[NameObject('/Contents')] = TextStringObject('Go to '+title)
    writer.add_annotation(3, annotation)
# Open at the tappable contents page in PDF readers that honor OpenAction.
writer.root_object[NameObject('/OpenAction')] = ArrayObject([writer.pages[3].indirect_reference, NameObject('/Fit')])
with output.open('wb') as f:
    writer.write(f)

result = PdfReader(output)
page_refs = {(p.indirect_reference.idnum, p.indirect_reference.generation):i for i,p in enumerate(result.pages)}
annotations = [a.get_object() for a in result.pages[3]['/Annots']]
assert len(annotations)==41
for i,(annotation,(title,index,depth)) in enumerate(zip(annotations,entries)):
    assert annotation['/Subtype']=='/Link'
    dest=annotation['/Dest']
    assert page_refs[(dest[0].idnum,dest[0].generation)]==index
    assert dest[1]=='/Fit'
    assert list(annotation['/Border'])==[0,0,0]
    assert annotation['/Contents']=='Go to '+title
    x0,y0,x1,y1=map(float,annotation['/Rect'])
    assert 0<=x0<x1<=603 and 0<=y0<y1<=783
    if i: assert y1 <= float(annotations[i-1]['/Rect'][1]) + 0.001
assert len(result.pages)==len(reader.pages)==328
for before,after in zip(reader.pages,result.pages):
    assert before.mediabox==after.mediabox
    b,a=before.get_contents(),after.get_contents()
    assert (b.get_data() if b else b'') == (a.get_data() if a else b'')
def outline(r):
    out=[]
    def walk(items,depth=0):
        for item in items:
            if isinstance(item,list): walk(item,depth+1)
            else: out.append((item.title,r.get_destination_page_number(item),depth))
    walk(r.outline)
    return out
assert outline(result)==outline(reader)
assert len(outline(result))==42
assert result.root_object['/OpenAction'][0].indirect_reference==result.pages[3].indirect_reference
print(f'Created: {output.resolve()}')
print('Verified all 41 contents links, non-overlapping tap areas, all 42 bookmarks, opening destination, and 328 unchanged pages.')
