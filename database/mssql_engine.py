from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

MSSQL_URL = os.getenv(
    "MSSQL_URL", "mssql+pyodbc://user:pass@host/db?driver=ODBC+Driver+17+for+SQL+Server"
)
mssql_engine = create_engine(MSSQL_URL)
MSSQLSession = sessionmaker(autocommit=False, autoflush=False, bind=mssql_engine)
