from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать диалог', callback_data='start_dialog')],
    [InlineKeyboardButton(text='Генерация изображения', callback_data='create_image')]
])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

new_image_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сгенерировать еще', callback_data='create_image')],
])