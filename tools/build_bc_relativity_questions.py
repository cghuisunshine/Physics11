#!/usr/bin/env python3
"""Build the standalone Special Relativity question collection with Pillow and Poppler."""
from pathlib import Path
from tempfile import TemporaryDirectory

from bc_question_collection import ROOT, build_collection, read_pages
from bc_relativity_answers import answer_groups
from bc_relativity_inventory import build_groups

TITLE = 'Special Relativity'
TOPICS = [('8.1', '8.1 Einstein’s theory of special relativity'), ('Extra practice', 'Extra practice')]
KINDS = ['Warm-up', 'Sample prompt', 'Practice', 'Quick check', 'Section review', 'Extension', 'Extra practice']


def build(work):
    scale = 1500
    lines, dimensions = read_pages(264, 283, work, scale)
    groups = build_groups(lines)
    answers = {}
    for group, solutions in zip(groups, answer_groups, strict=True):
        assert len(group['questions']) == len(solutions), group['title']
        for solution in solutions:
            answers[f'q-{len(answers) + 1}'] = solution
    template = (ROOT / 'tools/bc-energy-template.html').read_text()
    for old, new in [
        ('Chapter 5', 'Chapter 8'),
        ('energy-notes.html', 'relativity-notes.html'),
        ('Energy', TITLE),
        ('#page=137', '#page=264'),
        ('144', str(len(answers))),
        ('132-172', '259–278'),
        ('Every warm-up, quick check, practice problem, section and chapter review, and extra-practice problem, plus all six sample-problem prompts and the investigation questions and challenges.',
         'The warm-up, quick checks, two worked-example prompts, practice problems, section review, extension, and extra practice.'),
        ('Investigation answers explain how to use your measurements. Procedures open below their headings. ',
         'Shared textbook figures and setups accompany the relevant questions. '),
        ('Try work, heat, or 5.4', 'Try time dilation, momentum, or spaceship'),
        ('Choose beginner questions about work and power. Avoid thermal energy questions.',
         'Choose introductory questions about proper time and length contraction.'),
        ('Remove thermal energy questions. Or: Keep the five easiest work questions.',
         'Keep only questions involving reference frames or the Lorentz factor.'),
        ('Answers use g = 9.81 m/s² unless a question specifies another value. Use c = 4200 J/(kg·°C) for water and 1 hp = 746 W unless stated otherwise. Graph readings are approximate. Source errors are explained in the relevant answers. Assumptions and ambiguous wording are explained in the affected answers.',
         'Use c ≈ 3.00 × 10⁸ m/s. Identify the reference frame before applying a formula. Source discrepancies and assumptions are explained with the relevant answers.'),
    ]:
        assert old in template, old
        template = template.replace(old, new)
    template = template.replace(f'>{TITLE} notes</a>', '>Relativity notes</a> · '
                                '<a href="relativity-review.html">Quick Review</a>')
    build_collection(
        groups, answers, lines, dimensions, work, chapter=8, title=TITLE,
        slug='relativity', topics=TOPICS, kinds=KINDS, template=template, scale=scale,
    )


if __name__ == '__main__':
    with TemporaryDirectory(prefix='bc-ch8-') as directory:
        build(Path(directory))
