export $(cat .env | xargs)

if [ -z $STREAM_SERVER_PORT ]; then
    printf "Provide a port for the stream server"
    exit 77
fi

if [ -z $STREAM_PROJECT_DIR ]; then
    printf "Provide a directory for the stream project"
    exit 77
fi

# optionally activate the virtual environment for the api server
if [ ! -z $STREAM_ENV_DIR ]; then
    printf "Activating virtual environment for api server...\n"
    source "${STREAM_ENV_DIR}/bin/activate"
fi

python $STREAM_PROJECT_DIR/manage.py collectstatic --clear --noinput && \
python $STREAM_PROJECT_DIR/manage.py makemigrations && \
python $STREAM_PROJECT_DIR/manage.py migrate && \
python $STREAM_PROJECT_DIR/manage.py runserver $STREAM_SERVER_PORT --verbosity=3