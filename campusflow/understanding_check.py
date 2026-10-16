"""Engineering Understanding Check: question bank, scoring and quiz flow.

The question bank is data only. Scoring is pure. Input and output are
passed in as functions so the quiz can be tested without typing.
"""

QUESTIONS = [
    {
        "text": "Ticket T001 is open and unassigned. A user tries to move it to in_progress.",
        "options": {"A": "Accept", "B": "Reject and preserve all data",
                    "C": "Resolve it automatically", "D": "Remove ticket"},
        "answer": "B",
    },
    {
        "text": "The app has zero tickets. What should resolution percentage display?",
        "options": {"A": "Crash", "B": "100%", "C": "0%",
                    "D": "Divide by one without explanation"},
        "answer": "C",
    },
    {
        "text": "Filter title='wifi', category='Network', status='open'. Which records should match?",
        "options": {"A": "Any record matching one filter",
                    "B": "Only records matching all supplied filters",
                    "C": "All network records", "D": "All open records"},
        "answer": "B",
    },
    {
        "text": "A resolved ticket receives 'Add note'. What should happen?",
        "options": {"A": "Append anyway", "B": "Delete old notes",
                    "C": "Reject until reopened", "D": "Change status silently"},
        "answer": "C",
    },
    {
        "text": "The JSON file includes two tickets with the same ID. What should load do?",
        "options": {"A": "Keep both", "B": "Replace memory with duplicates",
                    "C": "Reject the load without changing current memory",
                    "D": "Rename IDs silently"},
        "answer": "C",
    },
    {
        "text": "A PR changes validation but has no negative-case tests. Best review action?",
        "options": {"A": "Approve because it runs",
                    "B": "Request focused tests and reasoning",
                    "C": "Merge immediately", "D": "Ask AI to approve it"},
        "answer": "B",
    },
]

VALID_CHOICES = ("A", "B", "C", "D")
EXPLAIN_NUMBERS = (1, 4)     # the two questions the learner must explain
MIN_EXPLANATION = 20         # characters


def normalize_choice(text):
    """Return 'A'-'D' for valid input (any case, spaces ignored), else None."""
    cleaned = text.strip().upper()
    return cleaned if cleaned in VALID_CHOICES else None


def score_answers(questions, answers):
    """Count exact matches. Missing answers count as wrong. No case conversion here."""
    score = 0
    for index, question in enumerate(questions):
        if index < len(answers) and answers[index] == question["answer"]:
            score += 1
    return score


def ask_question(question, number, ask, out):
    out(f"\nQ{number}. {question['text']}")
    for letter, option in question["options"].items():
        out(f"  {letter}. {option}")
    while True:
        choice = normalize_choice(ask("Your answer (A/B/C/D): "))
        if choice:
            return choice
        out("Invalid choice. Enter A, B, C, or D.")


def collect_answers(questions, ask, out):
    return [ask_question(q, n, ask, out) for n, q in enumerate(questions, start=1)]


def collect_explanations(numbers, ask, out):
    explanations = {}
    for number in numbers:
        while True:
            text = ask(f"Explain your answer to Q{number} in your own words "
                       f"(at least {MIN_EXPLANATION} characters): ").strip()
            if len(text) >= MIN_EXPLANATION:
                explanations[number] = text
                break
            out(f"Please write at least {MIN_EXPLANATION} characters.")
    return explanations


def save_learning_note(path, score, total, answers, explanations):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n## Understanding check: {score}/{total}\n")
        f.write(f"Answers: {', '.join(answers)}\n\n")
        for number, text in sorted(explanations.items()):
            f.write(f"Q{number}: {text}\n\n")


def run_understanding_check(questions=QUESTIONS, ask=input, out=print, note_path=None):
    answers = collect_answers(questions, ask, out)
    score = score_answers(questions, answers)
    out(f"\nFinal score: {score} / {len(questions)}")
    explanations = collect_explanations(EXPLAIN_NUMBERS, ask, out)
    if note_path:
        save_learning_note(note_path, score, len(questions), answers, explanations)
    return score