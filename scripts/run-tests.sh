export $(cat .dev.env | xargs)

python manage.py makemigrations
python manage.py migrate
echo "Starting running tests..."
python manage.py test feedapp.tests.test_channelmanager --failfast
echo "Done running tests!"