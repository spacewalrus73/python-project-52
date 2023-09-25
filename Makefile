MANAGE := poetry run python3 manage.py

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

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
	poetry run python3 manage.py runserver

.PHONY: messages
messages:
	poetry run python3 manage.py makemessages -l ru

.PHONY: compile
compile:
	poetry run django-admin compilemessages

.PHONY: lint
lint:
	@poetry run flake8 task_manager