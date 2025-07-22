from sqlalchemy import String, Integer, Column

from connections.database import Base, engine

def create_tables():
    Base.metadata.create_all(bind=engine)

class Students(Base):
    __tablename__ = 'Students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    address = Column(String)  
    classid = Column(Integer, index=True)