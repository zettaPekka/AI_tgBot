from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.init_database import engine, User


async_session = async_sessionmaker(bind=engine)

async def add_user_if_not_exists(tg_id: int):
    async with async_session() as session:
        user = await session.get(User, tg_id)
        if user is None:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()

async def get_context(tg_id: int):
    async with async_session() as session:
        user = await session.get(User, tg_id)
    return user.chat_context

async def update_context(tg_id: int, context: list):
    async with async_session() as session:
        user = await session.get(User, tg_id)
        context = context if len(context) <= 50 else context[2:]
        user.chat_context = context
        await session.commit()

async def reset_context(tg_id: int):
    async with async_session() as session:
        user = await session.get(User, tg_id)
        user.chat_context = None
        await session.commit()

async def amount_of_users():
    async with async_session() as session:
        amount = await session.scalar(func.count(User.tg_id))
        return amount

async def get_all_users_id():
    async with async_session() as session:
        users = await session.execute(select(User.tg_id))
        users = users.scalars().all()
        return users