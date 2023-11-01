PIPENV_RUN = pipenv run
BASE_DIR = ./list_page_project
MANAGE_PY = $(BASE_DIR)/manage.py
create_data_script = ./create_data.py

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

create_superuser:
	@echo "Creating superuser..."
	$(PIPENV_RUN) python $(MANAGE_PY) shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password') if not User.objects.filter(username='admin').exists() else print('Superuser already exists.')"


create_test_data:
	@echo "Creating test data..."
	cd $(BASE_DIR) && $(PIPENV_RUN) python $(create_data_script)

# 전체 세팅 (마이그레이션 적용, 슈퍼유저 생성, 테스트 데이터 생성)
setup: migrations migrate createsuperuser create_test_data
	@echo "Setup complete."