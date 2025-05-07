import aiomysql
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, TypeVar, Union
from ..models.base_model import BaseModel
from ..enums import OrderBy
from ..contracts.abstract_repository import AbstractRepository

T = TypeVar("T", bound=BaseModel)


class BaseRepository(AbstractRepository):
    def __init__(self, table_name: str, db_pool, model: Type[T]):
        super().__init__(table_name, db_pool)
        self.model = model

    async def initialize(self):
        # Optional: e.g., ping connection or run migrations
        async with self.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")

    async def close(self):
        self.db_pool.close()
        await self.db_pool.wait_closed()

    async def create(self, data: Dict[str, Any]) -> Optional[T]:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

        async with self.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, values)
                await conn.commit()
                inserted_id = cur.lastrowid
                return await self.read(inserted_id)

    async def read(self, record_id: Any) -> Optional[T]:
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        async with self.db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, (record_id,))
                row = await cur.fetchone()
                if row:
                    return self.model(**row)
                return None

    async def update_one_by(
            self,
            filter_query: Dict[str, Any],
            data: Dict[str, Any]
    ) -> Optional[T]:
        """
        Update a single record that matches the filter criteria.

        Args:
            filter_query (Dict[str, Any]): Conditions to filter the record to update
                Can use special operators like field__gt, field__like, etc.
                Example: {"email": "user@example.com", "status": 1}

            data (Dict[str, Any]): Fields and values to update
                Example: {"status": 2, "updated_at": "2023-05-06 12:00:00"}

        Returns:
            Optional[T]: Updated model instance or None if no record found

        Example:
            >>> # Update a user by email
            >>> updated_user = await repo.update_one_by(
            ...     filter_query={"email": "user@example.com"},
            ...     data={"status": 2, "last_login": datetime.now()}
            ... )
        """
        # First find the record that matches the criteria
        record = await self.find_one(filter_query)

        # If no record matches, return None
        if not record:
            return None

        # Get the ID of the found record
        record_id = getattr(record, "id")

        # Create SET clause with placeholders
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])

        # Values for the SET clause come first, followed by the ID
        values = list(data.values()) + [record_id]

        # Construct the full SQL query
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"

        # Perform the update
        async with self.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                # Execute the update query
                await cur.execute(query, values)

                # Commit the transaction
                await conn.commit()

                # Re-fetch the updated record to get its current state
                # We can use the find_one method to get it by ID
                return await self.find_one({"id": record_id})

    async def update(self, record_id: Any, data: Dict[str, Any]) -> Optional[T]:
        """
              Update a record in the database.

              Args:
                  record_id (Any): Primary key value
                  data (Dict[str, Any]): Key-value pairs of fields to update

              Returns:
                  Optional[T]: Updated model instance or None if not found

              Example:
                  >>> await repo.update(1, {"name": "New Name", "status": 2})
        """
        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        values = list(data.values()) + [record_id]
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"

        async with self.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, values)
                await conn.commit()
                return await self.read(record_id)

    async def delete(self, record_id: Any, soft_delete=False, user_id=None) -> bool:
        if soft_delete:
            query = f"UPDATE {self.table_name} SET deleted_at = NOW(), deleted_by = %s WHERE id = %s"
            params = (user_id, record_id)
        else:
            query = f"DELETE FROM {self.table_name} WHERE id = %s"
            params = (record_id,)

        async with self.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, params)
                await conn.commit()
                return cur.rowcount > 0

    async def count(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        where_clause, values = self._build_where_clause(filter_query)
        query = f"SELECT COUNT(*) as count FROM {self.table_name} {where_clause}"

        async with self.db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, values)
                row = await cur.fetchone()
                return row['count'] if row else 0

    async def find_one(
            self,
            filter_query: Dict[str, Any],
            ignore_deleted: bool = True
    ) -> Optional[T]:
        where_clause, values = self._build_where_clause(filter_query, not ignore_deleted)
        query = f"SELECT * FROM {self.table_name} {where_clause} LIMIT 1"

        async with self.db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, values)
                row = await cur.fetchone()
                if row:
                    return self.model(**row)
                return None

    async def get_pagination(
            self,
            page: int = 1,
            limit: int = 20,
            fields: str = "*",
            sort_by: str = "id",
            order_by: OrderBy = OrderBy.DECREASE.value,
            search: str = None,
            filter_query: Optional[Dict[str, Any]] = None,
            include_deleted: bool = False,
            search_fields: List[str] = None
    ) -> Tuple[Iterable[T], int, int, int]:

        offset = (page - 1) * limit
        where_clause, values = self._build_where_clause(filter_query, include_deleted)

        if search and search_fields:
            search_condition = " OR ".join([f"{field} LIKE %s" for field in search_fields])
            search_values = [f"%{search}%"] * len(search_fields)
            where_clause = f"{where_clause} AND ({search_condition})" if where_clause else f"WHERE {search_condition}"
            values += search_values

        order_clause = f"ORDER BY {sort_by} {'ASC' if order_by == OrderBy.INCREASE.value else 'DESC'}"
        query = f"SELECT {fields} FROM {self.table_name} {where_clause} {order_clause} LIMIT %s OFFSET %s"
        values.extend([limit, offset])

        async with self.db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, values)
                rows = await cur.fetchall()

                # Count query
                count_query = f"SELECT COUNT(*) as count FROM {self.table_name} {where_clause}"
                await cur.execute(count_query, values[:-2])
                total = (await cur.fetchone())["count"]

        total_pages = (total + limit - 1) // limit
        return [self.model(**row) for row in rows], total, total_pages, page

    async def list_alls(
            self,
            filter_query: Optional[Dict[str, Any]] = None,
            fields_limit: Union[List[str], str] = None,
            ignore_error: bool = False,
            include_deleted: bool = False
    ) -> Iterable[T]:
        """
        Retrieve multiple records from the database table based on filter criteria.

        Args:
            filter_query (Optional[Dict[str, Any]]): Dictionary of field-value pairs to filter records
                Supports operators using double underscore notation:
                - field__gt: Greater than
                - field__lt: Less than
                - field__gte: Greater than or equal
                - field__lte: Less than or equal
                - field__ne: Not equal
                - field__like: LIKE query (adds % wildcards automatically)
                - field__in: IN query (value should be a list)
                - field__isnull: IS NULL (if value is True) or IS NOT NULL (if value is False)
                Example: {"age__gt": 18, "status": "active", "note__isnull": False}

            fields_limit (Union[List[str], str]): Limit the fields returned in the query
                Can be either:
                - A list of field names: ["id", "name", "created_at"]
                - A string with comma-separated fields: "id, name, created_at"
                - None: Returns all fields (*)

            ignore_error (bool): Whether to suppress exceptions and return empty list on error

            include_deleted (bool): Whether to include soft-deleted records
                If the model has a deleted_at field, this controls whether to include
                records where deleted_at is not NULL

        Returns:
            Iterable[T]: List of model instances matching the criteria

        Raises:
            Exception: Database errors unless ignore_error is True
        """
        try:
            # Build the WHERE clause from filter conditions
            where_clause, values = self._build_where_clause(filter_query, include_deleted)

            # Determine which fields to select
            if isinstance(fields_limit, list):
                fields = ", ".join(fields_limit)
            elif isinstance(fields_limit, str):
                fields = fields_limit
            else:
                fields = "*"

            # Construct the full SQL query
            query = f"SELECT {fields} FROM {self.table_name} {where_clause}"

            # Execute the query
            async with self.db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cur:
                    await cur.execute(query, values)
                    rows = await cur.fetchall()

                    # Convert raw data to model instances
                    # return [self.model(**row) for row in rows]
                    return [row for row in rows]

        except Exception as e:
            if ignore_error:
                return []
            raise e

    @staticmethod
    def _build_where_clause(
            filter_query: Optional[Dict[str, Any]] = None,
            include_deleted: bool = False
    ) -> tuple:
        """
        Build a WHERE clause for SQL queries based on the filter criteria.
        Supports NULL/NOT NULL checks with special operators.

        Args:
            filter_query (Optional[Dict[str, Any]]): Key-value pairs for filtering
            include_deleted (bool): Whether to include soft-deleted records

        Returns:
            tuple: (where_clause_string, parameter_values)
        """
        conditions = []
        values = []

        # Add conditions from filter query
        if filter_query:
            for key, value in filter_query.items():
                # Special case for IS NULL and IS NOT NULL
                if "__isnull" in key:
                    field = key.split("__isnull")[0]
                    if value:  # If True, check for NULL
                        conditions.append(f"{field} IS NULL")
                    else:  # If False, check for NOT NULL
                        conditions.append(f"{field} IS NOT NULL")
                    continue  # Skip regular value handling

                # Handle different operators in keys (e.g., "age__gt")
                if "__" in key:
                    field, operator = key.split("__", 1)
                    if operator == "gt":
                        conditions.append(f"{field} > %s")
                    elif operator == "lt":
                        conditions.append(f"{field} < %s")
                    elif operator == "gte":
                        conditions.append(f"{field} >= %s")
                    elif operator == "lte":
                        conditions.append(f"{field} <= %s")
                    elif operator == "ne":
                        conditions.append(f"{field} != %s")
                    elif operator == "like":
                        conditions.append(f"{field} LIKE %s")
                        value = f"%{value}%"  # Add wildcards for LIKE
                    elif operator == "in":
                        placeholders = ", ".join(["%s"] * len(value))
                        conditions.append(f"{field} IN ({placeholders})")
                        values.extend(value)
                        continue  # Skip appending value since we've already extended the list
                    else:
                        conditions.append(f"{field} = %s")
                else:
                    if value is None:
                        # Handle NULL value with IS NULL
                        conditions.append(f"{key} IS NULL")
                        continue  # Skip appending NULL values to values list
                    else:
                        conditions.append(f"{key} = %s")

                values.append(value)

        # Add soft delete condition if applicable
        # if not include_deleted and hasattr(self.model, "deleted_at"):
        #     conditions.append("deleted_at IS NULL")

        # Construct the final WHERE clause
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        else:
            where_clause = ""

        return where_clause, tuple(values)
