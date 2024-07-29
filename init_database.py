from app import create_app, db
from app.models import User, Post, MemorySection, Memory

def init_database():
    app = create_app()

    with app.app_context():
        db.create_all()

        # Elimina los datos existentes
        db.session.query(Memory).delete()
        db.session.query(MemorySection).delete()
        db.session.query(Post).delete()
        db.session.query(User).delete()

        # Agregar usuarios de ejemplo
        user1 = User(email='user1@example.com')
        user1.set_password('password')
        user2 = User(email='user2@example.com')
        user2.set_password('password')

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Agregar posts de ejemplo con user_id
        post1 = Post(section='goals_and_services', title='Our Goals', subtitle='What we aim for', content='We aim to make a difference...', image='path/to/image1.jpg', user_id=user1.id)
        post2 = Post(section='next_mission', title='Upcoming Mission', subtitle='Details about the mission', content='We are preparing for our next mission...', image='path/to/image2.jpg', user_id=user2.id)

        db.session.add(post1)
        db.session.add(post2)

        # Agregar secciones de memoria de ejemplo
        section1 = MemorySection(sectionName='Travel Memories')
        section2 = MemorySection(sectionName='Event Highlights')

        db.session.add(section1)
        db.session.add(section2)
        db.session.commit()

        # Agregar memorias de ejemplo
        memory1 = Memory(fileType='image', section_id=section1.id)
        memory2 = Memory(fileType='video', section_id=section2.id)

        db.session.add(memory1)
        db.session.add(memory2)
        db.session.commit()

    print("Database initialized and data added.")

if __name__ == '__main__':
    init_database()
