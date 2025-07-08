import enum
from sqlalchemy import Column, Enum, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.core.db import Base



class CourseStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    rejected = "rejected"
    
    
class Course(Base):
    user_id = Column(Integer, ForeignKey("user.id"))
    course_title = Column(String(255), nullable=False)
    course_description = Column(Text, nullable=False)
    status = Column(Enum(CourseStatus), default=CourseStatus.pending, nullable=False)
    
    summary = relationship("CourseSummary", back_populates="course", uselist=False)


class CourseSummary(Base):
    ai_summary = Column(Text)
    course_id = Column(Integer, ForeignKey("course.id"))
    
    course = relationship("Course", back_populates="summary")