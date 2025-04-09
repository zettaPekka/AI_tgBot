from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database.crud import add_user_if_not_exists, reset_context
import components.keyboards.user_kb as kb
from components.states.user_states import Chat
from ai_api.generate import answer_to_text_prompt


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('привет это бот с нейросетью',
                            reply_markup=kb.start_kb)
    await add_user_if_not_exists(tg_id=message.from_user.id)

@router.callback_query(F.data == 'start_dialog')
async def start_dialog(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'Chat:active':
        await callback.answer('Диалог уже начат')
        await callback.message.answer('Диалог уже активен')
    else:
        await callback.message.answer('Диалог успешно начат')
        await callback.answer('Диалог начат')
        await state.set_state(Chat.active)

@router.message(Command('stop'))
async def stop(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'Chat:active':
        await state.clear()
        await message.answer('Диалог остановлен')
    elif current_state == 'Chat:waiting':
        await message.answer('Дождитесь ответа, чтобы закончить диалог')
    else:
        await message.answer('Нет активного диалога')

@router.message(Command('reset'))
async def reset(message: Message):
    await reset_context(tg_id=message.from_user.id)
    await message.answer('Контекст очищен')

@router.message(Chat.active)
async def chat_active(message: Message, state: FSMContext): 
    current_state = await state.get_state()
    if current_state == 'Chat:waiting':
        await message.answer('Дождитесь ответа')
    else:
        if message.content_type == ContentType.TEXT:
            await state.set_state(Chat.waiting)
            ai_response = await answer_to_text_prompt(main_prompt=message.text, tg_id=message.from_user.id)
            await message.answer(ai_response)
            await state.set_state(Chat.active)