export $(cat .env | xargs)
export $(cat .env.local | xargs)

echo $$ >> $PID_FILE

python manage.py collectstatic --clear --noinput && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py runserver --verbosity=3