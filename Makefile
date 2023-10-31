PIPENV_RUN = pipenv run
BASE_DIR = ./list_page_project
MANAGE_PY = $(BASE_DIR)/manage.py

.PHONY: test clean migrate migrations run createsuperuser

migrations:
	$(PIPENV_RUN) python $(MANAGE_PY) makemigrations

migrate:
	$(PIPENV_RUN) python $(MANAGE_PY) migrate

test:
	cd $(BASE_DIR) && $(PIPENV_RUN) python manage.py test $(target)

clean:
	$(PIPENV_RUN) python $(MANAGE_PY) flush --no-input
	rm -rf .cache
run:
	$(PIPENV_RUN) python $(MANAGE_PY) runserver

createsuperuser:
	$(PIPENV_RUN) python $(MANAGE_PY) createsuperuser