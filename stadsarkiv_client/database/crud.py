"""
Small CRUD class to handle basic database operations.

```
from stadsarkiv_client.database.crud import CRUD

DATABASE_ORDERS = "orders"
orders_crud = CRUD(DATABASE_ORDERS, "orders")

async def example():
    await orders_crud.insert({"order_id": 1, "order_name": "order1"})
    await orders_crud.insert({"order_id": 2, "order_name": "order2"})

    many_orders = [
        {"order_id": 3, "order_name": "test"},
        {"order_id": 4, "order_name": "test"},
    ]
    await orders_crud.insert_many(many_orders)

    await orders_crud.select(
        columns=["order_id"],
        filters={"order_name": "test"},
        order_by=[("order_id", "ASC")],
        limit_offset=(2, 0),
    )

    await orders_crud.exists({"order_name": "test"})
    await orders_crud.update({"order_name": "new test"}, {"order_id": 3})
    await orders_crud.delete({"order_id": 4})

class OrdersCRUD(CRUD):
    # Or extend CRUD with specific methods for orders.
    pass

```
"""

import sqlite3
from stadsarkiv_client.database.utils import transaction_scope
from stadsarkiv_client.core.logging import get_log
from stadsarkiv_client.database.sql_builder import SQLBuilder

log = get_log()


class CRUD:
    def __init__(self, database: str, table: str):
        self.database = database
        self.table = table
        self.sql_builder = SQLBuilder(self.table)

    async def insert(self, insert_values: dict):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_insert(insert_values)
                connection.execute(query, insert_values)
            except sqlite3.Error as e:
                raise e

    async def insert_many(self, insert_values_many: list):
        async with transaction_scope(self.database) as connection:
            try:
                for single_data in insert_values_many:
                    query = self.sql_builder.build_insert(single_data)
                    connection.execute(query, single_data)
            except sqlite3.Error as e:
                raise e

    async def select(self, columns: list = [], filters: dict = {}, order_by: list = [], limit_offset: tuple = ()):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_select(
                    columns=columns,
                    filters=filters,
                    order_by=order_by,
                    limit_offset=limit_offset,
                )
                result = connection.execute(query, filters)
                rows = result.fetchall()
                return rows
            except sqlite3.Error as e:
                raise e

    async def exists(self, filters: dict):
        rows = await self.select(filters=filters)
        return bool(rows)

    async def update(self, update_values: dict, filters: dict):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_update(update_values, filters)
                connection.execute(query, update_values)
            except sqlite3.Error as e:
                raise e

    async def delete(self, filters: dict):
        async with transaction_scope(self.database) as connection:
            try:
                query = self.sql_builder.build_delete(filters)
                connection.execute(query, filters)
            except sqlite3.Error as e:
                raise e
