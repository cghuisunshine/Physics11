"""Check source fidelity, shared diagrams/data, and multi-chapter expansion."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from build_physics_practice import ROOT, Tree, load_bank


class PracticeBuilderTests(unittest.TestCase):
    def test_source_fidelity(self):
        bank = load_bank(ROOT/'content/physics-practice-chapters.json')
        registry = json.loads((ROOT/'content/physics-practice-chapters.json').read_text())
        self.assertEqual(len(bank), 180)
        self.assertEqual(len({q['id'] for q in bank}), 180)
        by_id = {q['id']: q for q in bank}
        for chapter in registry['chapters']:
            inventory = json.loads((ROOT/chapter['inventory']).read_text())
            questions = [q for q in bank if q['chapter'] == chapter['id']]
            self.assertEqual(len(questions), inventory['question_count'])
            self.assertEqual([q['number'] for q in questions], list(range(1, len(questions)+1)))
            for group in inventory['groups']:
                for source_question in group['questions']:
                    question = by_id[chapter['id']+'-'+source_question['id']]
                    self.assertEqual(question['solution'], source_question['answer_html'].strip())
                    self.assertEqual(question['url'], chapter['html']+'#'+source_question['id'])
                    tree = Tree(question['html'])
                    self.assertIsNotNone(tree.root.find(cls='question-image'))
                    for cls in ['shared', 'context']:
                        if group.get(cls):
                            self.assertIsNotNone(tree.root.find(cls=cls))
            self.assertTrue(any('<svg' in q['solution'] for q in questions))

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
            registry['chapters'].append({**registry['chapters'][0], 'id':'bc-ch4', 'number':4, 'title':'Dynamics', 'inventory':str(source)})
            config = directory/'chapters.json'
            config.write_text(json.dumps(registry))
            result = load_bank(config)
            self.assertEqual(len(result), len(original)+2)
            self.assertEqual(result[:len(original)], original)
            self.assertEqual([q['id'] for q in result[len(original):]], ['bc-ch4-q-1', 'bc-ch4-q-2'])
            self.assertEqual([q['number'] for q in result[len(original):]], [1, 2])
            registry['chapters'][-1]['id'] = 'bc-ch2'
            config.write_text(json.dumps(registry))
            with self.assertRaises(ValueError):
                load_bank(config)


if __name__ == '__main__':
    unittest.main()
