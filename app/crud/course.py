from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Course, User
from app.models.course import CourseSummary


class CRUDCourse:
    def __init__(self, model):
        self.model = model
    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).options(selectinload(self.model.summary)).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: User | None = None,
    ):
        obj_in_data = obj_in.model_dump()
        if user is not None:
            obj_in_data["user_id"] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)

        for field in obj_data:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    async def get_by_user(
        self,
        session: AsyncSession,
        user: User
    ):
        courses = await session.execute(
            select(self.model).where(
                self.model.user_id == user.id
            )
        )
        return courses.scalars().all()


class CRUDCourseSummary:
    def __init__(self, model):
        self.model = model
        
    async def get_by_course_id(
        self,
        course_id: int,
        session: AsyncSession,
    ):
        print(self.model)
        db_obj = await session.execute(
            select(self.model).where(self.model.course_id == course_id)
        )
        a = db_obj.scalars().first()
        print(a)
        return a

    async def create(
        self,
        data,
        session: AsyncSession,
    ):
        db_obj = self.model(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    async def update(
        self,
        db_obj,
        obj_in,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)

        for field in obj_data:
            if field in obj_in:
                setattr(db_obj, field, obj_in[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    
    
course_crud = CRUDCourse(Course)
course_summary_crud = CRUDCourseSummary(CourseSummary)
