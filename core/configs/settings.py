import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

import logging

logger = logging.getLogger(__name__)


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Load environment variables from .env file
        self._load_env_file()

        # Application settings
        self.API_V1_STR = "/api/v1"
        self.PROJECT_NAME = " Package"
        self.TIMEZONE = os.getenv("TIMEZONE", "+07:00")

        # Auth settings
        self.USER_BASIC_AUTH = os.getenv("USER_BASIC_AUTH", "")
        self.PASSWORD_BASIC_AUTH = os.getenv("PASSWORD_BASIC_AUTH", "")
        self.AUTHENTICATION_TOKEN = os.getenv("AUTHENTICATION_TOKEN", "")

        # MySQL settings
        self.MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
        self.MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
        self.MYSQL_USER = os.getenv('MYSQL_USER', '')
        self.MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
        self.MYSQL_DB = os.getenv('MYSQL_DB', '')

        # Redis settings
        self.REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
        self.REDIS_PORT = os.getenv("REDIS_PORT", '6379')
        self.REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", '')

        # Kafka settings
        self.KAFKA_HOST = os.getenv("KAFKA_HOST", 'localhost')
        self.KAFKA_PORT = os.getenv("KAFKA_PORT", '9092')
        self.BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", 'localhost:9092')

        # Log loaded configuration
        self._log_config()

    def _load_env_file(self) -> None:
        """
        Loads environment variables from .env file in multiple possible locations.
        """
        # Try to find .env file
        env_file = find_dotenv()
        if env_file:
            load_dotenv(env_file)
            logger.info(f"Loaded environment from: {env_file}")
            return

        # Fallback to check multiple locations
        possible_locations = [
            '.env',  # Current directory
            Path(__file__).parent / '.env',  # Module directory
            Path(__file__).parent.parent / '.env',  # Project root directory
        ]

        for location in possible_locations:
            if Path(location).is_file():
                load_dotenv(location)
                logger.info(f"Loaded environment from: {location}")
                return

        logger.warning("No .env file found. Using environment variables if available.")

    def _log_config(self) -> None:
        """Log configuration (with masked passwords)."""
        logger.info(f"Settings initialized for {self.PROJECT_NAME}")
        logger.info(f"MySQL: {self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}")

    @property
    def MYSQL_URI(self) -> str:
        """Get the MySQL connection URI."""
        if self.MYSQL_USER and self.MYSQL_PASSWORD:
            return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        return f"mysql+aiomysql://{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"


settings = Settings()
