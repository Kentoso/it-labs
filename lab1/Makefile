
cli:
	cd src && python -m cli.cli --interactive

gui:
	cd src && python -m gui.gui

api-generate:
	cd src/api && \
	docker run --rm -v ".:/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi.yaml \
		--additional-properties=packageName=server \
		--global-property=apiTests=false,modelTests=false \
		-g python-flask \
		-o /local/generated \

api:
	docker compose -f api-docker-compose.yaml up --build -d

watch-api:
	docker compose -f api-docker-compose.yaml watch

distributed:
	docker compose -f distributed-docker-compose.yaml up --build -d