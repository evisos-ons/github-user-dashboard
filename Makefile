DESIGN_SYSTEM_VERSION=`cat .design-system-version`

load-design-system-templates:
	./scripts/load_release.sh onsdigital/design-system $(DESIGN_SYSTEM_VERSION)

clean:
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf __pycache__

lint: 
	poetry run black . || true
	poetry run ruff check . --fix || true
	poetry run mypy . || true

install: 
	poetry install --only main --no-root

install-dev: 
	poetry install --no-root

run-dev: load-design-system-templates
	flask --app application run --debug

run: load-design-system-templates
	flask --app application run

add:
	export GITHUB_TOKEN=$(token)