import redis


r = redis.Redis()

def check_premium(tg_id: str):
    return bool(r.exists(tg_id))

def add_premium(tg_id: str, time = 30 * 24 * 60 * 60):
    r.setex(tg_id, time, 'premium')


