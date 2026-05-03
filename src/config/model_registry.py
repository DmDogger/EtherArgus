from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ARTIFACTS_DIR = _PROJECT_ROOT / "artifacts"


class ModelRegistrySettings(BaseSettings):
    feature_order_path: Path = Field(default=_ARTIFACTS_DIR / "feature_order.json")
    imputer_path: Path = Field(default=_ARTIFACTS_DIR / "imputer.pkl")
    scaler_path: Path = Field(default=_ARTIFACTS_DIR / "scaler.pkl")
    model_path: Path = Field(default=_ARTIFACTS_DIR / "XGB_FRAUD.pickle")

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

model_registry_settings = ModelRegistrySettings()
