export $(cat .env | xargs)

python manage.py makemigrations && python manage.py migrate
python manage.py test feedapp.tests --failfast
