from sqlalchemy.orm import declarative_base,  sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:Swapnil%40123@localhost/Testing',echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#session = sessionmaker(bind=engine)()
Base = declarative_base()