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
from sqlalchemy.orm import joinedload
from helpers.sync_habits import SyncHabits

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            user_id = session['user_id']
            if user_id:
                user = db.session.get(User, user_id)
                if user:
                    return make_response(user.to_dict(), 200)
        return make_response({"error": "Unauthorized User Must Login"}, 401)

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
            return make_response(user.to_dict(), 201)
        except IntegrityError as e:
            print(e)
            return make_response({"error": "422 unprocessable Entity", "details": str(e)}, 422)
        
class Login(Resource):
    def post(self):
        params = request.json
        username= params.get('username')
        user = User.query.filter(User.username == username).first()
        if not user:
            return make_response({"Error": "User not found"})
        if user.authenticate(params.get('password')):
            session['user_id'] = str(user.id)
            return make_response(user.to_dict())
        else:
            return make_response({"Error": "Invalid password"}, 401)
        
class Logout(Resource):
    def delete(self):
        print("Logging user out...")
        session.pop('user_id', None)
        return make_response({}, 204)

class Users(Resource):
    def get(self):
        return ("Hello World!")

class GetHabitsByUserAndDateRange(Resource):
    def get(self, id):
        if 'user_id' in session:
            user_id = session['user_id']
            if user_id:
                user = db.session.get(User, user_id)
                SyncHabits(user)
                
        else:
            user = db.session.get(User, uuid.UUID(id))
            SyncHabits(user)


        #temp data need to put this in query, will need to make midnight adjustment though
        last_week = datetime.now(timezone.utc) - timedelta(days=7)
        last_week_midnight = last_week.replace(hour=0, minute=0, second=0, microsecond=0)

        today = datetime.now(timezone.utc) + timedelta(days=1)
        today_midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)

        user_habits = User_Habit.query.filter(User_Habit.user_id == user.id and 
                                         (User_Habit.habit.is_inactive == None or User_Habit.habit.is_inactive == False))
        habits = [habit for habit in user.habits if habit.is_inactive == None or habit.is_inactive == False]

        user_habits = User_Habit.query.filter(User_Habit.user_id == user.id and Habit_Occurance.due_date >= last_week_midnight and Habit_Occurance.due_date <= today_midnight and
                                         (User_Habit.habit.is_inactive == None or User_Habit.habit.is_inactive == False))
        
        user_habits2 = [uh for uh in user_habits]

        user_habits_test = db.session.query(User_Habit).filter(User_Habit.user_id == user.id 
                                                               ).join(Habit, or_(Habit.is_inactive == None, Habit.is_inactive == False)
                                                                      ).join(Habit_Occurance
                                                                             ).filter( and_(Habit_Occurance.due_date >= last_week_midnight, Habit_Occurance.due_date <= today_midnight)
                                                                                      ).options(joinedload(Habit_Occurance)).all()
        user_huser_habits_test2 = [uh for uh in user_habits_test]

        user_habits3 = db.session.query(User_Habit).filter(User_Habit.user_id == user.id 
                                         ).join(Habit, and_(Habit.id == User_Habit.id)#, or_(Habit.is_inactive == None, Habit.is_inactive == False))
                                                ).all()#.join(Habit_Occurance, and_(Habit_Occurance.habit_id == Habit.id, Habit_Occurance.due_date >= last_week_midnight, Habit_Occurance.due_date <= today_midnight))
        
        user_habits4 = [uh for uh in user_habits3]
        
        habits = [habit for habit in user.habits.filter(Habit_Occurance.due_date >= last_week_midnight and Habit_Occurance.due_date >= today_midnight
                                                        and (Habit.is_inactive == None or Habit.is_inactive == False))]
        
        if user:
            return make_response(user.to_dict(), 200)
        return make_response({"error": "Unauthorized User Must Login"}, 401)