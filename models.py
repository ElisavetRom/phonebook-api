from sqlalchemy import Column, Integer, String
from database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile = Column(String, nullable=True)
    home = Column(String, nullable=True)