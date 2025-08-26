.PHONY: up down logs psql

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

psql:
	docker exec -it spark_postgres psql -U $$POSTGRES_USER -d $$POSTGRES_DB