import asyncio
import logging

from db.models import (
    Activity,
    Building,
    Organization,
    OrganizationActivity,
    PhoneNumber,
)
from db.sessions import async_session


async def create_activities() -> dict[str, Activity]:
    """Create sample activities hierarchy

    Returns:
        Dictionary of activities

    """
    async with async_session() as session:
        food = Activity(name="Food", level=1)
        cars = Activity(name="Cars", level=1)
        session.add_all([food, cars])
        await session.commit()

        meat = Activity(name="Meat products", parent_id=food.id, level=2)
        dairy = Activity(name="Dairy products", parent_id=food.id, level=2)
        trucks = Activity(name="Trucks", parent_id=cars.id, level=2)
        passenger_cars = Activity(name="Passenger cars", parent_id=cars.id, level=2)
        session.add_all([meat, dairy, trucks, passenger_cars])
        await session.commit()

        parts = Activity(name="Parts", parent_id=passenger_cars.id, level=3)
        accessories = Activity(name="Accessories", parent_id=passenger_cars.id, level=3)
        session.add_all([parts, accessories])
        await session.commit()

        return {
            "food": food,
            "meat": meat,
            "dairy": dairy,
            "cars": cars,
            "trucks": trucks,
            "passenger_cars": passenger_cars,
            "parts": parts,
            "accessories": accessories,
        }


async def create_buildings() -> list[Building]:
    """Create sample buildings

    Returns:
        List of buildings

    """
    async with async_session() as session:
        buildings = [
            Building(
                address="123 Main St, New York", latitude=40.7128, longitude=-74.0060
            ),
            Building(
                address="456 Market St, San Francisco",
                latitude=37.7749,
                longitude=-122.4194,
            ),
            Building(
                address="789 Lombard St, San Francisco",
                latitude=37.8025,
                longitude=-122.4186,
            ),
            Building(
                address="321 Pine St, Seattle", latitude=47.6062, longitude=-122.3321
            ),
            Building(
                address="654 Broadway, New York", latitude=40.7308, longitude=-73.9973
            ),
        ]
        session.add_all(buildings)
        await session.commit()

        return buildings


async def create_organizations(
    buildings: list[Building], activities: dict[str, Activity]
) -> None:
    """Create sample organizations with phone numbers and activities

    Args:
        buildings: List of buildings
        activities: Dictionary of activities

    """
    async with async_session() as session:
        org1 = Organization(name="Best Foods Inc.", building_id=buildings[0].id)
        org2 = Organization(name="Dairy King", building_id=buildings[1].id)
        org3 = Organization(name="Meat Masters", building_id=buildings[0].id)
        org4 = Organization(name="Auto World", building_id=buildings[2].id)
        org5 = Organization(name="Truck Paradise", building_id=buildings[3].id)
        org6 = Organization(name="Car Parts Emporium", building_id=buildings[4].id)

        session.add_all([org1, org2, org3, org4, org5, org6])
        await session.commit()

        session.add_all(
            [
                PhoneNumber(number="555-123-4567", organization_id=org1.id),
                PhoneNumber(number="555-234-5678", organization_id=org1.id),
                PhoneNumber(number="555-345-6789", organization_id=org2.id),
                PhoneNumber(number="555-456-7890", organization_id=org3.id),
                PhoneNumber(number="555-567-8901", organization_id=org3.id),
                PhoneNumber(number="555-678-9012", organization_id=org4.id),
                PhoneNumber(number="555-789-0123", organization_id=org5.id),
                PhoneNumber(number="555-890-1234", organization_id=org6.id),
                PhoneNumber(number="555-901-2345", organization_id=org6.id),
            ]
        )
        await session.commit()

        session.add_all(
            [
                OrganizationActivity(
                    organization_id=org1.id, activity_id=activities["food"].id
                ),
                OrganizationActivity(
                    organization_id=org1.id, activity_id=activities["meat"].id
                ),
                OrganizationActivity(
                    organization_id=org1.id, activity_id=activities["dairy"].id
                ),
                OrganizationActivity(
                    organization_id=org2.id, activity_id=activities["food"].id
                ),
                OrganizationActivity(
                    organization_id=org2.id, activity_id=activities["dairy"].id
                ),
                OrganizationActivity(
                    organization_id=org3.id, activity_id=activities["food"].id
                ),
                OrganizationActivity(
                    organization_id=org3.id, activity_id=activities["meat"].id
                ),
                OrganizationActivity(
                    organization_id=org4.id, activity_id=activities["cars"].id
                ),
                OrganizationActivity(
                    organization_id=org4.id, activity_id=activities["passenger_cars"].id
                ),
                OrganizationActivity(
                    organization_id=org5.id, activity_id=activities["cars"].id
                ),
                OrganizationActivity(
                    organization_id=org5.id, activity_id=activities["trucks"].id
                ),
                OrganizationActivity(
                    organization_id=org6.id, activity_id=activities["cars"].id
                ),
                OrganizationActivity(
                    organization_id=org6.id, activity_id=activities["passenger_cars"].id
                ),
                OrganizationActivity(
                    organization_id=org6.id, activity_id=activities["parts"].id
                ),
            ]
        )
        await session.commit()


async def seed_db() -> None:
    """Main function to seed the database with test data"""
    await create_organizations(
        buildings=await create_buildings(), activities=await create_activities()
    )
    logging.info("Database seeded successfully")


if __name__ == "__main__":
    asyncio.run(seed_db())
