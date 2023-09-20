dev_server:
	poetry run python3 manage.py runserver

messages:
	poetry run python3 manage.py makemessages -l ru

compile:
	poetry run django-admin compilemessages