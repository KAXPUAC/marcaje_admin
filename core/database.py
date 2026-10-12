import oracledb
from core.config import settings

pool = None


def init_db_pool():
    global pool
    # Habilitar modo grueso/fino según configuración del driver
    pool = oracledb.create_pool(
        user=settings.ORACLE_USER,
        password=settings.ORACLE_PASSWORD,
        dsn=settings.ORACLE_DNS,
        min=2,
        max=10,
        increment=1
    )


def get_connection():
    if pool is None:
        init_db_pool()
    return pool.acquire()
