import uuid
import re
from typing import List
from flask_restful import Resource
from flask import request, session, make_response
from config import db
from dateutil import rrule
from sqlalchemy.exc import IntegrityError
from models.habitModel import Habit
from models.habitValueModel import Habit_Value
from models.userModel import User
from models.userHabitModel import User_Habit

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
        recrule: str = ""
        user_id: uuid 
        habit_values: List[str] = []
        valid_rule: rrule

        name = params.get('name')
        color = params.get('color')
        habit_tracking_type = params.get('habit_tracking_type_id')
        recrule = params.get('recurrence_pattern')
        user_id = params.get('user_id')
        try:
            valid_rule = rrule.rrulestr(recrule + "Count=1")
        except Exception as e:
            return make_response({"error": "422 Invalid Recurence Rule Set", "details": str(e)}, 422) 
        
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color)
        if not match:                      
            return make_response({"error": "422 Invalid Hex Color", "details": "Invalid Hex Color"}, 422) 

        habit_values = params.get('habit_values')

        user = db.session.query(User).filter_by(id=uuid.UUID(user_id)).one_or_none()

        try:
            if(user is None):
                raise Exception("User not found.")
        
            habit = Habit(
                name=name,
                color=color,
                habit_tracking_type_id = uuid.UUID(habit_tracking_type),
                recurrence_pattern = recrule
            )

            for hv in habit_values:
                habit_value = Habit_Value(
                    value = hv
                )
                habit.habit_values.append(habit_value)

            new_user_habit = User_Habit()
            new_user_habit.habit = habit
            user.user_habits.append(new_user_habit) 
            db.session.commit()

            return make_response(habit.to_dict(rules=("-user_habits","-habit_values", "-habit_occurances", "-user", "-habit_tracking_type")), 201)
        except IntegrityError as e:
            print(e)
            return make_response({"error": "422 unprocessable Entity", "details": str(e)}, 422)
        except Exception as e:
            print(e)
            return make_response({"error": "422 unprocessable Entity", "details": str(e)}, 422)
    
class HabitById(Resource):
    def patch(self, id):
        habit = db.session.get(Habit, uuid.UUID(id))
        if habit:
            params = request.json
            for attr in params:
                setattr(habit, attr, params[attr])
            habit.is_active = True
            db.session.commit()
            return make_response("Habit ID" + id + " successfully made inactive")