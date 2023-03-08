run:
	python3 manage.py runserver
	
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

test:
	./manage.py test
startproject:
	django-admin startproject main .

pull_origin:
	git add .
	git commit -m 'origin commit'
	git pull origin origin

pull_baha:
	git add .
	git commit -m 'baha commit'
	git pull origin baha

celery_run:
	celery -A main worker -l debug

celery_beat:
	celery -A main beat