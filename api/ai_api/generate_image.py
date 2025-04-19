from urllib.parse import quote
import random


async def image_generator(prompt: str):
    parsed_prompt = quote(prompt.replace(' ', '+'))
    
    seed = random.randint(1,999999)
    image_url = f'https://image.pollinations.ai/prompt/{parsed_prompt}?seed={seed}&width=1024&height=1024&model=dall-e-3&nologo=true&private=false&enhance=false&safe=false'
    return image_url