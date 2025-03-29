docker compose -f docker-compose.yml exec backend python manage.py dumpdata --indent 2 > data/full_data.json
docker compose -f docker-compose.yml cp backend:/app/media/ data/media