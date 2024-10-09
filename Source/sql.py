import sqlite3 as sql

db_path = 'Source\\database.db'


def connect():
    connection = sql.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS releases (
                id      INTEGER PRIMARY KEY AUTOINCREMENT
                        UNIQUE ON CONFLICT REPLACE
                        NOT NULL ON CONFLICT FAIL,
                day     INTEGER,
                month   INTEGER NOT NULL,
                desc    TEXT,
                value   REAL
            );
        """
    )

    return connection, cursor
