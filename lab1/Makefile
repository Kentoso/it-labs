
cli:
	cd src && python -m cli.cli --interactive

gui:
	cd src && python -m gui.gui

api-generate:
	cd src/api && \
	docker run --rm -v ".:/local" openapitools/openapi-generator-cli generate \
		-i /local/openapi.yaml \
		-g python-flask \
		-o /local/generated \

