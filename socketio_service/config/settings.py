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

    # Variables for the Mongo database
    mongodb_host: str
    mongodb_port: int
    mongodb_name: str

    # Variables for RabbitMQ
    rabbit_host: str = "rabbitmq"
    rabbit_port: int = 5672
    rabbit_user: str = "guest"
    rabbit_pass: str = "guest"
    rabbit_vhost: str = "/"

    rabbit_pool_size: int = 2
    rabbit_channel_pool_size: int = 10

    # Digital ocean SPACES
    spaces_space_name: str
    spaces_access_key: str
    spaces_secret_key: str
    spaces_region_name: str

    # base host
    base_host: str

    @property
    def mongodb_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: mongodb URL.

        """
        return URL.build(
            scheme="mongodb",
            host=self.mongodb_host,
            port=self.mongodb_port,
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
