from sqlalchemy import (
    Table,
    MetaData,
    Column,
    String,
    ForeignKey,
    UUID,
    Numeric,
    DateTime,
    text,
)
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum, Text

from domain.enums import RiskLevelEnum

metadata = MetaData(
    naming_convention={
        "pk": "pk_%(table_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ix": "ix_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
    }
)
ethereum_address = Table(
    "ethereum_addresses",
    metadata,
    Column(
        "id",
        UUID,
        server_default=text("gen_random_uuid()"),
        primary_key=True,
    ),
    Column("wallet_address", String(42), unique=True, index=True, nullable=False),
)

analysis_result = Table(
    "analysis_results",
    metadata,
    Column("id", UUID, primary_key=True),
    Column(
        "wallet_address",
        ForeignKey(
            "ethereum_addresses.wallet_address", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    ),
    Column("correlation_id", UUID, nullable=False),
    Column(
        "level",
        SQLAlchemyEnum(
            RiskLevelEnum,
            name="risk_level_enum",
        ),
        nullable=False,
    ),
    Column("score", Numeric(10, 2), nullable=False),
    Column(
        "processed_at",
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
    ),
)

outbox = Table(
    "outbox",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("aggregate_type", String, nullable=False),
    Column("aggregate_id", UUID, nullable=False),
    Column("event_type", String, nullable=False),
    Column("payload", Text),
    Column(
        "timestamp",
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    ),
)
