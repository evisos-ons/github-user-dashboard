DESIGN_SYSTEM_VERSION=`cat .design-system-version`

load-design-system-templates:
	./scripts/load_release.sh onsdigital/design-system $(DESIGN_SYSTEM_VERSION)

clean:
	rm -rf .mypy_cache
	rm -rf .ruff_cache

lint: 
	poetry run black --check .
	poetry run ruff check . || true
	poetry run mypy .

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