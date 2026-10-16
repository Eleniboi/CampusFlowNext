import os
import tempfile
import unittest

from campusflow.understanding_check import (
    QUESTIONS, normalize_choice, score_answers, run_understanding_check,
)

CORRECT = ["B", "C", "B", "C", "C", "B"]
SILENT = lambda *_: None


def scripted(inputs):
    items = list(inputs)
    def ask(prompt):
        return items.pop(0)
    return ask


class TestQuestionBank(unittest.TestCase):
    def test_six_questions_with_valid_answers(self):
        self.assertEqual(len(QUESTIONS), 6)
        for q in QUESTIONS:
            self.assertIn(q["answer"], q["options"])


class TestScoring(unittest.TestCase):
    def test_all_correct_scores_six(self):
        self.assertEqual(score_answers(QUESTIONS, CORRECT), 6)

    def test_all_wrong_scores_zero(self):
        self.assertEqual(score_answers(QUESTIONS, ["A", "A", "A", "A", "A", "A"]), 0)

    def test_missing_answers_count_as_wrong(self):
        self.assertEqual(score_answers(QUESTIONS, ["B", "C", "B"]), 3)

    def test_scorer_is_strict_about_case(self):
        self.assertEqual(score_answers(QUESTIONS, ["b"] + CORRECT[1:]), 5)


class TestInputHandling(unittest.TestCase):
    def test_normalize_accepts_lowercase_and_spaces(self):
        self.assertEqual(normalize_choice(" b "), "B")

    def test_normalize_rejects_other_input(self):
        for bad in ("E", "", "critical", "1"):
            self.assertIsNone(normalize_choice(bad))

    def test_invalid_choice_retries_until_valid(self):
        ask = scripted(["Z", "", "b", "C", "B", "C", "C", "B",
                        "Reject it and keep the data unchanged",
                        "Reject until reopened because resolved means closed"])
        score = run_understanding_check(ask=ask, out=SILENT)
        self.assertEqual(score, 6)


class TestFullRun(unittest.TestCase):
    def test_short_explanation_retries_and_note_is_saved(self):
        ask = scripted(CORRECT + ["short",
                                  "Reject it and keep the data unchanged",
                                  "Reject until reopened because resolved means closed"])
        with tempfile.TemporaryDirectory() as folder:
            note = os.path.join(folder, "notes.md")
            score = run_understanding_check(ask=ask, out=SILENT, note_path=note)
            with open(note, encoding="utf-8") as f:
                saved = f.read()
        self.assertEqual(score, 6)
        self.assertIn("Understanding check: 6/6", saved)
        self.assertIn("Q1: Reject it and keep the data unchanged", saved)


if __name__ == "__main__":
    unittest.main()