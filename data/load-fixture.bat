docker compose -f docker-compose.yml exec backend python manage.py loaddata data/full_data.json
docker compose -f docker-compose.yml cp data/media backend:/app/