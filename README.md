# Mini Stack Q&A Platform

A lightweight Q&A platform similar to Stack Overflow, built with Flask and SQLAlchemy.

## Features

- User registration and authentication
- Ask and answer questions
- Tag-based question categorization
- Search functionality
- Upvote answers
- Responsive web interface

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Database**: PostgreSQL (with SQLite fallback)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS
- **Deployment**: Gunicorn

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mini-stack1
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://username:password@localhost/dbname
   ```
   For SQLite (default), you can omit DATABASE_URL.

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## Usage

- Register a new account or login
- Ask questions with tags
- Browse and search questions
- Provide answers to questions
- Upvote helpful answers

## Project Structure

```
mini-stack1/
├── app.py              # Main Flask application
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── test_db_config.py   # Database configuration tests
├── static/             # Static files (CSS, JS)
├── templates/          # HTML templates
├── instance/           # Database files
└── __pycache__/        # Python cache
```

## Database Models

- **User**: User accounts with authentication
- **Question**: Questions with title, body, and tags
- **Answer**: Answers to questions with upvote system
- **Tag**: Question categorization tags

## API Endpoints

- `GET /` - Home page with question list
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout
- `GET/POST /ask` - Ask a new question
- `GET /question/<id>` - View specific question
- `POST /question/<id>/answer` - Answer a question
- `POST /answer/<id>/upvote` - Upvote an answer

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
