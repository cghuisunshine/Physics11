"""Check source fidelity, shared diagrams/data, and multi-chapter expansion."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from html import unescape
from build_physics_practice import ROOT, Tree, clean_fragment, load_bank


class PracticeBuilderTests(unittest.TestCase):
    def test_fragment_checks_attribute_names(self):
        image = '<img src="data:image/webp;base64,+oNyUCAA==" alt="Image">'
        self.assertEqual(clean_fragment(image), image)
        for unsafe in ('<script>alert(1)</script>', '<img onload="alert(1)">',
                       '<svg><g onload="alert(1)"></g></svg>'):
            with self.assertRaises(ValueError):
                clean_fragment(unsafe)

    def test_source_fidelity(self):
        bank = load_bank(ROOT/'content/physics-practice-chapters.json')
        registry = json.loads((ROOT/'content/physics-practice-chapters.json').read_text())
        self.assertEqual(len(bank), 824)
        self.assertEqual(len({q['id'] for q in bank}), 824)
        self.assertEqual(next(q['topicTitle'] for q in bank if q['topic'] == 'Ch 3 · 3.3'), "3.3 Hooke's law")
        by_id = {q['id']: q for q in bank}
        for chapter in registry['chapters']:
            inventory = json.loads((ROOT/chapter['inventory']).read_text())
            questions = [q for q in bank if q['chapter'] == chapter['id']]
            source_tree = Tree((ROOT/chapter['html']).read_text())
            titles = {o.attrs['value']: unescape(source_tree.inner(o))
                      for o in source_tree.root.find(id='topic').children if o.attrs.get('value')}
            self.assertEqual(len(questions), inventory['question_count'])
            self.assertEqual([q['number'] for q in questions], list(range(1, len(questions)+1)))
            for group in inventory['groups']:
                for source_question in group['questions']:
                    question = by_id[chapter['id']+'-'+source_question['id']]
                    self.assertEqual(question['solution'], source_question['answer_html'].strip())
                    self.assertEqual(question['url'], chapter['html']+'#'+source_question['id'])
                    self.assertEqual(question['topic'], f'Ch {chapter["number"]} · {group["topic"]}')
                    self.assertEqual(question['topicTitle'], titles[group['topic']])
                    tree = Tree(question['html'])
                    self.assertIsNotNone(tree.root.find(cls='question-image'))
                    for cls in ['shared', 'context']:
                        if group.get(cls):
                            self.assertIsNotNone(tree.root.find(cls=cls))
            self.assertTrue(any('<svg' in q['solution'] for q in questions))

    def test_energy_reference_context(self):
        bank = load_bank(ROOT/'content/physics-practice-chapters.json')
        energy = {q['sourceId']: q for q in bank if q['chapter'] == 'bc-ch5'}
        self.assertEqual(len(energy), 144)
        self.assertEqual({q['chapterNumber'] for q in energy.values()}, {5})
        self.assertEqual({q['chapterTitle'] for q in energy.values()}, {'Energy'})
        self.assertEqual({q['topic'] for q in energy.values()}, {
            'Ch 5 · 5.1', 'Ch 5 · 5.2', 'Ch 5 · 5.3', 'Ch 5 · 5.4',
            'Ch 5 · Chapter review', 'Ch 5 · Extra practice'})
        for source_id in ['q-11', 'q-59', 'q-63', 'q-88']:
            self.assertIsNotNone(Tree(energy[source_id]['html']).root.find(cls='context'))
        for source_id in ['q-77', 'q-92', 'q-127', 'q-128']:
            self.assertIsNotNone(Tree(energy[source_id]['html']).root.find(cls='shared'))
        self.assertIn('25 cm above the bottom', energy['q-110']['solution'])
        self.assertEqual(energy['q-144']['url'], 'bc-energy-questions.html#q-144')

    def test_add_chapter_without_changing_existing_ids(self):
        registry = json.loads((ROOT/'content/physics-practice-chapters.json').read_text())
        original = load_bank(ROOT/'content/physics-practice-chapters.json')
        inventory = json.loads((ROOT/'content/bc-kinematics-questions.json').read_text())
        # A chapter with two question entries, not a fixed 25- or 101-entry set.
        future = copy.deepcopy(inventory)
        future['groups'] = future['groups'][:2]
        future['question_count'] = 2
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            source = directory/'future.json'
            source.write_text(json.dumps(future))
            registry['chapters'].append({**registry['chapters'][0], 'id':'test-chapter', 'number':99, 'title':'Test chapter', 'inventory':str(source)})
            config = directory/'chapters.json'
            config.write_text(json.dumps(registry))
            result = load_bank(config)
            self.assertEqual(len(result), len(original)+2)
            self.assertEqual(result[:len(original)], original)
            self.assertEqual([q['id'] for q in result[len(original):]], ['test-chapter-q-1', 'test-chapter-q-2'])
            self.assertEqual([q['number'] for q in result[len(original):]], [1, 2])
            registry['chapters'][-1]['id'] = 'bc-ch2'
            config.write_text(json.dumps(registry))
            with self.assertRaises(ValueError):
                load_bank(config)


if __name__ == '__main__':
    unittest.main()
