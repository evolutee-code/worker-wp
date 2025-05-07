from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Tuple, Iterable, TypeVar
from ..enums import OrderBy
from ..models.base_model import BaseModel

T = TypeVar('T')


class AbstractRepository(ABC):
    """Abstract base class for repository pattern implementation using MySQL."""

    def __init__(self, table_name: str, db_pool):
        self.table_name = table_name
        self.db_pool = db_pool  # e.g., aiomysql pool

    @abstractmethod
    async def initialize(self):
        """Optional setup, like migrations or health checks."""
        ...

    @abstractmethod
    async def close(self):
        """Close database connection/pool."""
        ...

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Optional[BaseModel]:
        """Insert a new record."""
        ...

    @abstractmethod
    async def read(self, record_id: Any) -> Optional[BaseModel]:
        """Get a record by primary key."""
        ...

    @abstractmethod
    async def update_one_by(
            self,
            filter_query: Dict[str, Any],
            data: Dict[str, Any]
    ) -> Optional[T]:
        ...

    @abstractmethod
    async def update(self, record_id: Any, data: Dict[str, Any]) -> Optional[BaseModel]:
        """Update a record."""
        ...

    @abstractmethod
    async def delete(self, record_id: Any, soft_delete=False, user_id=None) -> bool:
        """Delete or soft-delete a record."""
        ...

    @abstractmethod
    async def list_alls(
        self,
        filter_query: Optional[Dict[str, Any]] = None,
        fields_limit: list | str = None,
        ignore_error: bool = False,
        include_deleted: bool = False
    ) -> Iterable[BaseModel]:
        """List all rows with optional filtering."""
        ...

    @abstractmethod
    async def count(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        """Count records."""
        ...

    @abstractmethod
    async def find_one(self, filter_query: Dict[str, Any], ignore_deleted: bool = True) -> Optional[BaseModel]:
        """Fetch one matching row."""
        ...

    @abstractmethod
    async def get_pagination(
        self,
        page: int = 0,
        limit: int = 20,
        fields: str = None,
        sort_by: str = None,
        order_by: OrderBy = OrderBy.DECREASE.value,
        search: str = None,
        filter_query: Optional[Dict[str, Any]] = None,
        include_deleted: bool = False,
        search_fields: List[str] = None
    ) -> Tuple[Iterable[BaseModel], int, int, int]:
        """Paginated and optionally searchable row list."""
        ...

