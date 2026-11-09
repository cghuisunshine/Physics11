#!/usr/bin/env python3
"""Build the standalone Chapter 5 question collection with Pillow and Poppler."""
from bc_energy_answers import ANSWERS
from bc_energy_inventory import build_groups
from bc_question_collection import ROOT, build_collection, read_pages

TOPICS=[('5.1','5.1 Work, power, and machines'),('5.2','5.2 Mechanical energy'),('5.3','5.3 Temperature and heat transfer'),('5.4','5.4 Thermal energy and efficiency'),('Chapter review','Chapter review'),('Extra practice','Extra practice')]
KINDS=['Warm-up','Sample prompt','Practice','Quick check','Investigation','Challenge','Section review','Chapter review','Extra practice']


if __name__ == '__main__':
    work = ROOT / 'tmp/bc-ch5-render'
    lines, dimensions = read_pages(137, 177, work)
    build_collection(
        build_groups(lines), ANSWERS, lines, dimensions, work,
        chapter=5, title='Energy', slug='energy', topics=TOPICS, kinds=KINDS,
        template=(ROOT / 'tools/bc-energy-template.html').read_text(),
    )
