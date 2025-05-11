from database.sqlite_engine import sqlite_engine
from database.models.role_mapping import Base

if __name__ == "__main__":
    Base.metadata.create_all(bind=sqlite_engine)
    print("SQLite schema created.")
