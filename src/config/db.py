from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    driver: str = Field(default="asyncpg", alias="DRIVER")
    dialect: str = Field(default="postgresql", alias="DIALECT")
    host: str = Field(default="localhost", alias="HOST")
    username: str = Field(..., alias="USERNAME")
    password: str = Field(..., alias="PASSWORD")
    port: int = Field(default=5432, alias="PORT")

    @property
    def build_url(self) -> str:
        return f"{self.driver}+{self.dialect}://{self.username}:{self.password}@{self.host}:{self.port}/"

    model_config = ConfigDict(
        extra="ignore",
    )


database_settings = DatabaseSettings()
