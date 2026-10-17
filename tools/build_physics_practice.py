#!/usr/bin/env python3
"""Build a standalone practice studio from chapter collections; Python stdlib only.

Each registry entry names an inventory (groups/questions with stable ids) and its
question HTML. The source page owns question crops, shared figures/procedures,
and worked answers. No image rendering or internet access is needed to rebuild.
"""
import argparse
import json
import re
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


@dataclass
class Node:
    tag: str
    attrs: dict
    start: int
    content_start: int
    content_end: int = 0
    end: int = 0
    children: list = field(default_factory=list)

    def find(self, *, id=None, cls=None):
        for child in self.children:
            if (id is not None and child.attrs.get('id') == id) or (cls is not None and cls in child.attrs.get('class', '').split()):
                return child
            found = child.find(id=id, cls=cls)
            if found:
                return found
        return None


class Tree(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.lines = [0]
        self.lines.extend(m.end() for m in re.finditer('\n', source))
        self.root = Node('', {}, 0, 0)
        self.stack = [self.root]
        self.feed(source)

    def absolute_position(self):
        line, column = self.getpos()
        return self.lines[line-1] + column

    def handle_starttag(self, tag, attrs):
        start = self.absolute_position()
        node = Node(tag, dict(attrs), start, start+len(self.get_starttag_text()))
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)
        else:
            node.content_end = node.end = node.content_start

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            node = self.stack.pop()
            node.content_end = node.end = node.content_start

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                node = self.stack[i]
                node.content_end = self.absolute_position()
                node.end = self.source.find('>', self.absolute_position())+1
                self.stack = self.stack[:i]
                return

    def outer(self, node):
        return self.source[node.start:node.end] if node else ''

    def inner(self, node):
        return self.source[node.content_start:node.content_end] if node else ''


def clean_fragment(fragment):
    # These fragments are copied into a pinned panel too. Collection control IDs
    # and scripts must not leak into the practice page.
    if re.search(r'<script\b|\bon\w+\s*=', fragment, re.I):
        raise ValueError('Chapter content must not contain scripts/event handlers')
    fragment = re.sub(r'\s+(?:id|aria-labelledby)="[^"]*"', '', fragment)
    for src in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', fragment, re.I):
        if not src.startswith('data:image/'):
            raise ValueError('Question images must be embedded for offline practice')
    return fragment


def enlarge_question_images(fragment):
    # Double the collection's display widths, retaining its responsive width
    # cap and automatic height for question crops, shared graphs and data.
    def enlarge(match):
        return re.sub(r'(?<![-\w])width:(\d+)px',
                      lambda width: f'width:{2 * int(width[1])}px', match[0])
    return re.sub(r'<img\b[^>]*>', enlarge, fragment, flags=re.I)


