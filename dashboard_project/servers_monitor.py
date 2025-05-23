"""
Мониторинг серверов видеонаблюдения Трассир через Интернет
Автор: Евгений Петров
Почта: p174@mail.ru, epoy74@gmail.com
"""

import asyncio
import logging
import os
from typing import Optional

import aiohttp
import asyncpg
import dotenv
from pydantic import BaseModel, ValidationError

# --- конфигурация и .env ---
dotenv.load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SERVERS = os.getenv("SERVERS", "").split(",")

DB_DSN = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# --- pydantic модель для ответа health ---
class HealthResponse(BaseModel):
    disks: str
    database: str
    channels_total: int
    channels_online: int
    uptime: int
    cpu_load: float
    network: str
    automation: str
    disks_stat_main_days: float
    disks_stat_priv_days: float
    disks_stat_subs_days: float


async def get_sid(session: aiohttp.ClientSession, ip: str) -> str | None:
    try:
        url = f"https://{ip}:8080/login"
        async with session.get(
            url,
            params={"username": USERNAME or "", "password": PASSWORD or ""},
            ssl=False,
            timeout=aiohttp.ClientTimeout(total=5),
        ) as resp:
            data = await resp.json()
            return data.get("sid")
    except Exception as e:
        logging.error(f"[{ip}] Ошибка авторизации: {e}")
        return None


async def get_health(
    session: aiohttp.ClientSession, ip: str, sid: str
) -> HealthResponse | None:
    try:
        url = f"https://{ip}:8080/health"
        async with session.get(
            url,
            params={"sid": sid},
            ssl=False,
            timeout=aiohttp.ClientTimeout(total=5),
        ) as resp:
            data = await resp.json()
            return HealthResponse(**data)
    except (aiohttp.ClientError, ValidationError, Exception) as e:
        logging.error(f"[{ip}] Ошибка получения или валидации health: {e}")
        return None


async def save_to_db(conn, ip: str, data: HealthResponse):
    try:
        await conn.execute(
            """
            INSERT INTO server_health (
                ip, raw, timestamp,
                channels_total, channels_online, cpu_load, uptime,
                disks_ok, database_ok, network_ok, automation_ok,
                disks_stat_main_days, disks_stat_priv_days, disks_stat_subs_days
            ) VALUES (
                $1, $2, NOW(),
                $3, $4, $5, $6,
                $7, $8, $9, $10,
                $11, $12, $13
            )
            """,
            ip,
            data.dict(),
            data.channels_total,
            data.channels_online,
            data.cpu_load,
            data.uptime,
            data.disks == "1",
            data.database == "1",
            data.network == "1",
            data.automation == "1",
            data.disks_stat_main_days,
            data.disks_stat_priv_days,
            data.disks_stat_subs_days,
        )
    except Exception as e:
        logging.error(f"[{ip}] Ошибка записи в БД: {e}")


async def monitor_server(ip: str, session: aiohttp.ClientSession, conn):
    ip = ip.strip()
    sid = await get_sid(session, ip)
    if sid:
        health_data = await get_health(session, ip, sid)
        if health_data:
            logging.info(
                f"[{ip}] channels_online={health_data.channels_online}, "
                f"cpu={health_data.cpu_load:.1f}%"
            )
            await save_to_db(conn, ip, health_data)


async def main():
    pool = await asyncpg.create_pool(dsn=DB_DSN)
    async with aiohttp.ClientSession() as session:
        while True:
            async with pool.acquire() as conn:
                tasks = [monitor_server(ip, session, conn) for ip in SERVERS]
                await asyncio.gather(*tasks)
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
