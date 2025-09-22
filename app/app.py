import os
import redis
import time
import random
import threading
from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# --- Redis setup ---
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)

# --- FastAPI app ---
app = FastAPI()

# --- Prometheus Counters ---
crawler_fetch_total = Counter("crawler_fetch_total", "Total number of fetch attempts")
crawler_success_total = Counter("crawler_success_total", "Total number of successful fetches")
crawler_error_total = Counter("crawler_error_total", "Total number of failed fetches")


# --- Healthcheck ---
@app.get("/healthz")
def healthz():
    try:
        r.ping()
        return {"status": "ok"}
    except Exception:
        return {"status": "unhealthy"}


# --- Prometheus metrics endpoint ---
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# --- Test endpoint: manual increment counters ---
@app.get("/test-inc")
def test_inc():
    crawler_fetch_total.inc()
    crawler_success_total.inc()
    return {"msg": "Counters incremented"}


# --- Worker thread to process Redis queue ---
def worker_loop():
    while True:
        try:
            job = r.rpop("crawler_queue")
            if job:
                crawler_fetch_total.inc()
                print(f"[Worker] Fetched job: {job}")

                # Mock fetch: random success/error
                if random.random() < 0.8:  # 80% success rate
                    crawler_success_total.inc()
                    print(f"[Worker] Success: {job}")
                else:
                    crawler_error_total.inc()
                    print(f"[Worker] Error: {job}")
            else:
                time.sleep(1)
        except Exception as e:
            print("[Worker] Error:", e)
            time.sleep(5)


# --- Start worker thread in background ---
threading.Thread(target=worker_loop, daemon=True).start()

