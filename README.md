# Diem: Your Personal Habit Tracker

Diem is a habit tracking application with a Python backend that helps users create, track, and maintain their habits over time.

## Features

- User profile creation
- Add or remove habits
- Choose the frequency of the habit
- Mark the habit as completed, which timestamps the completion and records it for tracking progress

### Built With

* Python
* Flask
* SQlite3


## System Requirements

- Python 3.8 or higher
- pip for package management

## Installation

1. Clone the repository
```console
git clone git@github.com:<username>/Diem.git
```

2. Navigate into the cloned project directory
```console
cd Diem
```

3. Install the required packages
```console
pipenv install
pipenv shell
pip install Flask
pip install Flask-SQLAlchemy
pip install Flask-RESTful
pip install Flask-Cors
pip install ipdb
pip install sqlalchemy-serializer
pip install Faker
```

## Testing

test are located in the tests directory
files must begin with 'test_'
function must begin with 'test_'
classes must begin with 'Test'

to run use:
```
python -m pytest --verbose
```

## Migration Issues Solutions
If you run into an issue with multiple heads in your migrations, run the following code in the console:
```
flask db merge heads -m "merging two heads"
```

To ensure that the database has only one head or to see the database history, run:
```
flask db history
```

## Running the Application

To run Diem, use the following command:
```console
python app.py
```

## Contributing

Contributions are welcome and can be made via pull requests. Please ensure that your code follows the PEP 8 style guide.

## Known Issues

There are no known issues or limitations with the current version of Diem.
Thank you for using Diem, your personal habit tracker. Happy habit forming!