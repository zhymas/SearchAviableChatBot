from DB.models import Session, User
from sqlalchemy.sql import exists

def check_exist_phone(phone):
    with Session.begin() as session:
        return session.query(exists().where(User.phone_number==phone)).scalar()


def check_user(user_id):
    with Session.begin() as session:
        return session.query(exists().where(User.id==user_id)).scalar()
    
