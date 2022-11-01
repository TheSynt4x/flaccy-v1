.PHONY: fmt
fmt:
	black .
	isort . --profile black
	autoflake --in-place --remove-all-unused-imports --recursive .

.PHONY: lint
lint:
	black --check .
	isort --profile black --check .
	flake8 .

.PHONY: devserver
devserver:
	sh ./scripts/devserver.sh
