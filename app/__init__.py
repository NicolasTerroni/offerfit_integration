from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Configure SQLAlchemy
engine = create_engine('sqlite:///events.db')
Session = sessionmaker(bind=engine)

from app import routes  # Import routes after initializing app

if __name__ == '__main__':
    app.run(debug=True)
