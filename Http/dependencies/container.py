from dependency_injector import containers, providers

from Http.implements.repositories.history_listing_repository import HistoryListingRepository
from Http.implements.repositories.store_repository import StoreRepository
from Http.services.history_listing_service import HistoryListingService
from Http.services.store_service import StoreService
from core import MySQLConnector


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

    history_listing_repository = providers.Factory(
        HistoryListingRepository,
        db_pool=db_pool
    )

    store_repository = providers.Factory(
        StoreRepository,
        db_pool=db_pool
    )

    history_listing_service = providers.Factory(
        HistoryListingService,
        history_listing_repository=history_listing_repository,
    )

    store_service = providers.Factory(
        StoreService,
        store_repository=store_repository,
    )
