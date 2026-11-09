"""Question and investigation crops for BC Science Physics 11 Chapter 6."""
import re

SUPERSCRIPT = str.maketrans('o0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
DIAGRAM_DESCRIPTIONS = {
    (199, 1): 'Circular wavefronts spread from a point toward a solid vertical barrier.',
    (199, 2): 'Straight, vertical wavefronts move right toward a narrow gap in a barrier.',
    (199, 4): 'The fronts pass through a strip of shallow water between two deep-water regions. Their spacing and slant change within the strip.',
    (199, 5): 'The approaching pairs are (a) equal crests, (b) unequal crests, (c) an equal crest and trough, (d) an unequal crest and trough, (e) tall then short crests facing shallow then deep troughs, and (f) tall then short crests facing deep then shallow troughs.',
    (203, 1): 'The image shows a repeating wave crossing a horizontal equilibrium line.',
    (203, 7): 'The four rows show progressively more complete cycles over the same horizontal span.',
}


def build_groups(lines):
    groups = []

    def group(topic, kind, title, *, shared=(), context=()):
        entry = dict(id=f'set-{len(groups) + 1}', topic=topic, kind=kind, title=title,
                     questions=[], shared=list(shared), context=list(context))
        groups.append(entry)
        return entry

    def full(page, top, bottom):
        return page, 44, top, 581, bottom

    def add(entry, label, *boxes):
        selected = (
            line['text'].strip()
            for page, left, top, right, bottom in boxes
            for line in lines[page]
            if left <= line['xMin'] < right and top <= line['yMin'] < bottom
        )
        text = ' '.join(line for line in selected if line and not re.fullmatch(r'[_@]+', line))
        # Repair symbol mappings in search and alt text. The crop retains the source notation.
        text = text.translate(str.maketrans({'¨': '×', '¡': '°', '\x89': '–'}))
        text = re.sub(r'(?<=× )10\s*(o?\d+)\b|\b10\s*(o\d+)\b',
                      lambda match: '10' + (match[1] or match[2]).translate(SUPERSCRIPT), text)
        text = re.sub(r'\b([mn]?)h\b(?=\s+(?:from|where|is))', r'\1λ', text)
        text = ' '.join(text.split())
        description = DIAGRAM_DESCRIPTIONS.get((boxes[-1][0], label))
        if description:
            text = text.rstrip('.') + '. ' + description
        entry['questions'].append(dict(label=str(label), boxes=list(boxes), text=text))

    def numbered(entry, page, anchor, left, top, right, bottom, expected, *, tight=True):
        column = [line for line in lines[page]
                  if left <= line['xMin'] < right and top <= line['yMin'] < bottom]
        starts = []
        for line in column:
            match = re.match(r'^(\d+)\.(?=\s|$)', line['text'])
            if match and abs(line['xMin'] - anchor) < 1:
                starts.append((line['yMin'], int(match[1])))
        starts.sort()
        assert [label for _, label in starts] == list(expected), (entry['title'], page, starts)
        for index, (start, label) in enumerate(starts):
            stop = starts[index + 1][0] - .4 if index + 1 < len(starts) else bottom
            if tight:
                stop = max(line['yMax'] for line in column
                           if start <= line['yMin'] < stop
                           and not re.fullmatch(r'[_@]+', line['text'].strip())) + .4
            box = (page, left, start - .4, right, stop)
            if page == 195 and label == 1:
                box = (page, left, 311, right, stop)  # Keep the adjacent Questions heading intact.
            # Printed p. 194 gives both drawing prompts a common instruction.
            if page == 199 and label in (1, 2):
                add(entry, label, (199, 44, 85, 300, 125), box)
            else:
                add(entry, label, box)

    def rows(entry, page, anchor, top, bottom, count, *, tight=True):
        numbered(entry, page, anchor, 44, top, 581, bottom, range(1, count + 1), tight=tight)

    def columns(entry, page, left_labels, right_labels, *, top=49, tight=True):
        anchor = 48 if page % 2 else 63
        split = 302 if page % 2 else 316
        numbered(entry, page, anchor, 44, top, split, 726, left_labels, tight=tight)
        numbered(entry, page, anchor + 258, split, top, 581, 726, right_labels, tight=tight)

    g = group('6.1', 'Warm-up', 'Vibrating glass: warm-up', shared=[full(179, 132, 203)])
    rows(g, 179, 60, 213, 335, 2)
    g = group('6.1', 'Quick check', 'Frequency and period: quick check')
    rows(g, 181, 60, 84, 323, 3, tight=False)
    g = group('6.1', 'Sample prompt', 'Sample 6.1.1: calculating wave speed')
    add(g, '6.1.1', full(182, 600, 614))
    g = group('6.1', 'Practice', 'Practice 6.1.1: calculating wave speed')
    rows(g, 183, 57.2, 76, 294, 3)
    g = group('6.1', 'Investigation', 'Investigation 6-1A: waves in springs',
              context=[full(184, 62, 365)])
    rows(g, 184, 75, 380, 535, 6)
    g = group('6.1', 'Investigation', 'Investigation 6-1B: waves in a tank',
              context=[full(185, 62, 479)])
    rows(g, 185, 63.5, 495, 535, 2)
    g = group('6.1', 'Section review', '6.1 Review: wave properties')
    columns(g, 186, range(1, 5), range(5, 9))
    columns(g, 187, range(9, 11), range(11, 13))

    g = group('6.2', 'Warm-up', 'Overlapping ripples: warm-up')
    add(g, 'Warm-up', full(188, 119, 158))
    g = group('6.2', 'Investigation', 'Investigation 6-2, Station 1: circular-wave reflection',
              context=[full(194, 62, 357)])
    add(g, 'Conclusion', full(194, 375, 390))
    g = group('6.2', 'Investigation', 'Investigation 6-2, Station 2: straight-wave reflection',
              context=[full(194, 397, 608)])
    rows(g, 194, 75, 632, 693, 2)
    g = group('6.2', 'Investigation', 'Investigation 6-2, Station 3: curved reflectors',
              context=[full(195, 58, 310)])
    rows(g, 195, 65, 325, 389, 2)
    g = group('6.2', 'Investigation', 'Investigation 6-2, Station 4: water-wave refraction',
              context=[full(195, 392, 725), full(196, 60, 351)])
    rows(g, 196, 75, 366, 577, 6)
    g = group('6.2', 'Investigation', 'Investigation 6-2, Station 5: diffraction',
              context=[full(196, 582, 724), full(197, 62, 307)])
    rows(g, 197, 60, 321, 483, 5)
    g = group('6.2', 'Investigation', 'Investigation 6-2, Station 6A: spring interference',
              context=[full(197, 487, 725)])
    rows(g, 198, 75, 78, 151, 2)
    g = group('6.2', 'Investigation', 'Investigation 6-2, Station 6B: water-wave interference',
              context=[full(198, 153, 377)])
    rows(g, 198, 75, 392, 562, 4)
    g = group('6.2', 'Section review', '6.2 Review: wave phenomena')
    columns(g, 199, range(1, 4), range(4, 6), top=84, tight=False)
    columns(g, 200, range(6, 10), range(10, 12))
    g = group('Chapter review', 'Chapter review', 'Chapter 6 Review Questions')
    columns(g, 201, range(1, 5), range(5, 10))
    # The textbook skips number 10. Keep the published numbering.
    columns(g, 202, range(11, 14), range(14, 17), tight=False)
    g = group('Extra practice', 'Extra practice', 'Chapter 6 Extra Practice')
    columns(g, 203, range(1, 8), range(8, 20), tight=False)
    return groups
