web: python codango/manage.py collectstatic --noinput --settings=buppli.settings
web: python codango/manage.py migrate --settings=codango.settings
web: gunicorn buppli.wsgi --pythonpath=buppli --log-file -
