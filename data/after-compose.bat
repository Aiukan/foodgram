docker compose -f docker-compose.yml exec backend python manage.py makemigrations
docker compose -f docker-compose.yml pull
docker compose build --pull
docker compose -f docker-compose.yml down
docker compose -f docker-compose.yml up -d
sleep 5
docker compose -f docker-compose.yml exec backend python manage.py migrate
docker compose -f docker-compose.yml exec backend python manage.py collectstatic --no-input
docker compose -f docker-compose.yml exec backend sh -c "python manage.py createsuperuser --no-input 2>/dev/null || true"
docker compose -f docker-compose.yml cp data backend:/app/data