from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RoleMapping(Base):
    __tablename__ = "role_mappings"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=False)
    title = Column(String, nullable=False)
    manager_dn = Column(String)
    ad_groups = Column(String)  # comma-separated for simplicity
