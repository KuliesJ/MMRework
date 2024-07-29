from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from app.models import Post, MemorySection, Memory, User, MemorySection, Memory  # Asegúrate de que la ruta al modelo sea correcta
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from app import db  # Asegúrate de que esto está importado si estás usando SQLAlchemy para la base de datos

main = Blueprint('main', __name__)

# ODDITIES

@main.app_errorhandler(404)
def not_found(error):
    return render_template('not_found.html'), 404

# PRINCIPAL ROUTES

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/goals_and_services')
def goalsServices():
    posts = Post.get_posts_by_section('goals_and_services')
    print(posts)
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
    print(memories)
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
@main.route('/create_block/<int:post_id>', methods=['GET', 'POST'])
@login_required
def create_block(post_id=None):
    post = None
    if post_id:
        post = Post.query.get(post_id)

    if request.method == 'POST':
        section = request.form['section']
        title = request.form.get('title', '')
        subtitle = request.form.get('subtitle', '')
        content = request.form.get('content', '')
        image = request.files.get('image')

        if not section:
            flash('Section is required.')
            return render_template('create_block.html', post=post, error='Section is required.')

        if not title and not subtitle and not content and not image:
            flash('At least one of Title, Subtitle, Content, or Image is required.')
            return render_template('create_block.html', post=post, error='At least one of Title, Subtitle, Content, or Image is required.')

        image_filename = post.image if post and post.image else None
        if image:
            image_filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image.save(image_path)

        if post:
            post.section = section
            post.title = title
            post.subtitle = subtitle
            post.content = content
            post.image = image_filename
        else:
            # Obtener el valor máximo actual de 'order' en la sección
            max_order = db.session.query(db.func.max(Post.order)).filter_by(section=section).scalar()
            new_order = (max_order or 0) + 1

            post = Post(section=section, title=title, subtitle=subtitle, content=content, image=image_filename, user_id=current_user.id, order=new_order)
            db.session.add(post)

        db.session.commit()
        flash('Block created successfully!' if not post_id else 'Block updated successfully!')
        return redirect(url_for('main.create_block'))

    return render_template('block_form.html', post=post)


@main.route('/editPosts', methods=['POST'])
@login_required
def editPosts():
    post_id = request.form.get('post_id')
    action = request.form.get('action')
    post = Post.query.get(post_id)

    if not post:
        flash('Post not found.')
        return redirect(url_for('main.home'))

    if action == 'delete':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!')

    elif action in ['move_up', 'move_down']:
        current_order = post.order
        section = post.section

        if action == 'move_up':
            new_order = current_order - 1
        elif action == 'move_down':
            new_order = current_order + 1

        # Find the post to swap with
        other_post = Post.query.filter_by(section=section, order=new_order).first()

        if other_post:
            # Swap orders
            post.order = new_order
            other_post.order = current_order
            db.session.commit()
            flash(f'Post {action.replace("_", " ")} successfully!')
        else:
            flash(f'Cannot {action.replace("_", " ")}. No post to swap with.')

    return redirect(request.referrer or url_for('main.home'))



@main.route('/add_section', methods=['GET', 'POST'])
@login_required
def addSection():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()

        if not title:
            flash('Section name is required.')
            return render_template('create_block.html', error='Section name is required.')

        # Verificar si la sección ya existe
        existing_section = MemorySection.query.filter_by(sectionName=title).first()
        if existing_section:
            flash('Section already exists.')
            return render_template('create_block.html', error='Section already exists.')

        # Crear una nueva sección
        new_section = MemorySection(sectionName=title)
        db.session.add(new_section)
        db.session.commit()

        flash('Section created successfully!')
        return redirect(url_for('main.home'))

    return render_template('section_form.html')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/add_image_or_video', methods=['GET', 'POST'])
def add_image_or_video():
    if request.method == 'POST':
        file = request.files.get('image')
        section_id = request.form.get('section_id')
        
        if not section_id:
            flash('Section ID is required.')
            return redirect(url_for('main.add_image_or_video'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Determinar el tipo de archivo
            file_type = 'image' if filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'} else 'video'
            
            # Crear una nueva entrada en la base de datos
            new_memory = Memory(file_name=filename, file_type=file_type, section_id=section_id)
            db.session.add(new_memory)
            db.session.commit()
            
            flash('File uploaded successfully!')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid file format. Only JPG, JPEG, PNG, and MP4 files are allowed.')
    
    # Obtener todas las secciones para mostrar en el formulario
    sections = MemorySection.query.all()
    return render_template('memory_form.html', sections=sections)

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
