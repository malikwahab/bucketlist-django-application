web: python bucketlist_application/manage.py makemigrations --settings=bucketlist_application.settings;
web: python bucketlist_application/manage.py migrate --settings=bucketlist_application.settings;
web: gunicorn bucketlist_application.wsgi --log-file -
