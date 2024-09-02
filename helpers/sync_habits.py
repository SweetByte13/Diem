from models.userModel import User
from models.habitModel import Habit
from dateutil import rrule, parser
from models.habitOccuranceModel import Habit_Occurance
from config import db
from datetime import datetime, timezone

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
        latest_habit_occurance = Habit_Occurance.query.filter(Habit_Occurance.habit_id == habit.id).order_by(Habit_Occurance.due_date).first()
        if(not latest_habit_occurance):
            print("use create date of habit as start date")
            #use create date of habit as start date
            create_date_of_habit = habit.created_dt
            CreateHabitOccurances(habit, create_date_of_habit)
        else:
            #use latest habit occurence due date
            print("use latest habit occurence due date")
    return ""

def CreateHabitOccurances(habit: Habit, start_date : datetime):
     date = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M") # + "Z"
     dates_to_add_obj = rrule.rrulestr(habit.recurrence_pattern + "UNTIL=" + date, dtstart=start_date)
     dates_to_add = list(dates_to_add_obj)
     test = ""
    #  try:
    #         valid_rule = rrule.rrulestr(recrule + "Count=1")
    #     except Exception as e:
    #         return make_response({"error": "422 Invalid Recurence Rule Set", "details": str(e)}, 422)
     return ""