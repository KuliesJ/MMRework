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
        user1 = User(email='renatos@nder.us')
        user1.set_password('medicalmissionstoperu')

        db.session.add(user1)
        db.session.commit()

        # Agregar posts de ejemplo con user_id

        # Agregar secciones de memoria de ejemplo
        section1 = MemorySection(sectionName='Travel Memories')
        section2 = MemorySection(sectionName='Event Highlights')

        db.session.add(section1)
        db.session.add(section2)
        db.session.commit()


    print("Database initialized and data added.")

if __name__ == '__main__':
    init_database()
