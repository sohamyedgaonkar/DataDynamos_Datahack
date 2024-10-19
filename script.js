// Sample questions array
const questions = [
    {
        question: "What is the capital of France?",
        options: ["Berlin", "Madrid", "Paris", "Rome"],
        correctAnswer: 2
    },
    {
        question: "What is 2 + 2?",
        options: ["3", "4", "5", "6"],
        correctAnswer: 1
    },
    {
        question: "Who wrote 'Hamlet'?",
        options: ["Charles Dickens", "William Shakespeare", "Mark Twain", "J.K. Rowling"],
        correctAnswer: 1
    },
    {
        question: "Which planet is known as the Red Planet?",
        options: ["Earth", "Mars", "Jupiter", "Venus"],
        correctAnswer: 1
    },
    {
        question: "What is the speed of light?",
        options: ["300,000 km/s", "150,000 km/s", "450,000 km/s", "500,000 km/s"],
        correctAnswer: 0
    }
];

let currentQuestion = 0;
let score = 0;
let attempts = 0; // Track the number of attempts
let incorrectQuestions = [];

// Load the first question
function loadQuestion() {
    const questionElement = document.getElementById("question");
    const options = document.querySelectorAll(".option");

    questionElement.textContent = questions[currentQuestion].question;
    options.forEach((button, index) => {
        button.textContent = questions[currentQuestion].options[index];
        button.classList.remove("correct", "wrong");
        button.disabled = false;
    });

    document.getElementById("result").textContent = '';
    document.getElementById("attempts-result").textContent = ''; // Clear the attempts result initially
}

// Handle option selection with flashcard flip effect
function selectOption(selectedOption) {
    const correctAnswer = questions[currentQuestion].correctAnswer;
    const options = document.querySelectorAll(".option");

    // Increment the attempts count
    attempts++;

    // Mark correct or wrong
    if (selectedOption === correctAnswer) {
        options[selectedOption].classList.add("correct");
        score++;
    } else {
        options[selectedOption].classList.add("wrong");
        options[correctAnswer].classList.add("correct");
        incorrectQuestions.push(questions[currentQuestion]); // Store incorrect questions
    }

    // Disable all options after selection
    options.forEach(button => button.disabled = true);

    // Add flip effect to the flashcard
    document.getElementById('flashcard').classList.add('flip');

    // Move to next question after 1 second
    setTimeout(() => {
        document.getElementById('flashcard').classList.remove('flip');
        currentQuestion++;
        if (currentQuestion < questions.length) {
            loadQuestion();
        } else {
            if (incorrectQuestions.length > 0) {
                reAskIncorrectQuestions();
            } else {
                showResult();
            }
        }
    }, 1000);
}

// Re-ask the incorrect questions
function reAskIncorrectQuestions() {
    questions.length = 0;
    questions.push(...incorrectQuestions);
    incorrectQuestions.length = 0;
    currentQuestion = 0;
    score = 0;
    loadQuestion();
}

// Show the result at the end
function showResult() {
    document.getElementById("quiz-container").innerHTML = `
        <h2>Your score: ${score} out of ${questions.length}</h2>
        <h3>Total attempts: ${attempts}</h3> <!-- Display the total attempts -->
        <button onclick="restartQuiz()">Restart Quiz</button>
    `;
}

// Restart the quiz
function restartQuiz() {
    location.reload();
}

// Start the quiz
loadQuestion();
