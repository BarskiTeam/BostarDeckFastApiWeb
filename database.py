from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# check_same_thread - tylko dla sqlite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# dla sqlite wymagane by dzialał cascade_delete
event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
