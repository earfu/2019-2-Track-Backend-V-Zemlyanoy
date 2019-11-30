up:
	docker-compose up -d

migrate: up
	docker-compose exec django python3 messanger/manage.py migrate