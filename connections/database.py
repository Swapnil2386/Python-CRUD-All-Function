from sqlalchemy.orm import declarative_base,  sessionmaker
from sqlalchemy import create_engine
from utility.password_utility import hash_password

engine = create_engine('postgresql://postgres:Swapnil%40123@localhost/Testing',echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#session = sessionmaker(bind=engine)()
Base = declarative_base()

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "hashed_password": hash_password("admin123")
    }
}

def get_hashed_password(password: str):
    _hashpassword = hash_password(password)
    if _hashpassword:
        return _hashpassword
    else:
     None

def get_user_by_username(username: str):
    return fake_users_db.get(username)