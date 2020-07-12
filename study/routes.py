import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from study import app,db,bcrypt
from study.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from study.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'subject': 'Mathematics',
        'topic': 'Trigonometry',
        'title': 'Multiple And Submultiple Angles',
        'author': 'Swikarya Dahal',
        'date': 'Apr 20, 2020',
        'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed velit mauris, ultrices ut ultrices a, elementum et libero. Nullam felis enim, dictum semper mauris in, vulputate dapibus elit. Nunc vestibulum magna vel arcu dapibus dapibus. Nunc tempor placerat diam interdum fermentum. Ut sit amet porta justo, sed feugiat erat. Curabitur fermentum venenatis tincidunt. Nulla accumsan bibendum ex, at varius lectus venenatis sit amet. Vivamus sed elit at lorem interdum tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in nulla sit amet ante ornare ultricies efficitur vel justo. Aenean quis consequat libero. Phasellus gravida, ipsum id sollicitudin rutrum, sem magna tincidunt dui, at consequat magna lacus in massa. """
    },
    {
        'subject': 'English',
        'topic': 'Nouns',
        'title': 'Modal Verbs',
        'author': 'Anwesh Dahal',
        'date': 'Apr 20, 2020',
        'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed velit mauris, ultrices ut ultrices a, elementum et libero. Nullam felis enim, dictum semper mauris in, vulputate dapibus elit. Nunc vestibulum magna vel arcu dapibus dapibus. Nunc tempor placerat diam interdum fermentum. Ut sit amet porta justo, sed feugiat erat. Curabitur fermentum venenatis tincidunt. Nulla accumsan bibendum ex, at varius lectus venenatis sit amet. Vivamus sed elit at lorem interdum tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in nulla sit amet ante ornare ultricies efficitur vel justo. Aenean quis consequat libero. Phasellus gravida, ipsum id sollicitudin rutrum, sem magna tincidunt dui, at consequat magna lacus in massa. """
    },
    {
        'subject': 'Physics',
        'topic': 'Thermodynamics',
        'title': 'First Law of Thermodynamics',
        'author': 'Lisa Lisa',
        'date': 'Apr 20, 2020',
        'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed velit mauris, ultrices ut ultrices a, elementum et libero. Nullam felis enim, dictum semper mauris in, vulputate dapibus elit. Nunc vestibulum magna vel arcu dapibus dapibus. Nunc tempor placerat diam interdum fermentum. Ut sit amet porta justo, sed feugiat erat. Curabitur fermentum venenatis tincidunt. Nulla accumsan bibendum ex, at varius lectus venenatis sit amet. Vivamus sed elit at lorem interdum tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in nulla sit amet ante ornare ultricies efficitur vel justo. Aenean quis consequat libero. Phasellus gravida, ipsum id sollicitudin rutrum, sem magna tincidunt dui, at consequat magna lacus in massa. """
    },
    {
        'subject': 'Chemistry',
        'topic': 'Inorganic Chemistry',
        'title': 'Nitrogen And Its Compounds',
        'author': 'Deek Gravie',
        'date': 'Apr 20, 2020',
        'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed velit mauris, ultrices ut ultrices a, elementum et libero. Nullam felis enim, dictum semper mauris in, vulputate dapibus elit. Nunc vestibulum magna vel arcu dapibus dapibus. Nunc tempor placerat diam interdum fermentum. Ut sit amet porta justo, sed feugiat erat. Curabitur fermentum venenatis tincidunt. Nulla accumsan bibendum ex, at varius lectus venenatis sit amet. Vivamus sed elit at lorem interdum tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in nulla sit amet ante ornare ultricies efficitur vel justo. Aenean quis consequat libero. Phasellus gravida, ipsum id sollicitudin rutrum, sem magna tincidunt dui, at consequat magna lacus in massa. """
    },
    {
        'subject': 'Chemistry',
        'topic': 'Physical Chemistry',
        'title': 'Rutherford\'s Atomic Model',
        'author': 'Mike Oxlong',
        'date': 'Apr 20, 2020',
        'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed velit mauris, ultrices ut ultrices a, elementum et libero. Nullam felis enim, dictum semper mauris in, vulputate dapibus elit. Nunc vestibulum magna vel arcu dapibus dapibus. Nunc tempor placerat diam interdum fermentum. Ut sit amet porta justo, sed feugiat erat. Curabitur fermentum venenatis tincidunt. Nulla accumsan bibendum ex, at varius lectus venenatis sit amet. Vivamus sed elit at lorem interdum tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in nulla sit amet ante ornare ultricies efficitur vel justo. Aenean quis consequat libero. Phasellus gravida, ipsum id sollicitudin rutrum, sem magna tincidunt dui, at consequat magna lacus in massa. """
    },
    {
        'subject': 'Biology',
        'topic': 'Zoology',
        'title': 'Vertibrates',
        'author': 'Anwesh Dahal',
        'date': 'Apr 20, 2020',
        'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed velit mauris, ultrices ut ultrices a, elementum et libero. Nullam felis enim, dictum semper mauris in, vulputate dapibus elit. Nunc vestibulum magna vel arcu dapibus dapibus. Nunc tempor placerat diam interdum fermentum. Ut sit amet porta justo, sed feugiat erat. Curabitur fermentum venenatis tincidunt. Nulla accumsan bibendum ex, at varius lectus venenatis sit amet. Vivamus sed elit at lorem interdum tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in nulla sit amet ante ornare ultricies efficitur vel justo. Aenean quis consequat libero. Phasellus gravida, ipsum id sollicitudin rutrum, sem magna tincidunt dui, at consequat magna lacus in massa. """
    },
    {
        'subject': 'English',
        'topic': 'Composition',
        'title': 'Letter Writing',
        'author': 'Anwesh Dahal',
        'date': 'Apr 20, 2020',
        'content': """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed velit mauris, ultrices ut ultrices a, elementum et libero. Nullam felis enim, dictum semper mauris in, vulputate dapibus elit. Nunc vestibulum magna vel arcu dapibus dapibus. Nunc tempor placerat diam interdum fermentum. Ut sit amet porta justo, sed feugiat erat. Curabitur fermentum venenatis tincidunt. Nulla accumsan bibendum ex, at varius lectus venenatis sit amet. Vivamus sed elit at lorem interdum tincidunt. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc in nulla sit amet ante ornare ultricies efficitur vel justo. Aenean quis consequat libero. Phasellus gravida, ipsum id sollicitudin rutrum, sem magna tincidunt dui, at consequat magna lacus in massa. """
    },
]


@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('static', filename='profile_pics/' + 'default.png')
    return render_template('home.html', title='Home', posts=posts, image_file=image_file)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered.', 'alt')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created and can now Sign In!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            flash(f"You have successfully logged in as { user.username }", "success")
            return redirect(next_page) if next_page else redirect(url_for('home'))
            
        else:
            flash("Login unsuccessful. Check your email and password", "danger")
    return render_template('login.html', title = 'Sign Up', form = form)

@app.route('/subject')
def subject():
    return render_template('subject.html', title='Home', posts=posts)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def newnote():
    form = PostForm()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("addNote.html", title="New Note", image_file=image_file)

@app.route("/logout")
def logout():
    logout_user()
    flash(f"You have logged out of your account", 'alt')
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file = image_file, posts=posts)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, fext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + fext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (410.566,410.566)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/update", methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("update.html", title="Update Info", form=form)
