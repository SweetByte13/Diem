from typing import List
import uuid
from flask_restful import Resource
from flask import request, session, make_response
from config import db
from sqlalchemy.exc import IntegrityError
from models.habitModel import Habit
from models.habitValueModel import Habit_Value
from models.userModel import User
# Supported iCalendar RRULE options
# freq = "DAILY", "WEEKLY", "MONTHLY"
# weekday = "SU", "MO", "TU", "WE", "TH", "FR", "SA"
# bymodaylist = ( monthdaynum *("," monthdaynum) )

class HabitController(Resource):
    def post(self):
        params = request.get_json()

        name: str = ""
        color: str = ""
        habit_tracking_type: uuid
        rrule: str = ""
        user_id: uuid 
        habit_values: List[str] = []

        name = params.get('name')
        color = params.get('color')
        habit_tracking_type = params.get('habit_tracking_type_id')
        rrule = params.get('recurrence_pattern')
        user_id = params.get('user_id')

        habit_values = params.get('habit_values')

        user = session.query(User).filter_by(id=user_id).one_or_none()

        try:
            if(user is None):
                raise Exception("User not found.")
        
            habit = Habit(
                name=name,
                color=color,
                habit_tracking_type_id = habit_tracking_type,
                recurrence_pattern = rrule
            )

            for hv in habit_values:
                habit_value = Habit_Value(
                    value = hv
                )
                habit.habit_values.append(habit_value)

            user.habits.append(habit)
                
            db.session.add(habit)
            db.session.commit()

            return make_response(habit.to_dict(), 201)
        except IntegrityError as e:
            print(e)
            return make_response({"error": "422 unprocessable Entity", "details": str(e)}, 422)
        except Exception as e:
            print(e)
            return make_response({"error": "422 unprocessable Entity", "details": str(e)}, 422)