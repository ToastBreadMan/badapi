from sqlalchemy import create_engine, Column, Integer, String, and_, delete
import sqlite3

from sqlalchemy.orm import declarative_base, sessionmaker


class SQLDatabaseControl:
    Base = None
    def __init__(self, dbname):
        # self.conn = sqlite3.connect(f'sqlite:///{dbname}')
        self.engine = create_engine(f'sqlite:///{dbname}', echo=True)
        self.session = sessionmaker(bind=self.engine)()
        self.Base = declarative_base()

    def filter(self, model, operation, *args):
        query_response = self.session.query(model).filter(operation(*args))
        return query_response

    def register(self):
        self.Base.metadata.create_all(self.engine)

    def add(self, model):
        self.session.add(model)
        self.session.commit()
        return "added model to database"

    def remove(self, model):
        # always commit changes
        self.session.delete(model)
        self.session.commit()
        return "object removed"

    def update(self, model, **kwargs):
        print(kwargs)
        # model.update(kwargs)


db = SQLDatabaseControl(dbname="test.db")


class User(db.Base):
    __tablename__  = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)

    def __init__(self, nickname):
        self.nickname = nickname

db.register()
user = User("test")
db.add(user)

