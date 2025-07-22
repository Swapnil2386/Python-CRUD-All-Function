from sqlalchemy import String, Integer, Column

from connections.database import Base, engine

def create_tables():
    Base.metadata.create_all(bind=engine)

class Teachers(Base):
    __tablename__ = 'Teachers'

    Id = Column(Integer, primary_key=True, index=True)
    TeacherName = Column(String, index=True)
    TeacherEmail = Column(String, unique=True, index=True)
    TeacherAddress = Column(String)