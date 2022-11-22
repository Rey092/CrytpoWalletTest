# -*- coding: utf-8 -*-
import enum
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings
from yarl import URL


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """
    Possible log levels.
    """

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured with environment variables.

    """

    base_dir: Path = Path(__file__).parent.parent

    # Site (or project) name
    site_name: str = "Test"
    # Base URL for the API.
    backend_url: str = "https://google.com"
    # The site name.
    frontend_url: str = "https://google.com"
    # quantity of workers for uvicorn
    workers_count: int = 3
    # Enable uvicorn reloading
    reload: bool = True
    # Current environment
    debug: bool = True

    # Secret key for signing jwt tokens
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_name: str = "access_token"
    jwt_access_expiration: int = 3600 * 24
    jwt_access_not_expiration: int = 3600 * 24 * 365

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_echo: bool = False

    # Variables for Redis
    redis_host: str
    redis_port: int
    redis_user: Optional[str] = None
    redis_pass: Optional[str] = None
    redis_base: Optional[str] = None
    redis_pool_size: int

    # Variables for RabbitMQ
    rabbit_host: str = "localhost"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    # Variables for SMTP
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    smtp_use_tls: bool
    smtp_use_ssl: bool
    smtp_mail_from: str
    display_name: str

    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    # Rate limit settings
    limit_login_times: int = 200
    limit_login_seconds: int = 60
    limit_register_times: int = 200
    limit_register_seconds: int = 60

    # Ethereum settings
    infura_api_url: str
    infura_api_key: str
    etherscan_api_url: str
    etherscan_api_key: str

    # Digital ocean SPACES
    spaces_space_name: str
    spaces_access_key: str
    spaces_secret_key: str
    spaces_region_name: str

    # superuser for sqladmin
    superuser_username: str
    superuser_password: str

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.

        """
        return URL.build(
            scheme="postgresql",
            host=self.postgres_host,
            port=self.postgres_port,
            user=self.postgres_user,
            password=self.postgres_password,
            path=f"/{self.postgres_db}",
        )

    @property
    def redis_url(self) -> URL:
        """
        Assemble REDIS URL from settings.

        :return: redis URL.

        """
        path = ""
        if self.redis_base is not None:
            path = f"/{self.redis_base}"
        return URL.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
            user=self.redis_user,
            password=self.redis_pass,
            path=path,
        )

    @property
    def rabbit_url(self) -> URL:
        """
        Assemble RabbitMQ URL from settings.

        :return: rabbit URL.

        """
        return URL.build(
            scheme="amqp",
            host=self.rabbit_host,
            port=self.rabbit_port,
            user=self.rabbit_user,
            password=self.rabbit_pass,
            path=self.rabbit_vhost,
        )

    @property
    def storage_url(self) -> URL:
        """
        Assemble Digital Ocean SPACES URL from settings.

        :return: storage URL.

        """
        return URL.build(
            scheme="https",
            host=f"{self.spaces_region_name}.digitaloceanspaces.com",
        )

    class Config:
        """
        Configure the application.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
