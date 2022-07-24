from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import _app_ctx_stack

db_url = "sqlite:///workspace.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
Base = declarative_base()
Base.metadata.bind = engine
Session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine),
    scopefunc=_app_ctx_stack.__ident_func__
)

def reset():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

