#!/usr/bin/env python3
"""Build the standalone Chapter 7 question collection with Pillow and Poppler."""
from pathlib import Path
from tempfile import TemporaryDirectory

from bc_optics_answers import answer_groups
from bc_optics_inventory import build_groups
from bc_question_collection import ROOT, build_collection, read_pages

TITLE = 'Light and Geometric Optics'
TOPICS = [
    ('7.1', '7.1 Reflection'), ('7.2', '7.2 Curved mirrors'),
    ('7.3', '7.3 Refraction of light'), ('7.4', '7.4 Optics'),
    ('Chapter review', 'Chapter review'), ('Extra practice', 'Extra practice'),
]
KINDS = ['Warm-up', 'Sample prompt', 'Practice', 'Quick check', 'Investigation',
         'Challenge', 'Section review', 'Chapter review', 'Extra practice']


def build(work):
    scale = 1500
    lines, dimensions = read_pages(204, 263, work, scale)
    groups = build_groups(lines)
    answers = {}
    for group, solutions in zip(groups, answer_groups, strict=True):
        assert len(group['questions']) == len(solutions), group['title']
        for solution in solutions:
            answers[f'q-{len(answers) + 1}'] = solution
    template = (ROOT / 'tools/bc-energy-template.html').read_text()
    for old, new in [
        ('Chapter 5', 'Chapter 7'),
        ('energy-notes.html', 'optics-notes.html'),
        ('Energy', TITLE),
        ('#page=137', '#page=204'),
        ('144', str(len(answers))),
        ('132-172', '199–258'),
        ('all six sample-problem prompts and the investigation questions and challenges',
         'the mirror-equation sample, investigations, and challenges'),
        ('Try work, heat, or 5.4', 'Try convex, Snell, or 7.4'),
        ('Choose beginner questions about work and power. Avoid thermal energy questions.',
         'Choose introductory questions about ray diagrams and image location.'),
        ('Remove thermal energy questions. Or: Keep the five easiest work questions.',
         'Keep questions about Snell’s law and total internal reflection.'),
        ('Answers use g = 9.81 m/s² unless a question specifies another value. Use c = 4200 J/(kg·°C) for water and 1 hp = 746 W unless stated otherwise. Graph readings are approximate. Source errors are explained in the relevant answers. Assumptions and ambiguous wording are explained in the affected answers.',
         'Measure ray angles from the normal. For mirrors and thin lenses, a positive image distance gives a real image and a negative one gives a virtual image.'),
    ]:
        assert old in template, old
        template = template.replace(old, new)
    template = template.replace(f'>{TITLE} notes</a>', '>Optics notes</a> · '
                                '<a href="optics-review.html">Quick Review</a>')
    build_collection(
        groups, answers, lines, dimensions, work, chapter=7, title=TITLE,
        slug='optics', topics=TOPICS, kinds=KINDS, template=template, scale=scale,
    )


if __name__ == '__main__':
    with TemporaryDirectory(prefix='bc-ch7-') as directory:
        build(Path(directory))
