# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ufcstats.models import Fighter, Event, Fight, SherdogIds, create_table
from dotenv import load_dotenv
import os

load_dotenv()


class fighter_pipeline:

    def __init__(self):
        try:
            uri = os.getenv("URI")
            if uri is None:
                raise ValueError("Database URI is not set in environment variables")
            self.engine = create_engine(uri)
            create_table(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except:
            print("Error connecting to database")
            raise

    def process_item(self, item, spider):
        session = self.Session()
        fighter = Fighter(**item)

        # Check if fighter already exists
        try:
            existing_fighter = (
                session.query(Fighter)
                .filter_by(first_name=fighter.first_name, last_name=fighter.last_name)
                .first()
            )
            if existing_fighter:
                session.close()

            session.add(fighter)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class event_pipeline:

    def __init__(self):
        uri = os.getenv("URI")
        if uri is None:
            raise ValueError("Database URI is not set in environment variables")
        self.engine = create_engine(uri)
        create_table(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def process_item(self, item, spider):
        session = self.Session()
        event = Event(**item)

        # Check if event already exists
        try:
            existing_event = (
                session.query(Event).filter_by(name=event.name, date=event.date).first()
            )
            if existing_event:
                session.close()

            session.add(event)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item


class fight_pipeline:

    def __init__(self):
        try:
            uri = os.getenv("URI")
            if uri is None:
                raise ValueError("Database URI is not set in environment variables")
            self.engine = create_engine(uri)
            create_table(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except:
            print("Error connecting to database")
            raise

    def process_item(self, item, spider):
        session = self.Session()
        fight = Fight(**item)

        # Check if fight already exists
        try:
            existing_fight = (
                session.query(Fight)
                .filter_by(
                    r_fighter=fight.r_fighter,
                    l_fighter=fight.l_fighter,
                    event_name=fight.event_name,
                )
                .first()
            )
            if existing_fight:
                session.close()

            session.add(fight)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

class sherdog_id_pipeline:
    
    def __init__(self):
        try:
            uri = os.getenv("URI")
            if uri is None:
                raise ValueError("Database URI is not set in environment variables")
            self.engine = create_engine(uri)
            create_table(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except:
            print("Error connecting to database")
            raise

    def process_item(self, item, spider):
        session = self.Session()
        sherdog_id = SherdogIds(**item)

        # Check if sherdog_id already exists
        try:
            existing_sherdog_id = (
                session.query(SherdogIds)
                .filter_by(
                    name=sherdog_id.name,
                    sherdog_id=sherdog_id.sherdog_id,
                )
                .first()
            )
            if existing_sherdog_id:
                print(f"Sherdog ID for {item['name']} already exists skipping") 
                session.close()
                return item

            session.add(sherdog_id)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item