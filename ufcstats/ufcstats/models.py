from sqlalchemy import Column, Integer, String, Boolean, Date, UniqueConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

def create_table(engine):
    Base.metadata.create_all(engine)


class Fighter(Base):
    __tablename__ = 'fighters'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    nationality = Column(String, nullable=True)
    locality = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    weight = Column(String, nullable=True)
    height = Column(String, nullable=True)
    reach = Column(Integer, nullable=True)
    stance = Column(String, nullable=True)
    wins = Column(Integer, nullable=True)
    losses = Column(Integer, nullable=True)
    draws = Column(Integer, nullable=True)
    belt = Column(Boolean, nullable=True)
    sherdog_id = Column(String, nullable=True, unique=True)
    nationality = Column(String, nullable=True)
    locality = Column(String, nullable=True)


class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    date = Column(Date, nullable=False)
    location = Column(String, nullable=False)

    fights = relationship("Fight", back_populates="event")
    __table_args__ = (UniqueConstraint('name', 'date', name='event_unique_constraint'),)

class Fight(Base):
    __tablename__ = 'fights'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String, ForeignKey('events.name'), nullable=False)
    r_fighter = Column(String, nullable=False)
    l_fighter = Column(String, nullable=False)
    r_status = Column(String, nullable=False)
    l_status = Column(String, nullable=False)
    r_knockdowns = Column(Integer, nullable=True)
    l_knockdowns = Column(Integer, nullable=True)
    r_significant_strikes = Column(Integer, nullable=True)
    l_significant_strikes = Column(Integer, nullable=True)
    r_takedowns = Column(Integer, nullable=True)
    l_takedowns = Column(Integer, nullable=True)
    r_submission_attempts = Column(Integer, nullable=True)
    l_submission_attempts = Column(Integer, nullable=True)
    weight_class = Column(String, nullable=False)
    method = Column(String, nullable=False)
    sub_method = Column(String, nullable=True)
    round = Column(Integer, nullable=False)
    time = Column(String, nullable=False)

    event = relationship("Event", back_populates="fights")
    __table_args__ = (UniqueConstraint('r_fighter', 'l_fighter', 'event_name', 'round', 'time', name='fight_unique_constraint'),)  

class SherdogIds(Base):
    __tablename__ = 'sherdog_ids'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    sherdog_id = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint('name', 'sherdog_id', name='sherdog_id_unique_constraint'),)