from flask import Flask, jsonify, render_template, request
import csv
import random

app = Flask(__name__)

# Load questions from CSV file with specified encoding
def load_questions():
    questions = []
    with open('utils/quiz_questions.csv', mode='r', encoding='utf-8', errors='replace') as file:
        reader = csv.DictReader(file)
        for row in reader:
            questions.append({
                'text': row['question'],
                'options': [row['option1'], row['option2'], row['option3'], row['option4']],
                'correctAnswer': row['correctAnswer'],
                'difficulty': row['difficulty']
            })
    return questions

questions = load_questions()

difficulty_order = ['Easy', 'Medium', 'Hard']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question', methods=['GET'])
def get_question():
    current_difficulty = request.args.get('difficulty', 'Easy')
    filtered_questions = [q for q in questions if q['difficulty'] == current_difficulty]
    
    if not filtered_questions:
        return jsonify({'error': 'No more questions available'}), 404

    question = random.choice(filtered_questions)
    return jsonify(question)

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    return jsonify({'questions': questions[:10]})  # Return the first 10 questions

if __name__ == '__main__':
    app.run(debug=True)

