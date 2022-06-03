export $(cat .env | xargs)

python manage.py collectstatic --clear --noinput && \
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py runserver 8001 --verbosity=3