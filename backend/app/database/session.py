import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from app.core.config import settings

logger = logging.getLogger("app.database")

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

def check_db_connectivity() -> bool:
    """
    Check if the database connection is available.
    Returns True if connected successfully, False otherwise.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connectivity verified successfully!")
        return True
    except OperationalError as e:
        logger.warning(
            f"⚠️ Database is not reachable at startup. Platform will run in mock mode. "
            f"Details: {e}"
        )
        return False
    except Exception as e:
        logger.warning(
            f"⚠️ Unexpected error checking database connectivity: {e}. Platform will run in mock mode."
        )
        return False