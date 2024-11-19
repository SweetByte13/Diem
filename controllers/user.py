import uuid
from flask import request, session, make_response, jsonify
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from models.userModel import User
from models.habitModel import Habit
from models.userHabitModel import User_Habit
from models.habitOccuranceModel import Habit_Occurance
from config import db
from datetime import datetime, timezone, timedelta
from sqlalchemy import and_, or_
from sqlalchemy.orm import joinedload, aliased
from helpers.sync_habits import SyncHabits

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        
        if user_id:
            try:
                # Convert user_id to UUID if necessary
                user_uuid = uuid.UUID(user_id)
                user = db.session.get(User, user_uuid)
                
                if user:
                    return make_response({"user": user.to_dict(only=("id", "username", "email"))}, 200)
                else:
                    return make_response({"error": "User not found"}, 404)
            except ValueError:
                # Handle cases where user_id is not a valid UUID
                return make_response({"error": "Invalid user ID"}, 400)
        else:
            return make_response({"error": "Not authenticated"}, 401)



class SignUp(Resource):
    def post(self):
        params = request.get_json()
        username = params.get('username')
        email = params.get('email')
        password = params.get('password')
        
        user = User(
            username=username,
            email=email
        )
        user.password_hash = password
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            print(user)
            return make_response(user.to_dict(only=("id", "username", "email")), 201)
        except IntegrityError as e:
            print(e)
            return make_response({"error": "422 unprocessable Entity", "details": str(e)}, 422)

class Login(Resource):
    def post(self):
        params = request.json
        username = params.get('username')
        password = params.get('password')

        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response({"Error": "User not found"}, 404)

        if user.authenticate(password):
            session['user_id'] = str(user.id)
            return make_response(user.to_dict(only=("id", "username", "email")), 200)
        else:
            return make_response({"Error": "Invalid password"}, 401)


class Logout(Resource):
    def delete(self):
        user_id = session.get('user_id')
        if user_id:
            print(f"Logging out user with ID: {user_id}")
            session.pop('user_id', None)
        else:
            print("No user_id found in session.")
        return make_response({}, 204)


class Users(Resource):
    def get(self):
        return ("Hello World!")

class GetHabitsByUserAndDateRange(Resource):
    def post(self, id):
        params = request.json
        param_start_date = params.get('startDate')
        param_end_date = params.get('endDate')

        try:
            start_date = datetime.strptime(param_start_date, '%Y-%m-%d')
            end_date = datetime.strptime(param_end_date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD.", 400

        if 'user_id' in session:
            user_id = session['user_id']
            if user_id:
                user = db.session.get(User, user_id)
                SyncHabits(user)
                
        else:
            user = db.session.get(User, uuid.UUID(id))
            SyncHabits(user)

        #adjusting endDate to make sure query includes all results from that day
        end_date = end_date + timedelta(days=1)
        end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)

        user_habits = User_Habit.query.filter(User_Habit.user_id == user.id and Habit_Occurance.due_date >= start_date and Habit_Occurance.due_date <= end_date and
                                         (User_Habit.habit.is_inactive == None or User_Habit.habit.is_inactive == False))
        
        habit_list = [uh.habit for uh in user_habits]
      
        #manually creating response dictionary because of problems getting sql alchemy to return the exact subset that is required
        result_list = []
        for habit in habit_list:
            #habit_occurances_in_range = Habit_Occurance.query.filter(Habit_Occurance.habit_id == habit.id and Habit_Occurance.due_date >= start_date and Habit_Occurance.due_date <= end_date)
            habit_occurances_in_range = Habit_Occurance.query.filter( Habit_Occurance.habit_id == habit.id ).filter( Habit_Occurance.due_date >= start_date ).filter( Habit_Occurance.due_date <= end_date ).all()
            result_list.append({
                "habit_id": habit.id,
                "name": habit.name,
                "color": habit.color,
                "recurrence_pattern": habit.recurrence_pattern,
                "created_dt": "" if habit.created_dt is None else habit.created_dt.strftime("%Y-%m-%d"),
                "habit_occurances": [{
                    "id": ho.id,
                    "is_complete": ho.is_complete,
                    "dt_completed": "" if ho.dt_completed is None else ho.dt_completed.strftime("%Y-%m-%d"),
                    "due_date": "" if ho.due_date is None else ho.due_date.strftime("%Y-%m-%d"),
                    "habit_value": "" if ho.habit_value is None else ho.habit_value.value
                } for ho in habit_occurances_in_range]
            })


        if user:
            return make_response(result_list, 200)
        return make_response({"error": "Could not get user habits"}, 401)