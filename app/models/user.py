from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    is_verified = Column(Boolean, default=True, nullable=False)