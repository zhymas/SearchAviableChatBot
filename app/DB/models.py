from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://bot_user:bot_user@localhost:5432/bot'
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String, unique=True)
    api_id = Column(Integer)
    api_hash = Column(String)
    user_id = Column(Integer, unique=True)
    
    def __init__(self, name, phone_number, api_id, api_hash, user_id):
        self.name = name
        self.phone_number = phone_number
        self.api_id = api_id
        self.api_hash = api_hash
        self.user_id = user_id
        
    def __repr__(self):
        return f"<User(name='{self.name}', phone_number='{self.phone_number}', api_id='{self.api_id}', api_hash='{self.api_hash}')>"

def create_tables():
    Base.metadata.create_all(engine)
    return "Successfully Created"

Session = sessionmaker(bind=engine)
session = Session()
