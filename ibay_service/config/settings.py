# -*- coding: utf-8 -*-
from pathlib import Path

from pydantic import BaseSettings
from yarl import URL


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured with environment variables.

    """

    base_dir: Path = Path(__file__).parent.parent

    # quantity of workers for uvicorn
    workers_count: int = 3
    # Enable uvicorn reloading
    reload: bool = True
    # Current environment
    debug: bool = True

    # Variables for the IBay database
    ibay_postgres_host: str = "localhost"
    ibay_postgres_port: int = 5432
    ibay_postgres_user: str
    ibay_postgres_password: str
    ibay_postgres_db: str
    ibay_postgres_echo: bool = False

    # Variables for RabbitMQ
    rabbit_host: str = "localhost"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    @property
    def ibay_db_url(self) -> URL:
        """
        Assemble IBay database URL from settings.

        :return: IBay database URL.

        """
        return URL.build(
            scheme="postgresql",
            host=self.ibay_postgres_host,
            port=self.ibay_postgres_port,
            user=self.ibay_postgres_user,
            password=self.ibay_postgres_password,
            path=f"/{self.ibay_postgres_db}",
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

    class Config:
        """
        Configure the application.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
