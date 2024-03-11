from . import db, Model
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class TimestampMixin(object):

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=datetime.utcnow, nullable=True)
