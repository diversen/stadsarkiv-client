#!/usr/bin/env python
"""

Adds option for uses ordering materials from the archive to create the database tables.

export CONFIG_DIR=example-config-aarhus
./bin/orders.py

"""

import sys

sys.path.append(".")

from maya.core.dynamic_settings import settings
from maya.core.migration import Migration
from maya.migrations.orders import migrations_orders
from maya.core.logging import get_log
import os

# Check if the environment variable CONFIG_DIR is set
if "BASE_DIR" not in os.environ:
    print("Environment variable CONFIG_DIR is not set. E.g. set it like this:")
    print("export BASE_DIR=example-config-aarhus")
    exit(1)

log = get_log()

try:
    db_path = settings["sqlite3"]["orders"]
except KeyError:
    log.error("No database URL found in settings")
    exit(1)

migration_manager = Migration(db_path, migrations_orders)
migration_manager.run_migrations()
migration_manager.close()
