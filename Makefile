.PHONY: pip run

# Makefile
env/bin/activate:
	virtualenv --system-site-packages env

# target: rm-pyc — delete *.pyc files
rm-pyc:
	find . -name '*.pyc' -delete

# target: rm-pyc — delete *.pyc files
env-vars:
	export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE-chrn.settings}
	export CHRN_ENV_ROLE=${CHRN_ENV_ROLE-LOCAL}
	export PYTHONPATH=./

# target: setup — bootstrap environment
setup: env/bin/activate requirements.txt
	. env/bin/activate; pip install -Ur requirements.txt

# target: run — run project
run: env/bin/activate requirements.txt
	. env/bin/activate; ./setup-env-vars.sh gunicorn --reload --config etc/gunicorn/chrn.py chrn.wsgi

# target: help — this help
help:
	@egrep "^# target:" [Mm]akefile
