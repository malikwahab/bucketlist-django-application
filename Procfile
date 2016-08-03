web: python manage.py makemigrations --settings=bucketlist_application.settings;
web: python manage.py migrate --settings=bucketlist_application.settings;
web: gunicorn bucketlist_application.wsgi --log-file -
