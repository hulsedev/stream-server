export $(cat .env | xargs)

if [ -z $STREAM_SERVER_PORT ]; then
    printf "Provide a port for the stream server"
    exit 77
fi

python manage.py collectstatic --clear --noinput && \
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py runserver $STREAM_SERVER_PORT --verbosity=3