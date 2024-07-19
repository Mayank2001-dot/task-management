from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
import pytz

Base = declarative_base()

class StatusEnum(enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class Management(Base):
    __tablename__ = 'management'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.todo)
    # created_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Kolkata')))