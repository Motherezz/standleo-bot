import aiosqlite
from datetime import datetime, timedelta
from config import DEFAULT_ELO

DB_NAME = "standleo.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                nickname TEXT,
                standleo_id TEXT UNIQUE,
                elo INTEGER DEFAULT 1000,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                tokens INTEGER DEFAULT 0,
                last_daily TIMESTAMP,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lobbies (
                lobby_id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER,
                channel_id INTEGER,
                host_id INTEGER,
                format TEXT,
                map TEXT,
                max_players INTEGER,
                players TEXT,
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pending_screens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lobby_id INTEGER,
                photo_file_id TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bans (
                user_id INTEGER PRIMARY KEY,
                reason TEXT,
                banned_by INTEGER,
                banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def register_user(user_id: int, username: str, nickname: str, standleo_id: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, username, nickname, standleo_id, elo) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, nickname, standleo_id, DEFAULT_ELO)
        )
        await db.commit()

async def get_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
            return await cursor.fetchone()

async def get_user_by_standleo(standleo_id: str):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE standleo_id = ?", (standleo_id,)) as cursor:
            return await cursor.fetchone()

async def update_elo(user_id: int, new_elo: int, win: bool = True):
    async with aiosqlite.connect(DB_NAME) as db:
        if win:
            await db.execute("UPDATE users SET elo = ?, wins = wins + 1 WHERE user_id = ?", (new_elo, user_id))
        else:
            await db.execute("UPDATE users SET elo = ?, losses = losses + 1 WHERE user_id = ?", (new_elo, user_id))
        await db.commit()

async def get_top_players(limit: int = 15):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT nickname, standleo_id, elo, wins, losses FROM users ORDER BY elo DESC LIMIT ?",
            (limit,)
        ) as cursor:
            return await cursor.fetchall()

async def create_lobby(host_id: int, format_: str, map_: str, max_players: int, message_id: int, channel_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "INSERT INTO lobbies (host_id, format, map, max_players, message_id, channel_id, players) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (host_id, format_, map_, max_players, message_id, channel_id, str(host_id))
        )
        await db.commit()
        return cursor.lastrowid

async def get_lobby(lobby_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM lobbies WHERE lobby_id = ?", (lobby_id,)) as cursor:
            return await cursor.fetchone()

async def update_lobby_players(lobby_id: int, players: str, status: str = "open"):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE lobbies SET players = ?, status = ? WHERE lobby_id = ?",
            (players, status, lobby_id)
        )
        await db.commit()

async def add_pending_screen(user_id: int, photo_file_id: str, lobby_id: int = None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO pending_screens (user_id, photo_file_id, lobby_id) VALUES (?, ?, ?)",
            (user_id, photo_file_id, lobby_id)
        )
        await db.commit()

async def ban_user(user_id: int, reason: str, banned_by: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO bans (user_id, reason, banned_by) VALUES (?, ?, ?)",
            (user_id, reason, banned_by)
        )
        await db.commit()

async def unban_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM bans WHERE user_id = ?", (user_id,))
        await db.commit()

async def is_banned(user_id: int) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
