from sqlalchemy import create_engine, Column, Integer, String, and_, delete
import sqlite3

from sqlalchemy.orm import declarative_base, sessionmaker
""""
conn = sqlite3.connect('test.db')
engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()

session = sessionmaker(bind=engine)()


class User(Base):
    __tablename__  = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String)

    def __init__(self, nickname):
        self.nickname = nickname


Base.metadata.create_all(engine)

user = User("testname123")
session.add(user)

session.commit()

test3 = User
test = test3.nickname == "testname123"
test2 = test3.id == 1


def search(model, operation, *args):
    print(args)
    users = session.query(model).filter(operation(*args))
    print(users[0].nickname)

search(test3, and_, test)
"""


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

