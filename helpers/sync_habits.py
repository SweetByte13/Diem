from models.userModel import User
from models.habitModel import Habit
from dateutil import rrule, parser
from models.habitOccuranceModel import Habit_Occurance
from config import db
from datetime import datetime, timezone, timedelta
from sqlalchemy import desc

def SyncHabits(user: User):
    """
    The backend then checks either: last habit occurance due_date, or if no previous occurrences 
    exist the create date of the habit. and uses it as the start date.

    The backend then uses the start date and recurrence pattern to generate all HabitOccurances 
    up to the Current DateTime.
    """
    #habits = Habit.query.filter(Habit.(Habit.is_inactive == None or Habit.is_inactive == False))
    #habits = user.habits.where(habit.is_inactive == None or habit.is_inactive == False)

    if(user is None or user.habits is None or len(user.habits) == 0):
        return

    habits = [habit for habit in user.habits if habit.is_inactive == None or habit.is_inactive == False]
    for habit in habits:
        latest_habit_occurance = Habit_Occurance.query.filter(Habit_Occurance.habit_id == habit.id).order_by(desc(Habit_Occurance.due_date)).first()
        if(not latest_habit_occurance):
            #use create date of habit as start date
            create_date_of_habit = habit.created_dt
            CreateHabitOccurances(habit, create_date_of_habit)
        else:
            #use the following date at midnight in order to include all habits for this date
            #adding 1 minute after midnight so it is not the same as the until RRULE
            day_after_midnight = (latest_habit_occurance.due_date + timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0)
            CreateHabitOccurances(habit, day_after_midnight)
    return ""

def CreateHabitOccurances(habit: Habit, start_date : datetime):
    #use the following date at midnight in order to include all habits for this date
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)
    tomorrow_midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    date = tomorrow_midnight.strftime("%Y%m%dT%H%M")
    dates_to_add_obj = rrule.rrulestr(habit.recurrence_pattern + "UNTIL=" + date, dtstart=start_date)
    dates_to_add = list(dates_to_add_obj)

    if len(dates_to_add) == 0:
        return ""

    habit_occurances_to_add = []
    for date in dates_to_add:
        new_occurance = Habit_Occurance(
            habit_id = habit.id,
            is_complete = False,
            due_date = date
        )
        habit_occurances_to_add.append(new_occurance)

    db.session.add_all(habit_occurances_to_add)
    db.session.commit()
    
    return ""