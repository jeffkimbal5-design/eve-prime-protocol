import sqlite3
import json
import uuid
import os

DEFAULT_DB = os.path.expanduser("~/.kgr_memory.db")

def _ensure_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY, type TEXT NOT NULL, name TEXT NOT NULL,
            properties TEXT, world_id TEXT DEFAULT 'prime',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            access_count INTEGER DEFAULT 1, forget_weight REAL DEFAULT 0.0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS edges (
            id TEXT PRIMARY KEY, source_id TEXT NOT NULL, target_id TEXT NOT NULL,
            relation TEXT NOT NULL, properties TEXT, world_id TEXT DEFAULT 'prime',
            weight REAL DEFAULT 1.0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_id) REFERENCES nodes (id),
            FOREIGN KEY (target_id) REFERENCES nodes (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS worlds (
            id TEXT PRIMARY KEY, parent_id TEXT, description TEXT,
            status TEXT DEFAULT 'active', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES worlds (id)
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO worlds (id, description, status) VALUES ('prime', 'The primary baseline reality (EVE_PRIME)', 'active')")
    conn.commit()

class KGRMemory:
    def __init__(self, db_path=DEFAULT_DB):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        _ensure_db(self.conn)

    def add_node(self, name, node_type, properties=None, world_id='prime'):
        node_id = str(uuid.uuid4())
        props_json = json.dumps(properties or {})
        self.conn.cursor().execute(
            "INSERT INTO nodes (id, type, name, properties, world_id) VALUES (?, ?, ?, ?, ?)",
            (node_id, node_type, name, props_json, world_id)
        )
        self.conn.commit()
        return node_id

    def branch_world(self, parent_id, new_world_id, description):
        self.conn.cursor().execute(
            "INSERT INTO worlds (id, parent_id, description) VALUES (?, ?, ?)",
            (new_world_id, parent_id, description)
        )
        self.conn.commit()
        return new_world_id
