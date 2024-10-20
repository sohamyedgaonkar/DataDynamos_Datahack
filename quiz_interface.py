import tkinter as tk
from tkinter import messagebox
from quiz import Quiz

class QuizApp:
    def __init__(self, root, quiz_file):
        self.root = root
        self.root.title("Quiz Application")
        self.quiz = Quiz(quiz_file)
        self.current_question = None
        self.current_question_index = 0
        self.score = 0
        self.incorrect_answers = []

        # Make the window full-screen
        self.root.attributes('-fullscreen', True)

        # Set background color
        self.root.configure(bg="#F0F8FF")

        # Start page with two options
        self.start_frame = tk.Frame(root, bg="#F0F8FF")
        self.start_frame.pack()

        self.start_button = tk.Button(self.start_frame, text="Start Quiz", command=self.start_quiz, bg="#4682B4", fg="white", font=("Arial", 14))
        self.start_button.pack(pady=20)

        self.upload_button = tk.Button(self.start_frame, text="Upload YouTube URL or PDF", command=self.upload, bg="#4682B4", fg="white", font=("Arial", 14))
        self.upload_button.pack(pady=20)

        # Quit button to exit the application
        self.quit_button = tk.Button(self.start_frame, text="Quit", command=self.root.quit, bg="#FF6347", fg="white", font=("Arial", 14))
        self.quit_button.pack(pady=20)

        # Quiz interface
        self.quiz_frame = tk.Frame(root, bg="#F0F8FF")

        self.question_label = tk.Label(self.quiz_frame, text="", wraplength=600, bg="#F0F8FF", font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.quiz_frame, text="", command=lambda i=i: self.submit_answer(i), bg="#87CEFA", font=("Arial", 12))
            button.pack(pady=5)
            self.option_buttons.append(button)

        # Ending page
        self.end_frame = tk.Frame(root, bg="#F0F8FF")

        self.score_label = tk.Label(self.end_frame, text="", bg="#F0F8FF", font=("Arial", 16, "bold"))
        self.score_label.pack(pady=20)

        self.wrong_answers_label = tk.Label(self.end_frame, text="", bg="#F0F8FF", font=("Arial", 12))
        self.wrong_answers_label.pack(pady=10)

        # Add "Back to Home" button
        self.home_button = tk.Button(self.end_frame, text="Back to Home", command=self.back_to_home, bg="#4682B4", fg="white", font=("Arial", 14))
        self.home_button.pack(pady=20)

    def start_quiz(self):
        self.start_frame.pack_forget()
        self.quiz_frame.pack()
        self.current_question_index = 0  # Reset the question index
        self.next_question()

    def next_question(self):
        if self.current_question_index >= 10:
            self.end_quiz()
            return
        
        # If there is a current question, check the answer
        if self.current_question is not None:
            is_correct = self.quiz.check_answer(self.selected_option, self.current_question["correct"])
            if is_correct:
                self.score += 1
            else:
                self.incorrect_answers.append({
                    "question": self.current_question["question"],
                    "correct": self.current_question["correct"]
                })
        
        # Get the next question based on user's performance
        self.current_question = self.quiz.next_question(is_correct)

        # Check if a question was returned (to avoid NoneType errors)
        if self.current_question is not None:
            self.display_question(self.current_question)
            self.current_question_index += 1  # Increment the question index
        else:
            messagebox.showinfo("Quiz Finished", "No more questions available.")
            self.end_quiz()

    def display_question(self, question):
        # Add the difficulty level in brackets next to the question
        self.question_label.config(text=f"{question['question']} (Difficulty: {question['difficulty'].capitalize()})")
        for i, option in enumerate(question["options"]):
            self.option_buttons[i].config(text=option)

    def submit_answer(self, option_index):
        self.selected_option = self.current_question["options"][option_index]
        self.next_question()  # Automatically go to the next question

    def end_quiz(self):
        self.quiz_frame.pack_forget()
        self.end_frame.pack()

        # Display final score
        self.score_label.config(text=f"Your Score: {self.score}/10")

        # Display only the wrong answers and the correct options
        if self.incorrect_answers:
            wrongs = "\n".join([f"Q: {q['question']} | Correct Answer: {q['correct']}" for q in self.incorrect_answers])
            self.wrong_answers_label.config(text="Incorrect Answers:\n" + wrongs)
        else:
            self.wrong_answers_label.config(text="You answered all questions correctly!")

    def back_to_home(self):
        self.end_frame.pack_forget()
        self.start_frame.pack()

        # Reset quiz parameters for a fresh start
        self.current_question_index = 0
        self.score = 0
        self.incorrect_answers = []

    def upload(self):
        messagebox.showinfo("Upload", "Upload functionality is ready!")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root, "questions.csv")
    root.mainloop()
