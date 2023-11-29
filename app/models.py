from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
from datetime import datetime   


Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    event_type = Column(String)
    timestamp = Column(String)
    email_id = Column(Integer)
    clicked_link = Column(String)
    product_id = Column(Integer)
    amount = Column(Float)


engine = create_engine('sqlite:///events.db')
inspector = inspect(engine)

if not inspector.has_table('events'):
    Base.metadata.create_all(engine)