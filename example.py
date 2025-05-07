from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from core.models.user_model import VDHUserInDB as UserModel  # update import accordingly
from core.repositories.base_repository import BaseRepository as BaseMySQLRepository  # use the new MySQL base
from dependency_injector import containers, providers
from core.database.mysql import MySQLConnector


class UserRepoInterface(BaseMySQLRepository, ABC):
    @abstractmethod
    async def find_by_email(self, item: Dict[str, Any]) -> Optional[UserModel]:
        pass


class UserRepository(UserRepoInterface):
    def __init__(self, db_pool):
        super().__init__(table_name="vdh_users", db_pool=db_pool, model=UserModel)

    async def find_by_email(self, item: Dict[str, Any]) -> Optional[UserModel]:
        return await self.find_one(item)


class UserService:
    def __init__(self, user_repository: UserRepoInterface):
        self.user_repo = user_repository

    async def find_by_email(self, email: str) -> Optional[UserModel]:
        return await self.user_repo.find_by_email({"email": email})

    async def find_by_id(self, id: int) -> Optional[UserModel]:
        return await self.user_repo.read(id)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["__main__"])

    # Create a provider for MySQLConnector
    mysql_connector = providers.Singleton(MySQLConnector)

    # Create a provider for the DB pool
    # Important: Use Factory instead of Resource for async resources
    db_pool = providers.Factory(
        lambda connector: connector.connect(),
        connector=mysql_connector
    )

    # Repository and service providers
    user_repository = providers.Factory(
        UserRepository,
        db_pool=db_pool
    )

    user_service = providers.Factory(
        UserService,
        user_repository=user_repository
    )


async def main():
    # Create container
    container = Container()

    # Get MySQL connector instance
    mysql_connector = container.mysql_connector()

    # Connect to database - await the coroutine
    db_pool = await container.db_pool()

    # Create repository with the connected pool
    user_repository = container.user_repository(db_pool=db_pool)

    # Create service with the repository
    user_service = container.user_service(user_repository=user_repository)

    # Use the service
    try:
        found_user = await user_service.find_by_email("mrson2828@gmail.com")
        if found_user:
            print("found_user", found_user)

        find_user = await user_service.find_by_id(1)
        if find_user:
            print("find_user", find_user)
    finally:
        # Cleanup: close the database connection
        if mysql_connector.pool:
            await mysql_connector.close()


if __name__ == "__main__":
    import asyncio

    # Print debug information
    import os

    print(f"Current working directory: {os.getcwd()}")
    print(f".env file exists: {os.path.exists('.env')}")

    asyncio.run(main())