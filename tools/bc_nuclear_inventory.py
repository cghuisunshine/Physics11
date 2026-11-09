"""Question, diagram, and procedure crops for BC Science Physics 11 Chapter 9."""
import re

DECAY_SERIES = (298, 167, 48, 551, 365)
IODINE_DATA = [(296, 60, 55, 184, 126), (296, 60, 230, 184, 254)]
LAB = (299, 48, 62, 563, 247)


def build_groups(lines):
    groups = []

    def group(topic, kind, title, *, shared=(), context=()):
        entry = dict(id=f'set-{len(groups) + 1}', topic=topic, kind=kind, title=title,
                     questions=[], shared=list(shared), context=list(context))
        groups.append(entry)
        return entry

    def add(entry, label, *boxes, text=None):
        if text is None:
            extracted = []
            for page, left, top, right, bottom in boxes:
                selected = sorted((line for line in lines[page]
                                   if left <= line['xMin'] < right and top <= line['yMin'] < bottom),
                                  key=lambda line: (line['yMin'], line['xMin']))
                extracted.extend(line['text'] for line in selected
                                 if not re.fullmatch(r'[_@\s]*', line['text']))
            text = ' '.join(' '.join(extracted).split()).replace('¨', '×')
        entry['questions'].append(dict(label=str(label), boxes=list(boxes), text=text))

    def numbered(entry, page, anchor, left, top, right, bottom, labels, *, keep=()):
        column = [line for line in lines[page]
                  if left <= line['xMin'] < right and top <= line['yMin'] < bottom]
        starts = []
        for line in column:
            match = re.match(r'^(\d+)\.(?=\s|$)', line['text'])
            if match and abs(line['xMin'] - anchor) < 1:
                starts.append((line['yMin'], int(match[1])))
        starts.sort()
        assert [label for _, label in starts] == list(labels), (page, entry['title'], starts)
        for index, (start, label) in enumerate(starts):
            stop = starts[index + 1][0] - .35 if index + 1 < len(starts) else bottom
            if label not in keep:
                stop = max(line['yMax'] for line in column if start <= line['yMin'] < stop
                           and not re.fullmatch(r'[_@\s]*', line['text'])) + .35
            add(entry, label, (page, left, start - .35, right, stop))

    def rows(entry, page, anchor, top, bottom, count):
        numbered(entry, page, anchor, 43, top, 580, bottom, range(1, count + 1))

    def columns(entry, page, left_labels, right_labels, *, top=49, keep=()):
        left = 48 if page % 2 else 63
        split = 302 if page % 2 else 316
        numbered(entry, page, left, 43, top, split, 726, left_labels, keep=keep)
        numbered(entry, page, left + 258, split, top, 580, 726, right_labels, keep=keep)

    g = group('9.1', 'Warm-up', 'The radiation symbol')
    add(g, 'Warm-up', (285, 48, 99, 544, 208),
        text='What hazard is represented by the three-bladed radiation symbol shown on some smoke detectors?')

    g = group('9.1', 'Quick check', 'The discovery of radioactivity')
    rows(g, 287, 60, 242, 390, 3)
    g = group('9.1', 'Quick check', 'Identifying alpha, beta, and gamma radiation')
    rows(g, 289, 60, 300, 574, 3)
    g = group('9.1', 'Quick check', 'Transmutation and the nucleus')
    rows(g, 292, 75, 300, 550, 4)
    g = group('9.1', 'Quick check', 'Isotopes and nuclear equations')
    numbered(g, 295, 60, 43, 92, 580, 210, (1, 2))
    add(g, 3, (295, 43, 212, 580, 235), text='Explain the meaning of the uranium-238 symbol, ²³⁸₉₂U.')
    add(g, 4, (295, 43, 267, 580, 402))

    g = group('9.1', 'Sample prompt', 'Sample 9.1.1 · Calculating half-life', shared=IODINE_DATA)
    add(g, '9.1.1', (296, 65, 408, 557, 456),
        text='How long will it take for a sample of iodine-131 to reach 1/16 of the original number of iodine-131 atoms? The table gives a half-life of 8.1 days.')
    g = group('9.1', 'Practice', 'Practice 9.1.1 · Calculating half-life')
    add(g, 1, (297, 52, 82, 555, 111))
    add(g, 2, (297, 52, 183, 555, 218),
        text='After 26 years, the number of cobalt-60 atoms is 1/32 of the original count. What is the half-life?')
    g = group('9.1', 'Quick check', 'Reading the uranium-238 decay series', shared=[DECAY_SERIES])
    rows(g, 297, 60, 525, 643, 3)
    g = group('9.1', 'Investigation', 'Investigation 9-1 · Simulating radioactive decay', context=[LAB])
    rows(g, 299, 60, 264, 280, 1)
    g = group('9.1', 'Section review', '9.1 Review · Radioactivity')
    columns(g, 300, range(1, 5), range(5, 8), keep=(6,))

    g = group('9.2', 'Warm-up', 'Fission and fusion')
    add(g, 'Warm-up', (301, 47, 133, 550, 152))
    g = group('9.2', 'Section review', '9.2 Review · Nuclear fission and fusion')
    columns(g, 307, range(1, 4), range(4, 7))

    g = group('Chapter review', 'Chapter review', 'Chapter 9 Review')
    numbered(g, 308, 63, 43, 84, 316, 726, (1, 2, 3))
    add(g, 4, (308, 316, 85, 580, 117))
    add(g, 5, (308, 316, 285, 580, 312), text='What does the symbol ⁰₋₁e represent?')
    add(g, 6, (308, 316, 486, 580, 510), text='Describe the differences between ²³⁵₉₂U and ²³⁸₉₂U.')
    columns(g, 309, range(7, 10), range(10, 13))
    columns(g, 310, range(13, 16), range(16, 18), keep=(13,))

    g = group('Extra practice', 'Extra practice', 'Chapter 9 Extra Practice')
    numbered(g, 311, 48, 43, 85, 302, 189, (1, 2, 3))
    add(g, 4, (311, 43, 191, 302, 214), text='What does the symbol ⁴₂He represent?')
    numbered(g, 311, 48, 43, 221, 302, 726, range(5, 9), keep=(6, 8))
    numbered(g, 311, 306, 302, 85, 580, 726, range(9, 18), keep=(9, 10))
    return groups
