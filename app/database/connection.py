import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session

Base = declarative_base()

class Connection():
    def __init__(self, db_dialect, db_username, db_password, db_host, db_port, db_database):
        self._db_dialect = db_dialect
        self._db_username = db_username
        self._db_password = db_password
        self._db_host = db_host
        self._db_port = db_port
        self._db_database = db_database

    def connect(self):
        _DATABASE_URL = f"{self._db_dialect}://{self._db_username}:{self._db_password}@{self._db_host}:{self._db_port}/{self._db_database}"        
        
        engine = db.create_engine(_DATABASE_URL,pool_size=10,max_overflow=2,pool_recycle=300,pool_pre_ping=True,pool_use_lifo=True,echo=False)
        
        
        session_local = sessionmaker(bind=engine,autocommit=False, autoflush=True)
        session_scope = scoped_session(session_local)
        
        return engine, session_scope