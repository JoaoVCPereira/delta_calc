from contextlib import contextmanager
import utils.utils as utils
import threading
import logging
from sqlalchemy.orm import scoped_session
from database.connection import Base, Connection as DBConnection
import database.connection as db


class Connection:
    def __init__(self, db_config, db_tables: str) -> None:
        self._db_config = db_config
        self._db_tables = db_tables

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()
        return True

    def connect(self):
        """
        Use this method only if manually opening. If used with the 'with' clause, don't need to
        call.
        Try:
        with Session(dbconfig, dbtables) as conn
        """
        db_conn = DBConnection(
            self._db_config.db_dialect,
            self._db_config.db_username,
            self._db_config.db_password,
            self._db_config.db_host,
            self._db_config.db_port,
            self._db_config.db_database
        )

        self._engine, self._session_scope = db_conn.connect()
        tables_list = self._db_tables.split(',')
        for table in tables_list:
            Base.metadata.create_all(self._engine, tables=[Base.metadata.tables[table]])

    def close(self):
        """
        Use this method only if manually opening. If used with the 'with' clause, don't need to
        call.        
        Try:
        with Session(dbconfig, dbtables) as conn
        """
        self._engine.dispose()
        
    @contextmanager
    def open_session(self):
        """
        use exclusively inside 'with' clause.
        opens the session
        """
        self._timer = utils.get_current_datetime()
        self._session = self._session_scope()
        try:
            yield self._session
        except:
            #RetryingQuery()
            raise
        finally:
            self._session.close()