def load_bank(registry_path):
    registry = json.loads(registry_path.read_text())
    bank, ids, chapters = [], set(), set()
    levels = {'Warm-up': 1, 'Sample prompt': 1, 'Chapter review': 3, 'Extra practice': 3}
    for chapter in registry['chapters']:
        cid = chapter['id']
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]*', cid) or cid in chapters:
            raise ValueError('Chapter IDs must be unique, stable lowercase identifiers')
        chapters.add(cid)
        source_path = ROOT / chapter['html']
        inventory = json.loads((ROOT / chapter['inventory']).read_text())
        tree = Tree(source_path.read_text())
        topic_select = tree.root.find(id='topic')
        topic_titles = {option.attrs['value']: unescape(re.sub(r'<[^>]+>', '', tree.inner(option))).strip()
                        for option in (topic_select.children if topic_select else [])
                        if option.tag == 'option' and option.attrs.get('value')}
        number = 0
        for group in inventory['groups']:
            section = tree.root.find(id=group['id'])
            if not section:
                raise ValueError(f'Missing question set {group["id"]}')
            shared = tree.outer(section.find(cls='shared'))
            context = tree.outer(section.find(cls='context'))
            for question in group['questions']:
                number += 1
                qid = f'{cid}-{question["id"]}'
                if qid in ids:
                    raise ValueError(f'Duplicate question ID {qid}')
                ids.add(qid)
                article = section.find(id=question['id'])
                image_node = article.find(cls='question-image') if article else None
                answer_node = article.find(cls='answer') if article else None
                if not image_node or not answer_node:
                    raise ValueError(f'Question {qid} needs a question-image and an answer')
                answer = re.sub(r'^\s*<h3>Answer</h3>', '', tree.inner(answer_node)).strip()
                if not answer:
                    raise ValueError(f'Missing worked answer for {qid}')
                bank.append({
                    'id': qid, 'sourceId': question['id'], 'kind': 'textbook',
                    'chapter': cid, 'chapterNumber': chapter['number'], 'chapterTitle': chapter['title'],
                    'number': number, 'topic': f'Ch {chapter["number"]} · {group["topic"]}',
                    'topicTitle': topic_titles.get(group['topic'], group['topic']),
                    'level': levels.get(group['kind'], 2), 'questionType': group['kind'],
                    'title': f'{group["title"]} — {question["label"]}',
                    'html': enlarge_question_images(clean_fragment(shared+tree.outer(image_node)+context)),
                    'solution': clean_fragment(answer),
                    'answer': 'See worked solution',
                    'url': chapter['html']+'#'+question['id'],
                })
        if number != inventory['question_count']:
            raise ValueError(f'Inventory count mismatch for {cid}: {number}')
    if not bank:
        raise ValueError('Register at least one chapter with questions')
    return bank


def embedded_script(name):
    text = (TOOLS / name).read_text()
    if '</script' in text.lower():
        raise ValueError(f'Unsafe inline script terminator in {name}')
    return '<script>\n'+text+'\n</script>\n'


def build(registry_path, output_path):
    bank = load_bank(registry_path)
    data = json.dumps(bank, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    scripts = '<script id="question-bank" type="application/json">'+data+'</script>\n'
    for name in ['physics-activity.js', 'physics-practice-core.js', 'physics-photo-review.js', 'physics-drawing-pad.js', 'physics-students.js', 'physics-live-share.js', 'physics-practice.js']:
        scripts += embedded_script(name)
    template = (TOOLS / 'physics-practice-template.html').read_text()
    output_path.write_text(template.replace('<!-- PRACTICE_SCRIPTS -->', scripts))
    # Reuse the studio's visual style and read-only monitoring controls.
    head = re.search(r'<head>(.*?)</head>', template, re.S).group(1)
    head = head.replace('Physics 11 · Practice Studio', 'Physics 11 · Student Activity')
    dialog = re.search(r'<dialog[^>]*>(.*?)</dialog>', template, re.S).group(1)
    dialog = re.sub(r'<button id="activity-close".*?</button>', '', dialog)
    dialog = re.sub(r'<p><a id="activity-page-link".*?</p>', '', dialog)
    monitor = '<!doctype html><html lang="en"><head>'+head+'</head><body><header><a class="brand" href="physics-practice.html">Physics 11 <span>/ Practice Studio</span></a><a href="content.html">Browse chapters ↗</a></header><main style="max-width:850px">'+dialog
    monitor += '<section class="panel storage"><h3>Optional sync</h3><label for="monitor-key" class="small">Firebase API key</label><input id="monitor-key" type="password" autocomplete="off" placeholder="Use the same key as the student"><button id="monitor-connect" class="secondary" type="button">Connect to synced history</button><p class="small">Without sync, this page reads the student’s saved history on this device. It never writes student progress.</p></section></main>'
    monitor += embedded_script('physics-activity.js')+embedded_script('physics-monitor.js')+'</body></html>'
    (output_path.parent/'physics-monitor.html').write_text(monitor)
    print(f'Built {output_path.name}: {len(bank)} questions across {len(set(p["chapter"] for p in bank))} chapter(s).')
    return bank


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapters', type=Path, default=ROOT/'content/physics-practice-chapters.json')
    parser.add_argument('--output', type=Path, default=ROOT/'physics-practice.html')
    args = parser.parse_args()
    build(args.chapters, args.output)
