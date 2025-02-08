from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    birth_city = Column(String, nullable=True)

class SupportRequest(Base):
    __tablename__ = "support_requests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    message = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)