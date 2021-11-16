#ps -ef|awk 'BEGIN{}{if(match($8, /python/))system("kill -9 " $2)}END{}'
lsof -t -i tcp:8001 | xargs kill -9
export DJANGO_SETTINGS_MODULE=featuringeg_data.settings.base
python manage.py runserver 0.0.0.0:8001
