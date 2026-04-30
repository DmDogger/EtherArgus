from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EtherscanSettings(BaseSettings):
    api_key_etherscan: str = Field(..., alias="API_KEY_ETHERSCAN")
    etherscan_url: str = Field(..., alias="ETHERSCAN_URL")
    etherscan_api_call_limit: int = Field(..., alias="ETHERSCAN_API_CALL_LIMIT")

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


etherscan_settings = EtherscanSettings()
