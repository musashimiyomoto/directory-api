from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base


class Building(Base):
    __tablename__ = "buildings"
    __table_args__ = (
        CheckConstraint(
            "latitude >= -90 AND latitude <= 90", name="check_latitude_range"
        ),
        CheckConstraint(
            "longitude >= -180 AND longitude <= 180", name="check_longitude_range"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    organizations = relationship("Organization", back_populates="building")
