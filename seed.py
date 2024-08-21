from random import randint, choice as rc
from faker import Faker
from app import app
from config import db
from models.userModel import User
from models.habitTrackingTypeModel import Habit_Tracking_Type
import uuid

fake = Faker()

def create_users():
    print("Creating Users...")
    users = []
    tina = User(
        username = "chefmaster",
        email = "chefmaster@example.com",
        password_hash = "hashed_password_1"
    )

    tim = User(
        username = "bakerqueen",
        email = "bakerqueen@example.com",
        password_hash = "hashed_password_2"
    )

    tommy = User(
        username = "pastrypro",
        email = "pastrypro@example.com",
        password_hash = "hashed_password_3"
    )
    users.append(tina)
    users.append(tim)
    users.append(tommy)
    db.session.add_all(users)
    db.session.commit()
    return users

def create_habit_tracking_type():
    print("Creating habit tracking type...")
    check = Habit_Tracking_Type(
        id = uuid.UUID("5288ff16dde74f5baa77c0c710897d28"),
        name = "Check"
    )
    db.session.add(check)
    db.session.commit()
    return check



def seed_database():
    with app.app_context():
        print("Clearing Database...")
        User.query.delete()
        Habit_Tracking_Type.query.delete()
        
        print("Seeding Users...")
        create_users()
        print("Seeding Habit Tracking Type...")
        create_habit_tracking_type()
        
        

if __name__ == '__main__':
    seed_database()