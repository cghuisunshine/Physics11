"""Source crops for BC Science Physics 11 Chapter 7, in textbook order."""
import re

SYMBOLS = str.maketrans({'¡': '°', '¨': '×', '\x89': '–', 'ƿ': 'θ', '': 'θ'})
EXPONENTS = str.maketrans('o0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def build_groups(lines):
    groups = []

    def group(topic, kind, title, *, shared=(), context=()):
        entry = dict(id=f'set-{len(groups) + 1}', topic=topic, kind=kind, title=title,
                     questions=[], shared=list(shared), context=list(context))
        groups.append(entry)
        return entry

    def box(page, top, bottom, left=42, right=582):
        return (page, left, top, right, bottom)

    def add(entry, label, *boxes):
        text = []
        for page, left, top, right, bottom in boxes:
            selected = sorted((line for line in lines[page]
                               if left <= line['xMin'] < right and top <= line['yMin'] < bottom),
                              key=lambda line: (line['yMin'], line['xMin']))
            text.extend(line['text'] for line in selected
                        if not re.fullmatch(r'[_@\s]*', line['text']))
        content = ' '.join(' '.join(text).translate(SYMBOLS).split())
        content = re.sub(r'([×w]) 10\s*(o?\d+)\b',
                         lambda m: '× 10' + m[2].translate(EXPONENTS), content)
        content = content.replace('renection', 'reflection').replace('Renection', 'Reflection')
        entry['questions'].append(dict(label=str(label), boxes=list(boxes), text=content))

    def numbered(entry, page, anchor, top, bottom, labels, *, left=42, right=582, keep=()):
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
            add(entry, label, box(page, start - .35, stop, left, right))

    def rows(entry, page, anchor, top, bottom, count, *, start=1, keep=()):
        numbered(entry, page, anchor, top, bottom, range(start, start + count), keep=keep)

    def columns(entry, page, left_labels, right_labels, *, top=49, right_end=728, keep=()):
        anchor = 48 if page % 2 else 63
        split = 302 if page % 2 else 316
        numbered(entry, page, anchor, top, 728, left_labels, right=split, keep=keep)
        numbered(entry, page, anchor + 258, top, right_end, right_labels, left=split, keep=keep)

    g = group('7.1', 'Warm-up', 'Pinhole camera warm-up')
    add(g, 'Warm-up', box(205, 93, 220))
    g = group('7.1', 'Quick check', 'Plane-mirror images')
    rows(g, 210, 75, 403, 680, 3)
    g = group('7.1', 'Investigation', 'Investigation 7-1A · Image location',
              context=[box(211, 62, 269)])
    rows(g, 211, 60, 284, 314, 2)
    plane_rays = [box(211, 316, 725), box(212, 62, 486)]
    g = group('7.1', 'Investigation', 'Investigation 7-1A · Reflected rays', context=plane_rays)
    rows(g, 212, 75, 501, 586, 3)
    g = group('7.1', 'Challenge', 'Investigation 7-1A · Photographing a mirror image')
    rows(g, 212, 75, 602, 638, 1)
    multiple = [box(213, 62, 724), box(214, 62, 248)]
    g = group('7.1', 'Investigation', 'Investigation 7-1B · Multiple images', context=multiple)
    rows(g, 214, 76, 263, 347, 2)
    g = group('7.1', 'Challenge', 'Investigation 7-1B · Infinity box and periscope')
    rows(g, 214, 76, 363, 422, 2)
    g = group('7.1', 'Section review', '7.1 Review · Reflection and the spectrum')
    columns(g, 215, range(1, 6), range(6, 9))
    columns(g, 216, range(9, 12), range(12, 14))

    g = group('7.2', 'Warm-up', 'Spoon mirrors warm-up')
    add(g, 'Warm-up', box(217, 120, 151))
    g = group('7.2', 'Quick check', 'Concave mirror ray diagrams')
    add(g, 1, box(220, 79, 440))
    g = group('7.2', 'Sample prompt', 'Sample 7.2.1 · Using the mirror equation')
    add(g, '7.2.1', box(222, 318, 346))
    g = group('7.2', 'Practice', 'Practice 7.2.1 · Using the mirror equation')
    rows(g, 223, 57.2, 80, 462, 4)
    g = group('7.2', 'Investigation', 'Investigation 7-2A · Convex mirrors',
              context=[box(225, 62, 431)])
    rows(g, 225, 60, 446, 519, 4)
    g = group('7.2', 'Investigation', 'Investigation 7-2A · Concave mirrors',
              context=[box(225, 520, 725), box(226, 62, 134)])
    rows(g, 226, 79, 149, 194, 3)
    g = group('7.2', 'Investigation', 'Investigation 7-2A · Measuring focal length',
              context=[box(226, 195, 607)])
    rows(g, 226, 79, 622, 680, 2)
    g = group('7.2', 'Investigation', 'Investigation 7-2B · Images in concave mirrors',
              context=[box(227, 62, 497)])
    rows(g, 227, 60, 513, 630, 6)
    g = group('7.2', 'Section review', '7.2 Review · Curved mirrors')
    rows(g, 228, 63, 86, 727, 6, keep=(6,))
    rows(g, 229, 48, 52, 727, 3, start=7, keep=(9,))
    rows(g, 230, 63, 52, 605, 1, start=10)
    g = group('7.2', 'Challenge', 'Curved mirrors challenge · The Mirage')
    add(g, 1, box(230, 605, 726))

    g = group('7.3', 'Warm-up', 'Pencil in water warm-up')
    add(g, 'Warm-up', box(231, 130, 161))
    g = group('7.3', 'Quick check', 'Snell’s law and dispersion')
    rows(g, 233, 60, 338, 647, 4)
    g = group('7.3', 'Quick check', 'Critical angles')
    rows(g, 235, 60, 79, 230, 3)
    g = group('7.3', 'Investigation', 'Investigation 7-3A · Refraction in water',
              context=[box(238, 62, 631)])
    rows(g, 238, 75, 646, 716, 3)
    g = group('7.3', 'Investigation', 'Investigation 7-3B · Internal reflection and critical angle',
              shared=[box(239, 512, 705, 51, 164), box(239, 707, 721, 52, 184)], context=[box(239, 62, 512)])
    numbered(g, 239, 168, 527, 600, range(1, 3), left=166)
    g = group('7.3', 'Investigation', 'Investigation 7-3C · Polarization',
              context=[box(240, 62, 725), box(241, 62, 572)])
    rows(g, 241, 60, 587, 676, 4)
    g = group('7.3', 'Section review', '7.3 Review · Refraction of light')
    columns(g, 242, range(1, 3), range(3, 8), keep=(1, 2))
    columns(g, 243, range(8, 12), range(12, 14), right_end=501)
    g = group('7.3', 'Challenge', 'Refraction Brain Stretch')
    numbered(g, 243, 306, 544, 727, range(1, 8), left=302)

    g = group('7.4', 'Warm-up', 'Looking through lenses warm-up')
    add(g, 'Warm-up', box(244, 130, 174))
    g = group('7.4', 'Quick check', 'Tracing rays through lenses',
              shared=[box(246, 46, 435)])
    rows(g, 247, 60, 83, 320, 2)
    g = group('7.4', 'Quick check', 'The thin-lens equation')
    rows(g, 249, 60, 81, 260, 3)
    g = group('7.4', 'Investigation', 'Investigation 7-4A · Focusing with lenses')
    add(g, 1, box(254, 136, 260))
    add(g, 2, box(254, 271, 342, 65, 459), box(254, 270, 465, 466, 560))
    add(g, 3, box(254, 352, 555, 65, 465))
    add(g, 4, box(254, 573, 664))
    lens_positions = box(255, 218, 722, 315, 549)
    g = group('7.4', 'Investigation', 'Investigation 7-4B · Predicting convex-lens images',
              shared=[lens_positions], context=[box(255, 62, 215)])
    numbered(g, 255, 60, 231, 467, range(1, 4), right=312)
    g = group('7.4', 'Investigation', 'Investigation 7-4B · Testing convex-lens images',
              shared=[lens_positions], context=[box(256, 62, 519)])
    rows(g, 256, 75, 534, 658, 4)
    g = group('7.4', 'Section review', '7.4 Review · Lenses and optical instruments')
    columns(g, 257, range(1, 4), range(4, 8))
    columns(g, 258, range(8, 10), range(10, 14))

    g = group('Chapter review', 'Chapter review', 'Chapter 7 Review')
    columns(g, 259, range(1, 7), range(7, 12))
    rows(g, 260, 63, 52, 722, 7, start=12)
    rows(g, 261, 48, 52, 723, 3, start=19, keep=(20, 21))
    rows(g, 262, 63, 52, 723, 5, start=22, keep=(23,))
    g = group('Extra practice', 'Extra practice', 'Chapter 7 Extra Practice')
    columns(g, 263, range(1, 15), range(15, 21), keep=(16, 17))
    return groups
