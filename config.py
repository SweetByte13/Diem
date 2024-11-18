from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import os
from dotenv import load_dotenv

load_dotenv()

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

def start_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json.compact = False

    # Load the secret key
    app.secret_key = os.getenv('SECRET_KEY_DIEM')
    print("!!!!!!!!!!!!!!!!!!!!!!!!")
    print(app.secret_key)

    if not app.secret_key:
        raise ValueError("SECRET_KEY not found in environment variables")

    migrate = Migrate(app, db)
    from models import baseModel
    db.init_app(app)
    
    # Allow CORS for specific origins (update with your frontend's URL)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    
    return app
