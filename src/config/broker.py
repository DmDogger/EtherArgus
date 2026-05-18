from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BrokerSettings(BaseSettings):
    bootstrap_server: str = Field(
        default="127.0.0.1:9092",
        alias="KAFKA_BOOTSTRAP_SERVERS",
    )
    topic: str = Field(default="MLServiceTopic", alias="KAFKA_TOPIC")

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )


broker_settings = BrokerSettings()
