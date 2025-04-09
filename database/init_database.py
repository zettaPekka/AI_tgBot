from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import BigInteger, JSON
from dotenv import load_dotenv

import os


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    tg_id = mapped_column(BigInteger, primary_key=True)
    chat_context: Mapped[list] = mapped_column(JSON, nullable=True)


load_dotenv()

engine = create_async_engine(os.getenv('DB_PATH'))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


