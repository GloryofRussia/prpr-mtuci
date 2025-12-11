from backend import config
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

url = (
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}"
    f"@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}"
    "?charset=utf8mb4"
)

engine = create_engine(url, pool_pre_ping=True, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()