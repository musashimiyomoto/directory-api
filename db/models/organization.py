from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")
    phone_numbers = relationship(
        "PhoneNumber", back_populates="organization", cascade="all, delete-orphan"
    )
    activities = relationship(
        "OrganizationActivity",
        back_populates="organization",
        cascade="all, delete-orphan",
    )
