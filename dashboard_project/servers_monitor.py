"""
Мониторинг серверов видеонаблюдения Трассир через Интернет
Автор: Евгений Петров
Почта: p174@mail.ru, epoy74@gmail.com
"""

import asyncio
import json
import logging
import os

import aiohttp
import asyncpg
import dotenv
from pydantic import BaseModel, ValidationError

# --- конфигурация и .env ---
dotenv.load_dotenv()
DVR_USERNAME = os.getenv("USERNAME")
DVR_PASSWORD = os.getenv("PASSWORD")
SERVERS = os.getenv("SERVERS", "").split(",")

DB_DSN = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
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
    logging.debug(f"[{ip}] Попытка входа: {DVR_USERNAME} {DVR_PASSWORD}")
    try:
        url = f"https://{ip}:8080/login"
        async with session.post(
            url,
            params={
                "username": DVR_USERNAME or "", 
                "password": DVR_PASSWORD or ""
                },
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
        raw_json = json.dumps(data.model_dump(mode="json"))
        await conn.execute(
            """
            INSERT INTO server_health (
                ip,  timestamp,
                channels_total, channels_online, cpu_load, uptime,
                disks_ok, database_ok, network_ok, automation_ok,
                disks_stat_main_days, disks_stat_priv_days,
                disks_stat_subs_days, raw
            ) VALUES (
                $1, NOW(), $2,
                $3, $4, $5, $6,
                $7, $8, $9, $10,
                $11, $12, $13
            )
            """,
            ip,
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
            raw_json,
        )
        # await conn.commit()
    except Exception as e:
        logging.error(f"[{ip}] Ошибка записи в БД: {e}")


async def monitor_server(ip: str, session: aiohttp.ClientSession, pool):
    ip = ip.strip()
    sid = await get_sid(session, ip)
    if sid:
        health_data = await get_health(session, ip, sid)
        if health_data:
            logging.info(
                f"[{ip}] channels_online={health_data.channels_online}, "
                f"cpu={health_data.cpu_load:.1f}%"
            )
            async with pool.acquire() as conn:
                await save_to_db(conn, ip, health_data) 


async def main():
    pool = await asyncpg.create_pool(dsn=DB_DSN, max_size=15)
    async with aiohttp.ClientSession() as session:
        while True:
            # async with pool.acquire() as conn:
            tasks = [monitor_server(ip, session, pool) for ip in SERVERS]
            await asyncio.gather(*tasks)
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
