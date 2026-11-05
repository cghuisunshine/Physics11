from pathlib import Path
import json
from pypdf import PdfReader, PdfWriter

source = Path('bc_science_physics_11.pdf')
output = Path('output/pdf/bc_science_physics_11_bookmarked.pdf')
chapters = [
    ('1 Skills, Methods, and the Nature of Physics', 1, [
        ('1.1 What is Physics?', 2),
        ('1.2 Equipment Essentials', 6),
        ('1.3 Physics Essentials', 9),
        ('1.4 Analysis of Units and Conversions in Physics', 19),
        ('1.5 Vectors', 33),
    ]),
    ('2 Kinematics', 37, [
        ('2.1 Speed and Velocity', 38),
        ('2.2 Acceleration', 48),
        ('2.3 Uniform Acceleration', 54),
        ('2.4 Acceleration of Bodies Due to Gravity', 64),
    ]),
    ('3 Forces', 75, [
        ('3.1 Force of Gravity', 76),
        ('3.2 Friction', 85),
        ("3.3 Hooke's Law", 93),
    ]),
    ("4 Newton's Laws of Motion", 101, [
        ("4.1 Inertia and Newton's First Law", 102),
        ("4.2 Newton's Second Law of Motion", 109),
        ("4.3 Newton's Third Law of Motion", 116),
        ('4.4 Momentum', 121),
    ]),
    ('5 Energy', 131, [
        ('5.1 Do You Know the Meaning of Work?', 132),
        ('5.2 Mechanical Energy', 142),
        ('5.3 Temperature, Heat, and Thermal Energy', 150),
        ('5.4 Measuring Thermal Energy', 160),
    ]),
    ('6 Wave Motion', 173, [
        ('6.1 Wave Properties', 174),
        ('6.2 Wave Phenomena', 183),
    ]),
    ('7 Light and Geometric Optics', 199, [
        ('7.1 Reflection', 200),
        ('7.2 Curved Mirrors', 212),
        ('7.3 Refraction of Light', 226),
        ('7.4 Optics', 239),
    ]),
    ('8 Special Relativity', 259, [
        ("8.1 Einstein's Theory of Special Relativity", 260),
    ]),
    ('9 Nuclear Fission and Fusion', 279, [
        ('9.1 The Discovery of Radioactivity', 280),
        ('9.2 Nuclear Fission and Fusion', 296),
    ]),
]
back_matter = [
    ('Answers to Even-Numbered Numerical and Short-Answer Questions', 307),
    ('Glossary', 313),
    ('Index', 318),
]
reader = PdfReader(source)
assert len(reader.pages) == 328
assert not reader.outline
writer = PdfWriter()
writer.clone_document_from_reader(reader)
expected = [('Contents', 3, 0)]
writer.add_outline_item('Contents', 3)
# Five physical pages precede printed page 1; pypdf destinations are zero-based.
for title, printed_page, sections in chapters:
    page_index = printed_page + 4
    parent = writer.add_outline_item(title, page_index, bold=True)
    expected.append((title, page_index, 0))
    for section_title, section_page in sections:
        writer.add_outline_item(section_title, section_page + 4, parent=parent)
        expected.append((section_title, section_page + 4, 1))
for title, printed_page in back_matter:
    writer.add_outline_item(title, printed_page + 4, bold=True)
    expected.append((title, printed_page + 4, 0))
writer.page_mode = '/UseOutlines'
with output.open('wb') as f:
    writer.write(f)

result = PdfReader(output)
actual = []
def collect(items, depth=0):
    for item in items:
        if isinstance(item, list):
            collect(item, depth + 1)
        else:
            actual.append((item.title, result.get_destination_page_number(item), depth))
collect(result.outline)
assert actual == expected, (actual, expected)
assert len(result.pages) == len(reader.pages)
for i, (before, after) in enumerate(zip(reader.pages, result.pages)):
    assert before.mediabox == after.mediabox, i
    assert before.rotation == after.rotation, i
    b, a = before.get_contents(), after.get_contents()
    assert (b.get_data() if b else b'') == (a.get_data() if a else b''), i
assert result.metadata == reader.metadata
assert result.page_mode == '/UseOutlines'
Path('tmp/pdfs/bookmarks_verified.json').write_text(json.dumps(actual, indent=2))
print(f'Created {output.resolve()}')
print(f'Validated {len(actual)} bookmarks, hierarchy, page destinations, and all {len(result.pages)} unchanged page content streams.')
