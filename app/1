import redis
import os

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
r = redis.from_url(REDIS_URL, decode_responses=False)

for i in range(10):
    r.lpush('crawler_queue', f'http://example.com/seed/{i}')

print('Seeded 10 jobs into crawler_queue')

