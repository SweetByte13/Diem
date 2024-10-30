from random import randint, choice as rc
from faker import Faker
from app import app
from config import db
from models.habitModel import Habit
from models.habitValueModel import Habit_Value
from models.userModel import User
from models.userHabitModel import User_Habit
from models.habitTrackingTypeModel import Habit_Tracking_Type
from models.habitOccuranceModel import Habit_Occurance
import uuid
from datetime import datetime, timedelta

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

def create_habits(user):
    name = "test habit"
    color = "#32a852"
    habit_tracking_type_id = "5288ff16dde74f5baa77c0c710897d28"
    recurrence_pattern = "FREQ=Weekly;BYDAY=Tu,Th;"
    habit_values = ["Cardio", "Weights"]

    habit = Habit(
                name=name,
                color=color,
                habit_tracking_type_id = uuid.UUID(habit_tracking_type_id),
                recurrence_pattern = recurrence_pattern
            )

    for hv in habit_values:
        habit_value = Habit_Value(
            value = hv
        )
        habit.habit_values.append(habit_value)

    new_user_habit = User_Habit()
    new_user_habit.habit = habit
    user.user_habits.append(new_user_habit) 

    name2 = "test habit2"
    color2 = "#333333"
    recurrence_pattern2 = "FREQ=Weekly;BYDAY=Mo,Tu,We,Th;"
    habit_values2 = ["Test Val1", "Test Val2"]

    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    habit2 = Habit(
                name=name2,
                color=color2,
                habit_tracking_type_id = uuid.UUID(habit_tracking_type_id),
                recurrence_pattern = recurrence_pattern2,
                created_dt=two_weeks_ago
            )

    for hv in habit_values2:
        habit_value = Habit_Value(
            value = hv
        )
        habit2.habit_values.append(habit_value)

    new_user_habit2 = User_Habit()
    new_user_habit2.habit = habit2
    user.user_habits.append(new_user_habit2) 

    name3 = "test habit3"
    color3 = "#fcba03"
    recurrence_pattern3 = "FREQ=Weekly;BYDAY=Mo,Tu,We,Th,Fr;"

    habit3 = Habit(
                name=name3,
                color=color3,
                habit_tracking_type_id = uuid.UUID(habit_tracking_type_id),
                recurrence_pattern = recurrence_pattern3,
                created_dt=two_weeks_ago
            )

    new_user_habit3 = User_Habit()
    new_user_habit3.habit = habit3
    user.user_habits.append(new_user_habit3) 

    db.session.commit()


def seed_database():
    with app.app_context():
        print("Clearing Database...")
        User_Habit.query.delete()
        Habit_Occurance.query.delete()
        Habit_Value.query.delete()
        Habit.query.delete()
        User.query.delete()
        Habit_Tracking_Type.query.delete()
        

        print("Seeding Users...")
        users = create_users()
        print("Seeding Habit Tracking Type...")
        create_habit_tracking_type()
        print("Seeding Habits...")
        create_habits(users[0])
        
        

if __name__ == '__main__':
    seed_database()