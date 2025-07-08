from pydantic import BaseModel
from app.models.course import CourseStatus


class CourseBase(BaseModel):
    course_title: str
    course_description: str
    
    model_config = {"extra": "forbid"}


class CourseCreate(CourseBase):
        ...  

    
class CourseOut(CourseBase):
    id: int
    status: CourseStatus
    
    class Config:
        from_attributes = True

class CourseSummaryBase(BaseModel):
    ai_summary: str 
    
    model_config = {"extra": "forbid"}

        
class CourseSummaryCreate(CourseSummaryBase):
    ...
    
class CourseSummaryOut(CourseSummaryBase):
    id: int
    course_id: int
    
    class Config:
        from_attributes = True