from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.services import get_ai_summary
from app.api.validation import validate_count_summaries_last_hour_for_user, validate_course_summary_creation
from app.core.db import get_async_session
from app.crud.course import course_crud, course_summary_crud
from app.models.course import CourseStatus
from app.schemas.course import CourseCreate, CourseOut, CourseSummaryOut

from app.core.user import current_user
from app.models import User

router = APIRouter()



@router.post("/course", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    course: CourseCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    # Here you need to add validation logic for the course creation.
    # For example, you might want to check if the course title is unique,
    new_course = await course_crud.create(course, session, user)
    return new_course


@router.post("/generate_summary/{course_id}", response_model=CourseSummaryOut, status_code=status.HTTP_201_CREATED)
async def generate_summary(
    course_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    obj = await course_crud.get(course_id, session)
    await validate_course_summary_creation(obj, user)
    if obj.status == CourseStatus.completed:
        return obj.summary
    await validate_count_summaries_last_hour_for_user(user, session)
    ai_summary = await get_ai_summary(obj.course_description)
    update_data = {"status": CourseStatus.completed}
    await course_crud.update(obj, update_data, session)
    ai_summary = await course_summary_crud.create({"ai_summary": ai_summary, "course_id": obj.id}, session)
    return ai_summary


@router.get(
    '/course/{course_id}', response_model=list[CourseOut],
)
async def get_my_courses(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """
    Retrieve the list of courses associated with the current user.

    Args:
        session (AsyncSession): The asynchronous database session dependency.
        user (User): The currently authenticated user dependency.

    Returns:
        List[Course]: A list of courses that belong to the current user.
    """
    courses = await course_crud.get_by_user(
        session=session, user=user
    )
    return courses 