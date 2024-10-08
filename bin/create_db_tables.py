"""
stadsarkiv-client exec -c example-config-aarhus -s bin/create_db_tables.py
"""

from stadsarkiv_client.core.dynamic_settings import init_settings
import sqlite3
import os
from stadsarkiv_client.core.logging import get_log

init_settings()
log = get_log()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")


conn = sqlite3.connect(DATABASE_URL)
cursor = conn.cursor()

create_migrations_table = """
CREATE TABLE IF NOT EXISTS migrations (
    id INTEGER PRIMARY KEY,
    migration_key VARCHAR(128),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def create_migrations_table_if_not_exists():
    cursor.execute(create_migrations_table)
    conn.commit()
    log.debug("Migrations table created (if not exists)")


create_migrations_table_if_not_exists()

create_booksmarks_query = """
CREATE TABLE IF NOT EXISTS bookmarks (
    id INTEGER PRIMARY KEY,
    bookmark VARCHAR(128),
    user_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_booksmarks_index_query = """
CREATE INDEX IF NOT EXISTS idx_bookmarks_user_id ON bookmarks (user_id);
"""

create_searches_query = """
CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY,
    search VARCHAR(1024),
    title VARCHAR(256),
    user_id VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

create_searches_index_query = """
CREATE INDEX IF NOT EXISTS idx_searches_user_id ON searches (user_id);
"""

create_cache_query = """
CREATE TABLE IF NOT EXISTS cache (
    id INTEGER PRIMARY KEY,
    key VARCHAR(128),
    value TEXT,
    unix_timestamp INTEGER DEFAULT 0
);
"""

create_cache_index_query = """
CREATE INDEX IF NOT EXISTS idx_cache_key ON cache (key);
"""

# List of migrations with keys
migrations = {
    "create_bookmarks": create_booksmarks_query,
    "create_bookmarks_index": create_booksmarks_index_query,
    "create_searches": create_searches_query,
    "create_searches_index": create_searches_index_query,
    "create_cache": create_cache_query,
    "create_cache_index": create_cache_index_query,
}


def has_migration_been_applied(migration_key):
    cursor.execute("SELECT 1 FROM migrations WHERE migration_key = ?", (migration_key,))
    return cursor.fetchone() is not None


def apply_migration(migration_key, sql):
    if not has_migration_been_applied(migration_key):
        cursor.execute(sql)
        conn.commit()
        log.debug(f"SQL for {migration_key} executed")
        cursor.execute("INSERT INTO migrations (migration_key) VALUES (?)", (migration_key,))
        conn.commit()
        log.debug(f"Migration {migration_key} recorded")


def create_tables():
    for migration_key, sql in migrations.items():
        apply_migration(migration_key, sql)


create_tables()
conn.close()