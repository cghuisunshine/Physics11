#!/usr/bin/env python3
"""Build the standalone Wave Motion question collection with Pillow and Poppler."""
from pathlib import Path
from tempfile import TemporaryDirectory

from bc_question_collection import ROOT, build_collection, read_pages
from bc_wave_motion_answers import answer_groups
from bc_wave_motion_inventory import build_groups

TOPICS = [
    ('6.1', '6.1 Wave properties'), ('6.2', '6.2 Wave phenomena'),
    ('Chapter review', 'Chapter review'), ('Extra practice', 'Extra practice'),
]
KINDS = ['Warm-up', 'Sample prompt', 'Practice', 'Quick check', 'Investigation',
         'Section review', 'Chapter review', 'Extra practice']


def build(work):
    scale = 1500
    lines, dimensions = read_pages(179, 203, work, scale)
    groups = build_groups(lines)
    answers = {}
    for group, solutions in zip(groups, answer_groups, strict=True):
        for _, solution in zip(group['questions'], solutions, strict=True):
            answers[f'q-{len(answers) + 1}'] = solution
    template = (ROOT / 'tools/bc-energy-template.html').read_text()
    for old, new in [
        ('Chapter 5', 'Chapter 6'),
        ('energy-notes.html', 'wave-motion-notes.html'),
        ('Energy', 'Wave Motion'),
        ('#page=137', '#page=178'),
        ('144', str(len(answers))),
        ('132-172', '173–198'),
        ('all six sample-problem prompts and the investigation questions and challenges',
         'the sample-problem prompt and investigation conclusions'),
        ('Try work, heat, or 5.4', 'Try wavelength, reflection, or 6.2'),
        ('Choose beginner questions about work and power. Avoid thermal energy questions.',
         'Choose beginner questions about frequency and wave speed.'),
        ('Remove thermal energy questions. Or: Keep the five easiest work questions.',
         'Remove Doppler questions. Or: Keep the five easiest wave-speed questions.'),
        ('Investigation answers explain how to use your measurements. Procedures open below their headings.',
         'Open the investigation procedures below their headings.'),
        ('Answers use g = 9.81 m/s² unless a question specifies another value. Use c = 4200 J/(kg·°C) for water and 1 hp = 746 W unless stated otherwise. Graph readings are approximate. Source errors are explained in the relevant answers. Assumptions and ambiguous wording are explained in the affected answers.',
         'Use the stated wave speed when supplied. Investigation answers describe expected patterns and how to interpret your own measurements. The chapter review follows the textbook numbering, which skips question 10.'),
    ]:
        assert old in template, old
        template = template.replace(old, new)
    template = template.replace('>Wave Motion notes</a>', '>Wave Motion notes</a> · '
                                '<a href="wave-motion-review.html">Quick Review</a>')
    build_collection(
        groups, answers, lines, dimensions, work, chapter=6, title='Wave Motion',
        slug='wave-motion', topics=TOPICS, kinds=KINDS, template=template, scale=scale,
    )


if __name__ == '__main__':
    with TemporaryDirectory(prefix='bc-ch6-') as directory:
        build(Path(directory))
