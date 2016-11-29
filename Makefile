.PHONY: pip run up stop build buildup

# Makefile
env/bin/activate:
	virtualenv --system-site-packages env

# target: rm-pyc — delete *.pyc files
rm-pyc:
	find . -name '*.pyc' -delete

# target: setup — bootstrap environment
setup: env/bin/activate requirements.txt
	. env/bin/activate; pip install -Ur requirements.txt

# target: pip - install python requirements
pip:
	pip install -r requirements.txt

# target: run — run project
run: env/bin/activate requirements.txt
	. env/bin/activate; gunicorn --reload --config etc/gunicorn/chrn.py chrn.wsgi

# target: build - build docker image
build:
	docker-compose build

# target: build - build docker image
stop:
	docker-compose stop

# target: up - start docker image
up: stop
	docker-compose up -d
	docker ps

# target: buildup - build and start docker image
buildup: stop build up

# target: makemessages - generate message files
makemessages:
	./app/manage.py makemessages --locale ru --locale en --ignore env

# target: pip-comile
pip-compile:
	pip-compile requirements.in -o requirements.txt

# target: tx - set translations
tx:
	tx set --auto-local -r pong.djangopo 'locale/<lang>/LC_MESSAGES/django.po' \
	--source-lang en --type PO --source-file locale/en/LC_MESSAGES/django.po --execute
	# tx set -r pong.djangopo -l en locale/en/LC_MESSAGES/django.po
	tx set -r pong.djangopo -l ru locale/ru/LC_MESSAGES/django.po

# target: help — this help
help:
	@egrep "^# target:" [Mm]akefile
