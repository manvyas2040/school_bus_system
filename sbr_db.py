from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
db_url ="postgresql://postgres:man1755@localhost:5432/demodb"

engine = create_engine(db_url)
Sessionlocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()