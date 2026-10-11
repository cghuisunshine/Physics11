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
        inventory = json.loads((ROOT/'content/bc-kinematics-questions.json').read_text())
        self.assertEqual(len(bank), 101)
        self.assertEqual(len({q['id'] for q in bank}), 101)
        by_source = {q['sourceId']: q for q in bank}
        shared_count = context_count = graph_count = 0
        for group in inventory['groups']:
            for source_question in group['questions']:
                question = by_source[source_question['id']]
                self.assertEqual(question['solution'], source_question['answer_html'].strip())
                tree = Tree(question['html'])
                self.assertIsNotNone(tree.root.find(cls='question-image'))
                if group.get('shared'):
                    self.assertIsNotNone(tree.root.find(cls='shared'))
                    shared_count += 1
                if group.get('context'):
                    self.assertIsNotNone(tree.root.find(cls='context'))
                    context_count += 1
                if '<svg' in question['solution']:
                    graph_count += 1
        self.assertEqual(shared_count, 5)
        self.assertEqual(context_count, 9)
        self.assertGreater(graph_count, 0)

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
            registry['chapters'].append({**registry['chapters'][0], 'id':'bc-ch3', 'number':3, 'title':'Dynamics', 'inventory':str(source)})
            config = directory/'chapters.json'
            config.write_text(json.dumps(registry))
            result = load_bank(config)
            self.assertEqual(len(result), 103)
            self.assertEqual(result[:101], original)
            self.assertEqual([q['id'] for q in result[101:]], ['bc-ch3-q-1', 'bc-ch3-q-2'])
            self.assertEqual([q['number'] for q in result[101:]], [1, 2])
            registry['chapters'][1]['id'] = 'bc-ch2'
            config.write_text(json.dumps(registry))
            with self.assertRaises(ValueError):
                load_bank(config)


if __name__ == '__main__':
    unittest.main()
