export $(cat .dev.env | xargs)

python manage.py makemigrations && python manage.py migrate
python manage.py test feedapp.tests.test_channelmanager --failfast