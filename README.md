# DataDynamos CSV Quiz

Flask application that serves a quiz based on questions loaded from `utils/quiz_questions.csv`. The app includes an HTML interface, quiz helpers, and JSON endpoints for fetching an individual question or a quiz.

## API

- `GET /api/question`
- `GET /api/quiz`

Install Flask and the packages imported by the project, then start the application with `python app.py`. Keep the CSV at the path expected by `app.py`.
