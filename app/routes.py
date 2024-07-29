from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from app.models import Post, MemorySection, Memory, User  # Asegúrate de que la ruta al modelo sea correcta
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from app import db  # Asegúrate de que esto está importado si estás usando SQLAlchemy para la base de datos

main = Blueprint('main', __name__)

# PRINCIPAL ROUTES

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/goals_and_services')
def goalsServices():
    posts = Post.get_posts_by_section("goals_and_services")
    return render_template("display_posts.html", title="Goals and Services", posts=posts)

@main.route('/next_mission_trip')
def nextMission():
    posts = Post.get_posts_by_section('next_mission')
    return render_template("display_posts.html", title="Next Mission Trip", posts=posts)

@main.route('/how_to_help')
def howToHelp():
    posts = Post.get_posts_by_section('how_to_help')
    return render_template("display_posts.html", title="How to Help", posts=posts)

@main.route('/contact_us')
def contactUs():
    posts = Post.get_posts_by_section('contact_us')
    return render_template("display_posts.html", title="Contact Us", posts=posts)

@main.route('/photos_videos')
def photoVideos():
    memory_sections = MemorySection.query.all()
    return render_template("display_memory_sections.html", title="Photos and Videos", memory_sections=memory_sections)

@main.route('/photos_videos/<int:section_id>')
def photos_videos_section(section_id):
    memories = Memory.query.filter_by(section_id=section_id).all()
    return render_template("display_memories.html", title="Photos and Videos", memories=memories)

@main.route('/terms_and_conditions')
def termsAndConditions():
    posts = Post.get_posts_by_section('terms_and_conditions')
    return render_template('display_posts.html', title="Terms and Conditions", posts=posts)

@main.route('/about_peru')
def aboutPeru():
    return render_template('about_peru.html')

@main.route('/previous_missions')
def previousMissions():
    posts = Post.get_posts_by_section('previous_missions')
    return render_template("display_posts.html", title="Previous Missions", posts=posts)

# BLOCK MANAGERS

@main.route('/create_block', methods=['GET', 'POST'])
@login_required
def create_block():
    if request.method == 'POST':
        section = request.form['section']
        title = request.form.get('title', '')
        subtitle = request.form.get('subtitle', '')
        content = request.form.get('content', '')
        image = request.files.get('image')

        if not section:
            flash('Section is required.')
            return render_template('create_block.html', error='Section is required.')

        if not title and not subtitle and not content and not image:
            flash('At least one of Title, Subtitle, Content, or Image is required.')
            return render_template('create_block.html', error='At least one of Title, Subtitle, Content, or Image is required.')

        image_filename = None
        if image:
            image_filename = secure_filename(image.filename)
            print(image_filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename))

        # Aquí puedes guardar el bloque en la base de datos
        new_block = Post(section=section, title=title, subtitle=subtitle, content=content, image=image_filename, user_id=current_user.id)
        db.session.add(new_block)
        db.session.commit()

        flash('Block created successfully!')
        return redirect(url_for('main.create_block'))  # Redirige a la misma página o a otra según tu lógica

    return render_template('block_form.html')

@main.route('/add_section', methods=['GET', 'POST'])
@login_required
def addSection():
    return render_template('section_form.html')

@main.route('/add_image_or_video', methods=['GET', 'POST'])
@login_required
def addImageOrVideo():
    return render_template('memory_form.html')

# SESSION MANAGERS

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Check your email and password.')
    return render_template('login.html')

# Vista de Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
