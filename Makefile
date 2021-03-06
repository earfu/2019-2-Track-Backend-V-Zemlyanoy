freeze:
	pip freeze > ./messanger/requirements.txt

build:
	docker-compose build

up:
	docker-compose up -d

anew:
	docker-compose down
	docker-compose build

migrate: up
	docker-compose exec django python3 messanger/manage.py makemigrations	
	docker-compose exec django python3 messanger/manage.py migrate

flush: up
	docker-compose exec django python3 messanger/manage.py flush

fixturize: up
	docker-compose exec django python3 messanger/fixturize.py

cli: up
	docker-compose exec django python3

shell: up
	docker-compose exec django python3 messanger/manage.py shell

superuser: up
	docker-compose exec django python3 messanger/manage.py createsuperuser

coverage_run: up
	docker-compose exec django coverage run --source="./messanger" ./messanger/manage.py test messanger

coverage_report: up
	docker-compose exec django coverage report

selenium: up
	docker-compose exec django python3 messanger/manage.py test chats.selenium_tests.SeleniumTestTry.test_login

profile:
	python3 -m cProfile -o "profiled.txt" messanger/manage.py runserver

profiled:
	python3 -i print_profiled.py