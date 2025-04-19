from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.crud import add_user_if_not_exists, reset_context
import components.keyboards.user_kb as kb
from components.states.user_states import Chat
from api.ai_api.generate_text import answer_to_text_prompt, answer_to_view_prompt
from api.ai_api.text_formatting import style_changer


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('<b>👋 Привет! Я — умный бот с нейросетью!\n\nЧто я умею?\n• Отвечать на вопросы\n• Писать тексты: статьи, посты, стихи и даже код\n• Анализировать картинки (что на фото?)\n• Помогать с идеями и советами\n\nКоманды:\n<i>/start - запуск бота\n/generate - начать диалог\n/stop - закончить диалог\n/reset - сбросить историю сообщений\n/info - информация и правила</i>\n\nНапиши мне что-нибудь, и я покажу, на что способен! Для начала диалога нажми кнопку ниже </b>🚀',
                            reply_markup=kb.start_kb)
    await add_user_if_not_exists(tg_id=message.from_user.id)

@router.callback_query(F.data == 'start_dialog')
async def start_dialog(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'Chat:active':
        await callback.answer('Диалог уже начат</b>')
        await callback.message.answer('<b>Диалог уже активен</b>')
    else:
        await callback.message.answer('<b>Диалог успешно начат. Для завершения используйте /stop</b>')
        await callback.answer('Диалог начат')
        await state.set_state(Chat.active)

@router.message(Command('stop'))
async def stop(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'Chat:active':
        await state.clear()
        await message.answer('<b>Диалог остановлен. Для начала нового используйте /generate</b>')
        await reset_context(tg_id=message.from_user.id)
    elif current_state == 'Chat:waiting':
        await message.answer('<b>Дождитесь ответа, чтобы закончить диалог</b>')
    else:
        await message.answer('<b>Нет активного диалога. Чтобы начать диалог используйте /generate</b>')

@router.message(Command('reset'))
async def reset(message: Message):
    await reset_context(tg_id=message.from_user.id)
    await message.answer('<b>Контекст очищен</b>')

@router.message(Command('generate'))
async def generate_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'Chat:active' or current_state == 'Chat:waiting':
        await message.answer('<b>Диалог уже активен</b>')
    else:
        await message.answer('<b>Диалог успешно начат. Для завершения используйте /stop</b>')
        await state.set_state(Chat.active)

@router.message(Command('info'))
async def info(message: Message):
    await message.answer('🚫 <b><i>Правила:</i></b>\n• Запрещён контент с ненавистью, дискриминацией (раса, пол, религия и др.), оскорблениями групп/личностей.\n• Нельзя использовать для буллинга, угроз, ксенофобии, расизма или унижающих материалов.\nПользователь несет ответственность за свои запросы.\n\n<b>Бот создан в добросовестных целях — соблюдайте уважение! 🙌</b>')

@router.message(Chat.active)
async def chat_active(message: Message, state: FSMContext): 
    current_state = await state.get_state()
    if current_state == 'Chat:waiting':
        await message.answer('<b>Дождитесь ответа</b>')
    else:
        if message.content_type == ContentType.TEXT:
            waiting_message = await message.answer('<b><i>⏳ Ответ генерируется...</i></b>')
            await state.set_state(Chat.waiting)
            ai_response = await answer_to_text_prompt(main_prompt=message.text, tg_id=message.from_user.id)
            ai_response = await style_changer(latex_code=ai_response)
            try:
                await message.answer(ai_response, parse_mode=ParseMode.MARKDOWN)
            except TelegramBadRequest:
                await message.answer(ai_response[:4050], parse_mode=None)
            await state.set_state(Chat.active)
            await waiting_message.delete()
        elif message.content_type == ContentType.PHOTO:
            waiting_message = await message.answer('<b><i>⏳ Ответ генерируется...</i></b>')
            await state.set_state(Chat.waiting)
            ai_response = await answer_to_view_prompt(message=message)
            ai_response = await style_changer(latex_code=ai_response)
            try:
                await message.answer(ai_response, parse_mode=ParseMode.MARKDOWN)
            except TelegramBadRequest:
                await message.answer(ai_response[:4050], parse_mode=None)
            await state.set_state(Chat.active)
            await waiting_message.delete()
        else: 
            await message.answer('<b>Нейросеть воспринимет только текстовые сообщения и изображения</b>')

@router.message(Chat.waiting)
async def waiting(message: Message):
    await message.answer('<b>Дождитесь ответа</b>')

@router.message()
async def other(message: Message):
    await message.answer('<b>Упс, я не знаю такую команду. Для начала диалога используйте /generate</b>')