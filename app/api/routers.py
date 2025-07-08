# app/api/routers.py
from fastapi import APIRouter

from app.api.endpoints import course_router, user_router

main_router = APIRouter()
main_router.include_router(
    course_router, tags=["Courses"]
)
main_router.include_router(user_router)
