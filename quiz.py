import csv
import random

class Quiz:
    def __init__(self, csv_file):
        self.questions = self.load_questions(csv_file)
        self.score = 0
        self.correct_answers = []
        self.wrong_answers = []
        self.difficulty = "easy"

    def load_questions(self, csv_file):
        questions = {"easy": [], "medium": [], "hard": []}
        try:
            with open(csv_file, newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    difficulty = row["difficulty"].strip().lower()
                    question = {
                        "question": row["question"],
                        "options": [row["option1"], row["option2"], row["option3"], row["option4"]],
                        "correct": row["correct"],
                        "difficulty": difficulty
                    }
                    if difficulty in questions:
                        questions[difficulty].append(question)
                    else:
                        print(f"Warning: Difficulty level '{difficulty}' not recognized for question '{row['question']}'")
            print("Questions loaded:", {k: len(v) for k, v in questions.items()})  # Print count of questions by difficulty
        except Exception as e:
            print(f"Error loading questions: {e}")
        return questions

    def get_random_question(self, difficulty):
        if self.questions[difficulty]:  # Check if there are questions available for the difficulty level
            return random.choice(self.questions[difficulty])
        return None  # Return None if no questions are available

    def next_question(self, is_correct):
        # Adjust difficulty based on the previous answer
        if is_correct:
            self.score += 1
            if self.difficulty == "easy":
                self.difficulty = "medium"
            elif self.difficulty == "medium":
                self.difficulty = "hard"
        else:
            if self.difficulty == "hard":
                self.difficulty = "medium"
            elif self.difficulty == "medium":
                self.difficulty = "easy"

        # Select next question based on new difficulty
        question = self.get_random_question(self.difficulty)
        return question

    def check_answer(self, selected_option, correct_option):
        return selected_option == correct_option

    def add_wrong_answer(self, question, selected_option):
        self.wrong_answers.append((question, selected_option))

    def get_score_summary(self):
        return self.score, self.correct_answers, self.wrong_answers
