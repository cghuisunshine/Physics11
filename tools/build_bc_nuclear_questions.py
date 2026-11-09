#!/usr/bin/env python3
"""Build the standalone Chapter 9 question collection with Pillow and Poppler."""
from pathlib import Path
from tempfile import TemporaryDirectory

from bc_nuclear_answers import answer_groups
from bc_nuclear_inventory import build_groups
from bc_question_collection import ROOT, build_collection, read_pages

TITLE = 'Nuclear Fission and Fusion'
TOPICS = [
    ('9.1', '9.1 The discovery of radioactivity'),
    ('9.2', '9.2 Nuclear fission and fusion'),
    ('Chapter review', 'Chapter review'), ('Extra practice', 'Extra practice'),
]
KINDS = ['Warm-up', 'Sample prompt', 'Practice', 'Quick check', 'Investigation',
         'Section review', 'Chapter review', 'Extra practice']


def build(work):
    scale = 1500
    lines, dimensions = read_pages(284, 311, work, scale)
    groups = build_groups(lines)
    answers = {}
    for group, solutions in zip(groups, answer_groups, strict=True):
        assert len(group['questions']) == len(solutions), group['title']
        for solution in solutions:
            answers[f'q-{len(answers) + 1}'] = solution
    template = (ROOT / 'tools/bc-energy-template.html').read_text()
    for old, new in [
        ('Chapter 5', 'Chapter 9'),
        ('energy-notes.html', 'nuclear-notes.html'),
        ('Energy', TITLE),
        ('#page=137', '#page=284'),
        ('144', str(len(answers))),
        ('132-172', '279–306'),
        ('all six sample-problem prompts and the investigation questions and challenges',
         'the half-life sample and dice-decay investigation'),
        ('Try work, heat, or 5.4', 'Try half-life, gamma, or reactor'),
        ('Choose beginner questions about work and power. Avoid thermal energy questions.',
         'Choose introductory questions about half-life and balancing decay equations.'),
        ('Remove thermal energy questions. Or: Keep the five easiest work questions.',
         'Keep only questions on isotope notation or half-life.'),
        ('Answers use g = 9.81 m/s² unless a question specifies another value. Use c = 4200 J/(kg·°C) for water and 1 hp = 746 W unless stated otherwise. Graph readings are approximate. Source errors are explained in the relevant answers. Assumptions and ambiguous wording are explained in the affected answers.',
         'Check mass number and charge number separately. Half-life calculations use the values specified in the exercise. Printed isotope and equation discrepancies are explained with the relevant answers.'),
    ]:
        assert old in template, old
        template = template.replace(old, new)
    template = template.replace(f'>{TITLE} notes</a>', '>Nuclear physics notes</a> · '
                                '<a href="nuclear-review.html">Quick Review</a>')
    build_collection(
        groups, answers, lines, dimensions, work, chapter=9, title=TITLE,
        slug='nuclear', topics=TOPICS, kinds=KINDS, template=template, scale=scale,
    )


if __name__ == '__main__':
    with TemporaryDirectory(prefix='bc-ch9-') as directory:
        build(Path(directory))
