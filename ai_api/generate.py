from mistralai import Mistral

from database.crud import get_context, update_context
import os

api_key = os.getenv('MISTRAL_API_KEY')
model = 'codestral-latest'

client = Mistral(api_key=api_key)


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
            print(index, message)
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