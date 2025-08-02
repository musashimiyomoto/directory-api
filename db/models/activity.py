from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base


class Activity(Base):
    __tablename__ = "activities"
    __table_args__ = (
        CheckConstraint("level >= 1 AND level <= 3", name="check_level_range"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id"), nullable=True
    )
    level: Mapped[int] = mapped_column(nullable=False, default=1)

    parent = relationship("Activity", remote_side=[id], backref="children")
    organizations = relationship("OrganizationActivity", back_populates="activity")
