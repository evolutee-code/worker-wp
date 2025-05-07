import os
from pathlib import Path
from typing import Optional, Dict, Any, Union
from dotenv import load_dotenv
import aiomysql
import pymysql

from ..configs import settings
from ..logger import logger

class MySQLConnector:
    """Asynchronous MySQL database connector using aiomysql."""

    def __init__(self, env_path: Optional[str] = None):
        """
        Initialize MySQL connector.

        Args:
            env_path (str, optional): Path to .env file. If None, looks in the current
                                      working directory and package directory.
        """
        self.pool = None
        self.connection = None
        self._load_env(env_path)
        self._connection_params = self._get_connection_params()

    @staticmethod
    def _load_env(env_path: Optional[str] = None) -> None:
        """
        Load environment variables from .env a file.

        First checks the provided path, then the current working directory, then the package installation directory.

        Args:
            env_path (str, optional): Path to .env file.
        """
        # Try loading from a provided path
        if env_path and os.path.isfile(env_path):
            load_dotenv(env_path)
            logger.info(f"Loaded .env from provided path: {env_path}")
            return

        # Try loading from the current directory
        if os.path.isfile('.env'):
            load_dotenv()
            logger.info("Loaded .env from current directory")
            return

        # Try loading from the package directory
        package_dir = Path(__file__).parent
        package_env = package_dir / '.env'
        if package_env.is_file():
            load_dotenv(package_env)
            logger.info(f"Loaded .env from package directory: {package_env}")
            return

        logger.warning("No .env file found. Using environment variables if available.")

    def _get_connection_params(self) -> Dict[str, Any]:
        """
        Get MySQL connection parameters from environment variables.

        Returns:
            dict: MySQL connection parameters
        """

        # Get connection parameters from settings
        host = getattr(settings, 'MYSQL_HOST', os.getenv('MYSQL_HOST', 'localhost'))
        port = getattr(settings, 'MYSQL_PORT', os.getenv('MYSQL_PORT', '3306'))
        user = getattr(settings, 'MYSQL_USER', os.getenv('MYSQL_USER', ''))
        password = getattr(settings, 'MYSQL_PASSWORD', os.getenv('MYSQL_PASSWORD', ''))

        # Build connection parameters
        conn_params = {
            "host": host,
            "port": int(port) if port else 3306,
            "user": user,
        }

        # Add a password if provided
        if password:
            conn_params["password"] = password

        return conn_params

    async def connect(self, db_name: Optional[str] = None) -> aiomysql.Connection:
        """
        Connect to MySQL asynchronously.

        Args:
            db_name (str, optional): Database name. Defaults to MYSQL_DB from .env.

        Returns:
            aiomysql.Connection: MySQL connection instance

        Raises:
            ConnectionError: If connection fails
        """
        if not db_name:
            db_name = settings.MYSQL_DB
            if not db_name:
                raise ValueError("Database name must be provided either as parameter or in .env as MYSQL_DB")

        try:
            # Create a connection pool
            self.pool = await aiomysql.create_pool(
                **self._connection_params,
                db=db_name,
                autocommit=True
            )

            # Get a connection from the pool to test it
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT 1")
                    result = await cursor.fetchone()
                    if result and result[0] == 1:
                        logger.info(f"Successfully connected to MySQL database: {db_name}")
                    else:
                        raise ConnectionError("Failed to verify MySQL connection")

            return self.pool

        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            error_msg = f"Failed to connect to MySQL: {str(e)}"
            logger.error(error_msg)
            raise ConnectionError(error_msg)

    async def execute_query(self, query: str, params: Optional[tuple] = None) -> Any:
        """
        Execute a query on the connected database.

        Args:
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query

        Returns:
            Any: Query result

        Raises:
            ConnectionError: If not connected to database
        """
        if self.pool is None:
            raise ConnectionError("Not connected to database. Call connect() first.")

        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, params)
                    if query.strip().upper().startswith(("SELECT", "SHOW")):
                        return await cursor.fetchall()
                    return None
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise

    async def get_table(self, table_name: str) -> Any:
        """
        Get a reference to a table (similar to a collection in MongoDB).
        This is just a convenience method that returns the table name.

        Args:
            table_name (str): Name of the table

        Returns:
            str: Table name

        Raises:
            ConnectionError: If not connected to a database
        """
        if self.pool is None:
            raise ConnectionError("Not connected to database. Call connect() first.")

        return table_name

    async def init_db(self):
        """Initialize database tables and indexes."""
        try:
            logger.info("Database initialized successfully")

        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    async def close(self) -> None:
        """Close the MySQL connection pool asynchronously."""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection closed")
            self.pool = None

