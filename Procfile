web: python codango/manage.py collectstatic --noinput --settings=buppli.settings;
web: python codango/manage.py migrate --settings=codango.settings;
web: gunicorn bucketlist_application.wsgi --log-file -
