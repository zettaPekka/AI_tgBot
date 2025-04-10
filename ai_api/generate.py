from mistralai import Mistral
from aiogram.types import Message

import os
import base64

from core.init_bot import bot
from database.crud import get_context, update_context


api_key = os.getenv('MISTRAL_API_KEY')
model = 'codestral-latest'

client = Mistral(api_key=api_key)

def encode_image(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f'Error: The file {image_path} was not found.')
        return None
    except Exception as e:
        print(f'Error: {e}')
        return None


async def generate_prompt(tg_id: int, main_prompt: str):
    current_context = await get_context(tg_id=tg_id)
    if current_context is None:
        messages_list = [{
            'role':'user',
            'content':main_prompt
        }]
    else:
        messages_list = []
        for index, message in enumerate(current_context):
            if index % 2 == 0:
                messages_list.append({'role':'user', 'content':message['content']})
            else:
                messages_list.append({'role':'system', 'content':message['content']})
        messages_list.append({'role':'user', 'content':main_prompt})
    return messages_list

async def answer_to_text_prompt(main_prompt: str, tg_id: int):
    prompt = await generate_prompt(tg_id=tg_id, main_prompt=main_prompt)
    chat_response = await client.chat.complete_async(
        model = model,
        messages = prompt
    )
    response = chat_response.choices[0].message.content
    new_context = prompt
    new_context.append({'role':'system', 'content':response})
    
    await update_context(tg_id=tg_id, context=new_context)
    return response

async def answer_to_view_prompt(message: Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id=file_id)
    file_path = file.file_path
    await bot.download_file(file_path=file_path, destination=f'images/image_{message.from_user.id}.jpg')
    
    image_path = f'images/image_{message.from_user.id}.jpg'
    base64_image = encode_image(image_path)
    model = 'pixtral-large-latest'
    
    message_text = message.text if message.text is not None else 'Изображение.'
    main_prompt = {
            'role': 'user',
            'content': [
                {
                    'type': 'text',
                    'text': message_text
                },
                {
                    'type': 'image_url',
                    'image_url': f'data:image/jpeg;base64,{base64_image}' 
                }
            ]
        }
    
    context = await get_context(tg_id=message.from_user.id)
    if context is None:
        prompt = [main_prompt]
    else:
        prompt = context
        prompt.append(main_prompt)

    chat_response = await client.chat.complete_async(
        model=model,
        messages=prompt
    )
    chat_response = chat_response.choices[0].message.content
    os.remove(f'images/image_{message.from_user.id}.jpg')
    
    new_context = prompt[:-1]
    new_context.append({'role':'user', 'content':message_text})
    new_context.append({'role':'system', 'content':chat_response})
    await update_context(tg_id=message.from_user.id, context=new_context)

    return chat_response