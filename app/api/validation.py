from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.core.config import settings
from app.models.course import Course, CourseStatus, CourseSummary
from app.models.user import User


async def validate_course_summary_creation(course: Course, user: User) -> None:    
    """
    Asynchronously validates whether a user is authorized to create a summary for a given course.

    Args:
        course (Course): The course object to validate.
        user (User): The user attempting to create the summary.

    Raises:
        HTTPException: If the course does not exist (404 Not Found).
        HTTPException: If the user is not the author of the course (403 Forbidden).
    """
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if course.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only author of the course can create summary")

async def validate_count_summaries_last_hour_for_user(user: User, session: AsyncSession,) -> None:
    """
    Validates that the given user has not exceeded the allowed number of summary generation requests(default 3) in the past hour.

    Args:
        user (User): The user for whom to validate the request count.
        session (AsyncSession): The asynchronous database session.

    Raises:
        HTTPException: If the user has reached or exceeded the allowed number of summary requests per hour.
    """
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)

    stmt = (
        select(func.count(CourseSummary.id))
        .join(Course)
        .filter(
            Course.user_id == user.id,
            CourseSummary.created_at >= one_hour_ago
        )
    )

    result = await session.execute(stmt)
    count = result.scalar()
    if count >= settings.number_of_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You have reached the limit of 3 summaries per hour."
        )
