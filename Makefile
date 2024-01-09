MANAGE := poetry run python3 manage.py

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: migrations
migrations:
	@$(MANAGE) makemigrations

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: install
install:
	@poetry install

.PHONY: db-clean
db-clean:
	@rm db.sqlite3 || true

.PHONY: dev_server
dev_server:
	@$(MANAGE) runserver

.PHONY: messages
messages:
	@$(MANAGE) makemessages -l ru

.PHONY: compile
compile:
	poetry run django-admin compilemessages

.PHONY: lint
lint:
	@poetry run flake8 task_manager

.PHONY: port-clean
port-clean:
	sudo fuser -k 8000/tcp

.PHONY: test
test:
	@$(MANAGE) test