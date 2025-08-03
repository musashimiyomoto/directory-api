from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", extra="ignore"
    )

    # Database settings
    DB_HOST: str = Field(default=..., description="DB Host")
    DB_PORT: int = Field(default=5432, description="DB Port")
    DB_USER: str = Field(default=..., description="DB User")
    DB_PASSWORD: str = Field(default=..., description="DB Password")
    DB_NAME: str = Field(default=..., description="DB Name")

    # API settings
    API_KEY: str = Field(default=..., description="API Key")
    API_KEY_NAME: str = Field(default="X-API-KEY", description="API Key Name")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()
