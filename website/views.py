from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Course
from .init import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template('index.html')


@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.index'))
    return render_template('signup.html')

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                print('incorrect password')
        else:
            flash('Email does not exist.', category='error')
            print('email does not exist')
    return render_template('login.html')

@views.route('/home')
@login_required
def home():
    if current_user.role == 'admin':
        courses = Course.query.filter_by(owner=current_user).all()
        return render_template('admin.html',user=current_user,courses=courses)
    return render_template('home.html',user=current_user)


@views.route('/createcourse', methods=['GET', 'POST'])
@login_required
def createcourse():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', category='error')
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image=request.form.get('image')
        duration = request.form.get('duration')
        level = request.form.get('level')
        price = request.form.get('price')
        language = request.form.get('language')
        tags = request.form.get('tags')

        # Create a new course
        new_course = Course(
            title=title,
            description=description,
            image=image,
            duration=duration,
            level=level,
            price=price,
            language=language,
            tags=tags,
            owner=current_user
        )

        db.session.add(new_course)
        db.session.commit()

        flash('Course created successfully!', category='success')
        return redirect(url_for('views.home'))

    return render_template('createcourse.html')

@views.route('/editcourse/<int:course_id>', methods=['GET', 'POST'])
@login_required
def editcourse(course_id):
    course= Course.query.get(course_id)
    return render_template('editcourse.html',course=course)


# Edit Title Route
@views.route('/edit_title/<int:course_id>', methods=['POST'])
@login_required
def edittitle(course_id):
    course = Course.query.get(course_id)
    course.title = request.form['title']
    db.session.commit()
    return redirect(url_for('editcourse', course_id=course.id))

# Edit Description Route
@views.route('/edit_description/<int:course_id>', methods=['POST'])
@login_required
def editdescription(course_id):
    course = Course.query.get(course_id)
    course.description = request.form['description']
    db.session.commit()
    return redirect(url_for('editcourse',course_id=course.id))

# Edit Duration Route
@views.route('/edit_duration/<int:course_id>', methods=['POST'])
@login_required
def editduration(course_id):
    course = Course.query.get(course_id)
    course.duration = int(request.form['duration'])
    db.session.commit()
    return redirect(url_for('editcourse',course_id=course_id))

# Edit Level Route
@views.route('/edit_level/<int:course_id>', methods=['POST'])
@login_required
def editlevel(course_id):
    course = Course.query.get(course_id)
    course.level = request.form['level']
    db.session.commit()
    return redirect(url_for('editcourse', course_id=course.id))

# Edit Language Route
@views.route('/edit_language/<int:course_id>', methods=['POST'])
@login_required
def editlanguage(course_id):
    course = Course.query.get(course_id)
    course.language = request.form['lanaguag']
    db.session.commit()
    return redirect(url_for('editcourse', course_id=course.id))