from geopy.distance import geodesic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import models


async def get_organizations_by_name(
    skip: int,
    limit: int,
    name: str | None,
    session: AsyncSession,
) -> list[models.Organization]:
    query = select(models.Organization)
    if name:
        query = query.where(models.Organization.name.ilike(f"%{name}%"))
    result = await session.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_organizations_by_building_id(
    skip: int, limit: int, building_id: int, session: AsyncSession
) -> list[models.Organization]:
    result = await session.execute(
        select(models.Organization)
        .where(models.Organization.building_id == building_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_organizations_by_activity_id(
    skip: int,
    limit: int,
    activity_id: int,
    include_children: bool,
    session: AsyncSession,
) -> list[models.Organization]:
    query = select(models.Organization).join(
        models.OrganizationActivity,
        models.Organization.id == models.OrganizationActivity.organization_id,
    )

    if include_children:
        activity_ids = [activity_id]
        activity_result = await session.execute(
            select(models.Activity).where(models.Activity.id == activity_id)
        )
        activity = activity_result.scalar_one_or_none()

        if not activity:
            return None
        if activity.level < 3:
            children_result = await session.execute(
                select(models.Activity).where(models.Activity.parent_id == activity_id)
            )
            children = children_result.scalars().all()
            activity_ids.extend([child.id for child in children])
            if activity.level == 1:
                for child in children:
                    grandchildren_result = await session.execute(
                        select(models.Activity).where(
                            models.Activity.parent_id == child.id
                        )
                    )
                    activity_ids.extend(
                        [
                            grandchild.id
                            for grandchild in grandchildren_result.scalars().all()
                        ]
                    )
        query = query.where(
            models.OrganizationActivity.activity_id.in_(activity_ids)
        ).distinct()
    else:
        query = query.where(models.OrganizationActivity.activity_id == activity_id)

    result = await session.execute(query.offset(skip).limit(limit))
    return result.scalars().all()


async def get_organizations_by_radius(
    skip: int,
    limit: int,
    center_latitude: float,
    center_longitude: float,
    radius: float,
    session: AsyncSession,
) -> list[models.Organization]:
    buildings_result = await session.execute(select(models.Building))
    building_ids = []
    for building in buildings_result.scalars().all():
        distance = geodesic(
            (center_latitude, center_longitude),
            (building.latitude, building.longitude),
        ).kilometers
        if distance <= radius:
            building_ids.append(building.id)
    if not building_ids:
        return []
    result = await session.execute(
        select(models.Organization)
        .where(models.Organization.building_id.in_(building_ids))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_organizations_by_rectangle(
    skip: int,
    limit: int,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
    session: AsyncSession,
) -> list[models.Organization]:
    buildings_result = await session.execute(
        select(models.Building.id).where(
            (models.Building.latitude >= min_latitude)
            & (models.Building.latitude <= max_latitude)
            & (models.Building.longitude >= min_longitude)
            & (models.Building.longitude <= max_longitude)
        )
    )
    building_ids = buildings_result.scalars().all()
    if not building_ids:
        return []
    result = await session.execute(
        select(models.Organization)
        .where(models.Organization.building_id.in_(building_ids))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_organization_detail(
    organization_id: int, session: AsyncSession
) -> models.Organization | None:
    result = await session.execute(
        (
            select(models.Organization)
            .options(
                selectinload(models.Organization.building),
                selectinload(models.Organization.phone_numbers),
                selectinload(models.Organization.activities).selectinload(
                    models.OrganizationActivity.activity
                ),
            )
            .where(models.Organization.id == organization_id)
        )
    )
    return result.scalar_one_or_none()
