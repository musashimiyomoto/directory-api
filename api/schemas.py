from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


#########################
# Activity
#########################


class Activity(BaseSchema):
    id: int = Field(default=..., description="ID of the activity", ge=0)
    name: str = Field(
        default=..., description="Name of the activity", min_length=1, max_length=255
    )
    parent_id: int | None = Field(
        default=None, description="Parent ID of the activity", ge=0
    )
    level: int = Field(default=1, description="Level of the activity", ge=1, le=3)


#########################
# Building
#########################


class Building(BaseSchema):
    id: int = Field(default=..., description="ID of the building", ge=0)
    address: str = Field(
        default=..., description="Address of the building", min_length=1, max_length=255
    )
    latitude: float = Field(
        default=..., description="Latitude of the building", ge=-90, le=90
    )
    longitude: float = Field(
        default=..., description="Longitude of the building", ge=-180, le=180
    )


#########################
# Phone Number
#########################


class PhoneNumber(BaseSchema):
    id: int = Field(default=..., description="ID of the phone number", ge=0)
    organization_id: int = Field(
        default=..., description="ID of the organization", ge=0
    )
    number: str = Field(
        default=..., description="Phone number", min_length=1, max_length=255
    )


#########################
# Organization
#########################


class Organization(BaseSchema):
    id: int = Field(default=..., description="ID of the organization", ge=0)
    name: str = Field(
        default=...,
        description="Name of the organization",
        min_length=1,
        max_length=255,
    )
    building_id: int = Field(default=..., description="ID of the building", ge=0)


class OrganizationDetail(Organization):
    building: Building = Field(default=..., description="Building of the organization")
    phone_numbers: list[PhoneNumber] = Field(
        default_factory=list, description="Phone numbers of the organization"
    )
    activities: list[Activity] = Field(
        default_factory=list, description="Activities of the organization"
    )


#########################
# Query
#########################


class PaginationQuery(BaseModel):
    skip: int = Field(default=0, description="Skip", ge=0)
    limit: int = Field(default=100, description="Limit", gt=0)


class OrganizationByNameQuery(PaginationQuery):
    name: str | None = Field(default=None, description="Name")


class OrganizationByBuildingQuery(PaginationQuery):
    building_id: int | None = Field(default=None, description="Building ID", ge=0)


class OrganizationByActivityQuery(PaginationQuery):
    activity_id: int | None = Field(default=None, description="Activity ID", ge=0)
    include_children: bool = Field(default=True, description="Include children ?")


class OrganizationByRadiusQuery(PaginationQuery):
    center_latitude: float = Field(default=..., description="Latitude", ge=-90, le=90)
    center_longitude: float = Field(
        default=..., description="Longitude", ge=-180, le=180
    )
    radius: float = Field(default=..., description="Search radius in kilometers", gt=0)


class OrganizationByRectangleQuery(PaginationQuery):
    min_latitude: float = Field(
        default=..., description="Minimum latitude", ge=-90, le=90
    )
    min_longitude: float = Field(
        default=..., description="Minimum longitude", ge=-180, le=180
    )
    max_latitude: float = Field(
        default=..., description="Maximum latitude", ge=-90, le=90
    )
    max_longitude: float = Field(
        default=..., description="Maximum longitude", ge=-180, le=180
    )
