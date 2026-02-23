.PHONY: up down build migrate superuser test shell

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up --build

migrate:
	docker compose exec web python manage.py migrate

superuser:
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web python manage.py test

shell:
	docker compose exec web python manage.py shell
