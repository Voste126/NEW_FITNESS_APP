from app import db,app
from models import User, Workout, Exercise
from faker import Faker
import re
import random

fake = Faker()

def generate_fake_password():
    while True:
        password = fake.password(length=12)
        if (
            len(password) >= 12 and
            len(password) <= 60 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password)
        ):
            return password
def generate_fake_email():
    return fake.email()

def generate_fake_phone_number():
    return fake.phone_number()

def seed():
    with app.app_context():
        db.create_all()

        for _ in range(5):
            fake_username = fake.user_name()
            fake_password = generate_fake_password()
            fake_email = generate_fake_email()  # Add this line to generate fake email
            fake_phone_number = generate_fake_phone_number()  # Generate fake phone number
            user = User(username=fake_username, password=fake_password, user_email=fake_email, user_phone_number=fake_phone_number)
            db.session.add(user)

            for _ in range(3):
                fake_date = fake.date_this_decade()
                workout = Workout(date=fake_date, user=user)
                db.session.add(workout)

                for _ in range(4):
                    fake_name = fake.word()
                    fake_duration = fake.random_int(min=10, max=120)
                    fake_distance = random.uniform(1.0, 10.0)
                    fake_sets = fake.random_int(min=1, max=5)
                    fake_reps = fake.random_int(min=5, max=20)
                    fake_weight = fake.random_int(min=5, max=50)
                    fake_category = fake.random_element(elements=('Upper Body', 'Lower Body'))
                    exercise = Exercise(
                        name=fake_name,
                        duration_minutes=fake_duration,
                        distance_km=fake_distance,
                        sets=fake_sets,
                        reps=fake_reps,
                        weight_kg=fake_weight,
                        category=fake_category,
                        workout=workout
                    )
                    db.session.add(exercise)

        db.session.commit()

if __name__ == '__main__':
    seed()
