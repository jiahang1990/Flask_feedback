from flask import request, redirect, Flask, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback,  db, connect_db
from forms import RegisterForm, LoginForm, FeedbackForm
    
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///flask-feedback'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar=DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods =  ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.passward.data
        first_name = form.first_name.data 
        last_name = form.last_name.data 
        email = form.email.data 

        user = User.register(username, password, first_name, last_name, email)

        #db.session.add(user)
        session['username'] = user.username 
        db.session.commit()

        return redirect(f'/users/{username}')
    else:
        return render_template('users/register.html',form = form)

@app.route('/login', methods =  ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.passward.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username 
            return redirect(f'/users/{username}')
        else:
            return render_template('users/login.html',form = form)
    else:
        return render_template('users/login.html',form = form)

@app.route('/users/<username>')
def show(username):
    if (session.get('username')==username):
        user = User.query.filter_by(username=username).first()
        return render_template('users/show.html', user = user)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')

@app.route('/users/<username>/delete', methods = ['POST'])
def delete_user(username):
    if username == session.get('username'):
        user = User.query.filter_by(username = username).first()
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods = ['GET', 'POST'])
def add_feedback(username):
    if session.get('username')==username:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(
                title = title,
                content = content,
                username = username
            )
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('feedback/new.html', form = form)
    else:
        return redirect('/')

@app.route('/feedback/<int:feedback_id>/update', methods = ['GET', 'POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if session.get('username')!=feedback.username:
        return redirect('/')
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        feedback.title = title
        feedback.content = content
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        form.title.data = feedback.title
        form.content.data = feedback.content
        return render_template('feedback/edit.html', form = form)

@app.route('/feedback/<int:feedback_id>/delete', methods = ['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)
    if feedback.username == session.get('username'):
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')
    else:
        return redirect('/login')