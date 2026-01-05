import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from models import db, User, Question, Answer, Tag, question_tags
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# ===== ROUTES =====

# Home
@app.route('/')
def home():
    search_query = request.args.get('q', '')
    tag_filter = request.args.get('tag', '')

    # Start with all questions
    query = Question.query

    # Search by keyword in title or body
    if search_query:
        query = query.filter(
            (Question.title.ilike(f'%{search_query}%')) |
            (Question.body.ilike(f'%{search_query}%'))
        )

    # Filter by tag
    if tag_filter:
        query = query.join(Question.tags).filter(Tag.name == tag_filter)

    # Order by newest
    questions = query.order_by(Question.created_at.desc()).all()

    # Get all tags for the tag cloud
    all_tags = Tag.query.all()

    return render_template('index.html', 
                           questions=questions, 
                           all_tags=all_tags,
                           search_query=search_query,
                           tag_filter=tag_filter)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))

        # Hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create new user
        new_user = User(username=username, email=email, password=hashed_password)
        
        with app.app_context():
            db.session.add(new_user)
            db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('home'))

# Ask a question
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if 'user_id' not in session:
        flash('You must be logged in to ask a question.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tag_names = request.form['tags']

        # Create question
        new_question = Question(
            title=title,
            body=body,
            user_id=session['user_id']
        )

        # Handle tags
        if tag_names:
            tag_list = [tag.strip() for tag in tag_names.split(',')]
            for tag_name in tag_list:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                new_question.tags.append(tag)

        db.session.add(new_question)
        db.session.commit()

        flash('Question posted successfully!')
        return redirect(url_for('home'))

    return render_template('ask.html')

# View a question
@app.route('/question/<int:question_id>')
def view_question(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question.html', question=question)

# Post an answer
@app.route('/answer/<int:question_id>', methods=['POST'])
def post_answer(question_id):
    if 'user_id' not in session:
        flash('You must be logged in to answer.')
        return redirect(url_for('login'))

    body = request.form['body']
    new_answer = Answer(
        body=body,
        user_id=session['user_id'],
        question_id=question_id
    )
    db.session.add(new_answer)
    db.session.commit()

    flash('Answer posted!')
    return redirect(url_for('view_question', question_id=question_id))

# Upvote an answer
@app.route('/upvote/<int:answer_id>', methods=['POST'])
def upvote_answer(answer_id):
    if 'user_id' not in session:
        flash('You must be logged in to upvote.')
        return redirect(url_for('login'))

    answer = Answer.query.get_or_404(answer_id)
    answer.upvotes += 1
    db.session.commit()

    flash('Upvoted!')
    return redirect(url_for('view_question', question_id=answer.question_id))

# About page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)