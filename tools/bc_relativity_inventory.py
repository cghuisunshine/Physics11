"""Question crops for BC Science Physics 11 Chapter 8."""
import re

SUPERSCRIPT = str.maketrans('o0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
RIVER = (266, 178, 191, 560, 361)
VAN = (268, 178, 302, 568, 453)
LIGHT_CLOCK = (271, 162, 306, 565, 570)
RIVER_DESCRIPTION = (
    ' In Figure 8.1.1 downstream is left. The river flows left at 5.0 km/h relative to Earth, '
    'the boat moves left at 10 km/h relative to water, the wind blows right at 20 km/h relative to Earth, '
    'and the bird flies left at 25 km/h relative to air.'
)


def build_groups(lines):
    groups = []

    def group(topic, kind, title, *, shared=()):
        entry = dict(id=f'set-{len(groups) + 1}', topic=topic, kind=kind, title=title,
                     questions=[], shared=list(shared), context=[])
        groups.append(entry)
        return entry

    def add(entry, label, *boxes, text=None, suffix=''):
        if text is None:
            extracted = []
            for page, left, top, right, bottom in boxes:
                selected = sorted((line for line in lines[page]
                                   if left <= line['xMin'] < right and top <= line['yMin'] < bottom),
                                  key=lambda line: (line['yMin'], line['xMin']))
                extracted.extend(line['text'] for line in selected
                                 if not re.fullmatch(r'[_@"\s]*', line['text']))
            text = ' '.join(' '.join(extracted).split()).replace('¨', '×')
            text = re.sub(r'× 10\s*(o?\d+)\b',
                          lambda m: '× 10' + m[1].translate(SUPERSCRIPT), text)
        entry['questions'].append(dict(label=str(label), boxes=list(boxes), text=text + suffix))

    def numbered(entry, page, anchor, left, top, right, bottom, labels, *, suffix=''):
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
            end = max(line['yMax'] for line in column if start <= line['yMin'] < stop
                      and not re.fullmatch(r'[_@"\s]*', line['text']))
            add(entry, label, (page, left, start - .35, right, end + .35), suffix=suffix)

    def rows(entry, page, anchor, top, bottom, labels, *, suffix=''):
        numbered(entry, page, anchor, 42, top, 581, bottom, labels, suffix=suffix)

    def columns(entry, page, left_labels, right_labels, *, top=49):
        left = 48 if page % 2 else 63
        split = 302 if page % 2 else 317
        numbered(entry, page, left, 42, top, split, 725, left_labels)
        numbered(entry, page, left + 258, split, top, 581, 725, right_labels)

    g = group('8.1', 'Warm-up', 'Motion at a red light')
    add(g, 'Warm-up', (265, 47, 134, 572, 164))

    g = group('8.1', 'Quick check', 'Relative velocities in the river', shared=[RIVER])
    # Two prompts use a secondary PDF font with a different broken character map.
    add(g, 1, (266, 63, 461, 565, 490),
        text='Find the velocity of the person in the boat relative to (a) the water and (b) Earth’s surface.',
        suffix=RIVER_DESCRIPTION)
    add(g, 2, (266, 63, 520, 565, 547),
        text='Find the velocity of the bird relative to (a) the air, (b) the water, and (c) Earth’s surface.',
        suffix=RIVER_DESCRIPTION)
    rows(g, 266, 75, 576, 710, range(3, 6), suffix=RIVER_DESCRIPTION)

    g = group('8.1', 'Quick check', 'A ball thrown inside a moving van', shared=[VAN])
    rows(g, 268, 75, 518, 601, (1, 2),
         suffix=' Figure 8.1.4 shows observer A standing by the road and observer B in a van travelling right at 50 km/h.')

    g = group('8.1', 'Sample prompt', 'Sample 8.1.1 · Time dilation', shared=[LIGHT_CLOCK])
    add(g, '8.1.1', (272, 57, 408, 562, 437))
    g = group('8.1', 'Practice', 'Practice 8.1.1 · Time dilation',
              shared=[(273, 51, 81, 553, 126)])
    for label, left, top, right in [(1, 53, 136, 253), (2, 53, 257, 253),
                                     (3, 269, 136, 551), (4, 269, 257, 551)]:
        add(g, label, (273, left, top, right, top + 14),
            suffix=' Calculate the outside observer’s time for a proper time of 5.0 s.')

    g = group('8.1', 'Sample prompt', 'Sample 8.1.2 · Length contraction')
    add(g, '8.1.2', (275, 51, 81, 555, 97))
    g = group('8.1', 'Practice', 'Practice 8.1.2 · Length contraction',
              shared=[(275, 51, 334, 552, 369)])
    rows(g, 275, 57.2, 380, 623, (1, 2, 3),
         suffix=' Find the length measured from outside the ship when its proper length is 100 m.')

    g = group('8.1', 'Quick check', 'Newtonian and relativistic momentum')
    rows(g, 277, 60, 84, 458, (1, 2, 3))

    g = group('8.1', 'Section review', '8.1 Review · Special relativity')
    columns(g, 279, (1, 2), (3,))
    numbered(g, 280, 63, 42, 49, 317, 725, (4, 5))
    numbered(g, 280, 321.4, 317, 49, 581, 359, (6,))
    add(g, 7, (280, 317, 362, 581, 472),
        text='When you look at a distant star, are you seeing it (a) as it appears now, '
             '(b) as it will look in the future, or (c) as it looked in the past? Explain your answer.')
    columns(g, 281, (8, 9), (10,))
    numbered(g, 282, 63, 42, 49, 317, 725, (11,))

    g = group('8.1', 'Extension', '8.1 Extension · The speed limit and gravity')
    numbered(g, 282, 321, 317, 78, 581, 726, (12, 13))

    g = group('Extra practice', 'Extra practice', 'Chapter 8 Extra Practice')
    columns(g, 283, (1, 2, 3), (4, 5, 6), top=84)
    return groups
