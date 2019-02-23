
import unittest
from phv_eng import *

class TestParse(unittest.TestCase):

    def setUp(self):
        self.model = Model(123)
        self.assertEqual(True, self.model.load("phv.lang"))

    def test_nb_forms(self):
        self.assertEqual(NB_FORMS, 5)

    def test_modes(self):
        m = Model()
        self.assertEqual(m.mode(), NONE)
        m.parse(VERBS_LINE)
        self.assertEqual(m.mode(), VERBS)
        m.parse(TEXT_LINE)
        self.assertEqual(m.mode(), TEXT)
        m.parse(VERBS_LINE.upper())
        self.assertEqual(m.mode(), VERBS)
        m.parse(TEXT_LINE.upper())
        self.assertEqual(m.mode(), TEXT)

    def test_comments(self):
        m = Model()
        self.assertEqual(m.simplify("abc"), "abc")
        self.assertEqual(m.simplify("abc #def"), "abc")
        self.assertEqual(m.simplify("  #abc"), "")
        self.assertEqual(m.simplify("   abc #def #fgh"), "abc")

    def test_verbs(self):
        m = Model()
        m.parse(VERBS_LINE)
        m.parse("give given g g g        up out")
        self.assertEqual(m.verbs(), ['give out', 'give up'])
    
    def test_parse(self):
        m = Model()
        m.parse(VERBS_LINE)
        m.parse("give gives giving gave given         up out")
        m.parse(TEXT_LINE)
        e = m.parsePhrase("If you give up something, you stop doing it or having it.")
        self.assertEqual(e.question, "If you ... something, you stop doing it or having it.")
        self.assertEqual(e.answer, "give up")

    def test_unexisting_file(self):
        self.assertEqual(Model().load("some"), False)

    def test_parseFile(self):
        self.assertEqual(self.model.nbExercises(), 45)

    def test_randomEx(self):
        e = self.model.randomEx()
        self.assertEqual(e.question, "After a fruitless morning sitting at his desk he had ....")
        self.assertEqual(e.answer, "given up")
        self.assertEqual(self.model.findSimilar(e.answer), ['given out', 'taken up'])



if __name__ == '__main__':
    unittest.main()
