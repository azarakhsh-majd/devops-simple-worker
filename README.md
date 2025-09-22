# devops-simple-worker
# 1. 
docker compose down -v
docker compose up --build -d
# 2. 
docker ps
# 3. Healthcheck
curl http://localhost:8000/healthz
# 4. 
docker compose exec worker python /app/seed.py
docker compose exec redis redis-cli LLEN crawler_queue
# 5. 
curl http://localhost:8000/metrics | grep crawler
# 6. 
curl http://localhost:8000/test-inc
curl http://localhost:8000/metrics | grep crawler
# for prometheous:

docker run -d --name prometheus -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml:ro   prom/prometheus:latest
 curl http://localhost:9090/targets

